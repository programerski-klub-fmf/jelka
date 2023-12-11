#!/usr/bin/python3
import flask
import threading
import os
import secrets
import subprocess
import hashlib
import base64
import time
import signal

http = flask.Flask(__name__)
onemogočeni = set(["onemogočen.py"])
skrivnost = secrets.token_bytes(8)
čas_vzorca = 30
proces = None
naslednji = None

def trenuten():
	if proces:
		return proces.args[1]
	return None

def json_status():
	return "data: " + http.json.dumps({"čas": čas_vzorca, "vzorci": os.listdir("../patterns"), "trenuten": trenuten(), "onemogočeni": [x for x in onemogočeni]}) + "\n\n"

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
	return flask.render_template("index.html");

@http.route("/stream/", methods=["GET"])
def stream():
	return flask.Response(http_event_stream(), headers={"Access-Control-Allow-Origin": "*", "Content-Type": "text/event-stream"})

@http.route("/<koda>", methods=["POST"])
def update(koda):
	global onemogočeni
	global čas_vzorca
	global naslednji
	if koda not in kode():
		return flask.Response(http.json.dumps({"napaka": {"koda": 1, "besedilo": "napačna koda"}}), status=200)
	data = flask.json.loads(flask.request.data)
	if "omogoči" in data.keys():
		onemogočeni -= set(data["omogoči"])
	if "onemogoči" in data.keys():
		onemogočeni |= set(data["onemogoči"])
	if "čas" in data.keys():
		if data["čas"] < 1 or data["čas"] > 300:
			return flask.Response(http.json.dumps({"napaka": {"koda": 2, "besedilo": "čas ni v [1,300]"}}), status=200)
		čas_vzorca = data["čas"]
	sprememba_stanja.set()
	if "začni" in data.keys() and type(data["začni"]) == str:
		naslednji = data["začni"]
		začni_vzorec.set()
	return "true"

@http.route("/<koda>", methods=["OPTIONS"])
def update_preflight(koda):
	return flask.Response("", status=204, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type", "Access-Control-Max-Age": "86400"})

def kode():
	return [base64.b64encode(hashlib.sha256(skrivnost+bytes(str(int(time.time()/1000)), encoding="utf-8")).digest()).replace(b"/", b"").replace(b"+", b"")[:4].lower().decode(), base64.b64encode(hashlib.sha256(skrivnost+bytes(str(int(time.time()/1000)-1), encoding="utf-8")).digest()).replace(b"/", b"").replace(b"+", b"")[:4].lower().decode(), os.getenv("KODA")]

def zaznaj_smrt():
	proces.wait()
	začni_vzorec.set()

die = False
subprocess_manager_thread = None

def subprocess_manager():
	global naslednji
	global proces
	global začni_vzorec
	while True:
		if not naslednji:
			vzorci = set(os.listdir("../patterns"))-set(["začasen.py"])-onemogočeni
			naslednji = sorted(vzorci)[0]
		if die:
			return
		print("daemon: starting " + naslednji)
		proces = subprocess.Popen(["./wrapper.py", naslednji])
		sprememba_stanja.set()
		vzorci = set(os.listdir("../patterns"))-set(["začasen.py"])-onemogočeni
		naslednji = sorted(vzorci)[0]
		if trenuten() in vzorci:
			naslednji = sorted(vzorci)[(sorted(vzorci).index(trenuten())+1)%len(vzorci)]
		začni_vzorec.clear()
		threading.Thread(target=zaznaj_smrt).start()
		razlog = začni_vzorec.wait(timeout=čas_vzorca)
		proces.send_signal(subprocess.signal.SIGINT)
		proces.wait()

začni_vzorec = threading.Event()
sprememba_stanja = threading.Event()

def samomor(signal_descriptor, stack_frame):
	global die
	die = True
	global proces
	global subprocess_manager_thread
	print("daemon: exiting")
	if subprocess_manager_thread:
		print("daemon: subprocess_manager_thread: waiting to join ...")
		subprocess_manager_thread.join()
	else:
		print("daemon: subprocess_manager_thread was not started, not waiting to join.")
	proces.send_signal(subprocess.signal.SIGINT)
	print("daemon: waiting for proces to terminate")
	proces.wait()
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
