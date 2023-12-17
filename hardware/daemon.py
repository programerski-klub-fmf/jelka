#!/usr/bin/python3

import base64
import hashlib
import os
import pathlib
import re
import secrets
import signal
import subprocess
import threading
import time

import flask

http = flask.Flask(__name__)
secret = secrets.token_bytes(8)

name_regex = re.compile(r"# *NAME: ((?:[-_+*.!? ]|\w)+)")

pattern_time = int(os.getenv("PATTERN_TIME", 30))

disabled_patterns = set(os.getenv("DISABLED_PATTERNS", "").split(",")) - {""}
hidden_patterns = set(os.getenv("HIDDEN_PATTERNS", "").split(",")) - {""}

forced_pattern: str | None = None
current_pattern: str | None = None
current_process: subprocess.Popen | None = None


def get_patterns():
	patterns = set()

	for pattern in pathlib.Path("../patterns/").iterdir():
		if not pattern.is_file():
			continue

		if pattern.name in hidden_patterns:
			continue

		name = pattern.name

		for line in pattern.open(encoding="utf-8"):
			if match := name_regex.search(line):
				name = match.group(1)
				break

		# name, filename, enabled
		patterns.add((name, pattern.name, pattern.name not in disabled_patterns))

	return sorted(patterns)

def json_status():
	return "data: " + http.json.dumps({"time": pattern_time, "patterns": get_patterns(), "disabled": list(disabled_patterns), "current": current_pattern}) + "\n\n"

def http_event_stream():
	yield json_status()
	while sprememba_stanja.wait():
		yield json_status()
		print("daemon: current password: " + kode()[0])
		sprememba_stanja.clear()

@http.route("/vzorci/<vzorec>", methods=["GET"])
def vzorec(vzorec):
	if "/" in vzorec:
		return flask.Response(http.json.dumps({"napaka": {"koda": 3, "besedilo": "vzorec ne sme vsebovati poševnice"}}), status=403)
	return flask.send_file("../patterns/" + vzorec, mimetype="text/x-python")

@http.route("/", methods=["GET"])
def index():
	return flask.render_template("index.html")

@http.route("/stream/", methods=["GET"])
def stream():
	return flask.Response(http_event_stream(), headers={"Access-Control-Allow-Origin": "*", "Content-Type": "text/event-stream"})

@http.route("/<koda>", methods=["POST"])
def update(koda):
	global disabled_patterns
	global pattern_time
	global forced_pattern
	if not koda or koda not in kode():
		return flask.Response(http.json.dumps({"napaka": {"koda": 1, "besedilo": "Napačno geslo!"}}), status=200)
	data = flask.json.loads(flask.request.data)
	print("daemon: received data:", data)
	if "omogoči" in data.keys():
		disabled_patterns -= set(data["omogoči"])
	if "onemogoči" in data.keys():
		disabled_patterns |= set(data["onemogoči"])
	if "čas" in data.keys():
		if data["čas"] < 1 or data["čas"] > 600:
			return flask.Response(http.json.dumps({"napaka": {"koda": 2, "besedilo": "Čas mora biti med 1 in 600 sekund!"}}), status=200)
		pattern_time = data["čas"]
	sprememba_stanja.set()
	if "začni" in data.keys() and type(data["začni"]) == str:
		forced_pattern = data["začni"]
		začni_vzorec.set()
	return "true"

@http.route("/<koda>", methods=["OPTIONS"])
def update_preflight(koda):
	return flask.Response("", status=204, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type", "Access-Control-Max-Age": "86400"})

def kode():
	return [base64.b64encode(hashlib.sha256(secret + bytes(str(int(time.time() / 1000)), encoding="utf-8")).digest()).replace(b"/", b"").replace(b"+", b"")[:6].lower().decode(), base64.b64encode(hashlib.sha256(secret + bytes(str(int(time.time() / 1000) - 1), encoding="utf-8")).digest()).replace(b"/", b"").replace(b"+", b"")[:4].lower().decode(), os.getenv("KODA")]

def zaznaj_smrt():
	current_process.wait()
	začni_vzorec.set()

die = False
subprocess_manager_thread = None

def subprocess_manager():
	global forced_pattern
	global current_pattern
	global current_process
	global začni_vzorec

	while True:
		if die:
			return

		patterns = [pattern[1] for pattern in get_patterns() if pattern[2]]
		print(f"daemon: enabled patterns: {list(patterns)}")
		print(f"daemon: disabled patterns: {list(disabled_patterns)}")

		if not patterns:
			sprememba_stanja.wait(timeout=5)
			continue

		try: current_pattern = patterns[(patterns.index(current_pattern) + 1) % len(patterns)]
		except ValueError: current_pattern = patterns[0]

		if forced_pattern:
			current_pattern = forced_pattern
			forced_pattern = None

		print(f"daemon: starting pattern {current_pattern}")
		current_process = subprocess.Popen(["./wrapper.py", current_pattern])

		sprememba_stanja.set()
		začni_vzorec.clear()

		threading.Thread(target=zaznaj_smrt).start()
		začni_vzorec.wait(timeout=pattern_time)
		current_process.send_signal(subprocess.signal.SIGINT)
		current_process.wait()

začni_vzorec = threading.Event()
sprememba_stanja = threading.Event()

def samomor(signal_descriptor, stack_frame):
	global die
	die = True
	global current_process
	global subprocess_manager_thread
	print("daemon: exiting")
	if subprocess_manager_thread:
		print("daemon: waiting to join subprocess_manager_thread")
		subprocess_manager_thread.join()
	else:
		print("daemon: subprocess_manager_thread was not started, not waiting to join")
	current_process.send_signal(subprocess.signal.SIGINT)
	print("daemon: waiting for proces to terminate")
	current_process.wait()
	os._exit(0)


if __name__ == "__main__":
	signal.signal(signal.SIGINT, samomor)
	signal.signal(signal.SIGHUP, samomor)
	signal.signal(signal.SIGTERM, samomor)

	port = int(os.getenv("PORT", 6969))
	debug = os.getenv("DEBUG", "0") == "1"

	threading.Thread(target=lambda: http.run(host="::", port=port, debug=debug, use_reloader=False)).start()

	subprocess_manager_thread = threading.Thread(target=subprocess_manager)
	subprocess_manager_thread.start()
