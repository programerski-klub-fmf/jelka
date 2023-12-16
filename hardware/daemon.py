#!/usr/bin/python3
import base64
import hashlib
import os
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

disabled_patterns = set(os.getenv("DISABLED_PATTERNS", "").split(","))
hidden_patterns = set(os.getenv("HIDDEN_PATTERNS", "").split(","))


next_pattern = None

process = None

def current_pattern():
	if process:
		return process.args[1]
	return None

def json_status():
	return "data: " + http.json.dumps({"čas": pattern_time, "vzorci": os.listdir("../patterns"), "trenuten": current_pattern(), "onemogočeni": [x for x in disabled_patterns]}) + "\n\n"

def http_event_stream():
	yield json_status()
	while sprememba_stanja.wait():
		yield json_status()
		print("geslo je: " + kode()[0])
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
	global next_pattern
	if not koda or koda not in kode():
		return flask.Response(http.json.dumps({"napaka": {"koda": 1, "besedilo": "napačna koda"}}), status=200)
	data = flask.json.loads(flask.request.data)
	if "omogoči" in data.keys():
		disabled_patterns -= set(data["omogoči"])
	if "onemogoči" in data.keys():
		disabled_patterns |= set(data["onemogoči"])
	if "čas" in data.keys():
		if data["čas"] < 1 or data["čas"] > 300:
			return flask.Response(http.json.dumps({"napaka": {"koda": 2, "besedilo": "čas ni v [1,300]"}}), status=200)
		pattern_time = data["čas"]
	sprememba_stanja.set()
	if "začni" in data.keys() and type(data["začni"]) == str:
		next_pattern = data["začni"]
		začni_vzorec.set()
	return "true"

@http.route("/<koda>", methods=["OPTIONS"])
def update_preflight(koda):
	return flask.Response("", status=204, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type", "Access-Control-Max-Age": "86400"})

def kode():
	return [base64.b64encode(hashlib.sha256(secret + bytes(str(int(time.time() / 1000)), encoding="utf-8")).digest()).replace(b"/", b"").replace(b"+", b"")[:6].lower().decode(), base64.b64encode(hashlib.sha256(secret + bytes(str(int(time.time() / 1000) - 1), encoding="utf-8")).digest()).replace(b"/", b"").replace(b"+", b"")[:4].lower().decode(), os.getenv("KODA")]

def zaznaj_smrt():
	process.wait()
	začni_vzorec.set()

die = False
subprocess_manager_thread = None

def subprocess_manager():
	global next_pattern
	global process
	global začni_vzorec
	while True:
		if len(vzorci) == 0:
			continue
		if not next_pattern:
			vzorci = set(os.listdir("../patterns")) - set(["začasen.py"]) - disabled_patterns
			next_pattern = sorted(vzorci)[0]
		if die:
			return
		print("daemon: starting " + next_pattern)
		process = subprocess.Popen(["python", "./wrapper.py", next_pattern])
		sprememba_stanja.set()
		vzorci = set(os.listdir("../patterns")) - set(["začasen.py"]) - disabled_patterns
		next_pattern = sorted(vzorci)[0]
		if current_pattern() in vzorci:
			next_pattern = sorted(vzorci)[(sorted(vzorci).index(current_pattern()) + 1) % len(vzorci)]
		print("TRENUTEN", current_pattern(), "NASLEDNJI", next_pattern, "VSI", vzorci)
		začni_vzorec.clear()
		threading.Thread(target=zaznaj_smrt).start()
		začni_vzorec.wait(timeout=pattern_time)
		process.send_signal(subprocess.signal.SIGINT)
		process.wait()

začni_vzorec = threading.Event()
sprememba_stanja = threading.Event()

def samomor(signal_descriptor, stack_frame):
	global die
	die = True
	global process
	global subprocess_manager_thread
	print("daemon: exiting")
	if subprocess_manager_thread:
		print("daemon: subprocess_manager_thread: waiting to join ...")
		subprocess_manager_thread.join()
	else:
		print("daemon: subprocess_manager_thread was not started, not waiting to join.")
	process.send_signal(subprocess.signal.SIGINT)
	print("daemon: waiting for proces to terminate")
	process.wait()
	os._exit(0)

if __name__ == "__main__":
	signal.signal(signal.SIGINT, samomor)
	signal.signal(signal.SIGHUP, samomor)
	signal.signal(signal.SIGTERM, samomor)
	port = 6969
	if os.getenv("PORT"):
		port = int(os.getenv("PORT"))
	threading.Thread(target=lambda: http.run(host="::", port=port, debug=True, use_reloader=False)).start()
	subprocess_manager_thread = threading.Thread(target=subprocess_manager)
	subprocess_manager_thread.start()
