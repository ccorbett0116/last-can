#!/usr/bin/env python3
"""
List the robot's ROS topics from the lab PC, and optionally watch one.
No SSH needed: it asks the robot through rosbridge.

    python tools/list_topics.py                   # every topic and its message type
    python tools/list_topics.py servo             # only topics containing "servo"
    python tools/list_topics.py --echo /cmd_vel   # print messages as they arrive (Ctrl+C stops)

A topic marked NO PUBLISHER exists only because something is listening to it:
no data will ever arrive on it until some node publishes.

Needs the rosapi node on the robot (rosbridge launch files normally start it).
If this prints nothing useful, use the SSH method in docs/robot_guide.md.

Requires:  pip install websocket-client
"""
import json
import sys
import time

try:
    import websocket                    # from the websocket-client package
except ImportError:
    sys.exit("websocket-client is not installed. Run:  pip install websocket-client")

ROBOT_IP       = "192.168.149.1"        # same address as in your GUI
ROSBRIDGE_PORT = 9090
MAX_PRINT      = 400                    # characters shown per message when echoing


def call_service(ws, service, args=None, timeout=5.0):
    """Call a ROS service through rosbridge and return its answer (a dict),
    or None if nothing came back in time."""
    call_id = f"call:{service}:{time.time()}"
    ws.send(json.dumps({"op": "call_service", "id": call_id,
                        "service": service, "args": args or {}}))
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            reply = json.loads(ws.recv())
        except websocket.WebSocketTimeoutException:
            break
        if reply.get("op") == "service_response" and reply.get("id") == call_id:
            return reply.get("values") if reply.get("result", True) else None
    return None


def list_topics(ws, text):
    found = call_service(ws, "/rosapi/topics")
    if not found:
        sys.exit("No answer from /rosapi/topics - is the rosapi node running on the robot?")
    for topic, msg_type in sorted(zip(found.get("topics", []), found.get("types", []))):
        if text in topic.lower():
            pubs = call_service(ws, "/rosapi/publishers", {"topic": topic}) or {}
            note = "" if pubs.get("publishers") else "   (NO PUBLISHER)"
            print(f"{topic:<55} {msg_type}{note}")


def echo(ws, topic):
    found = call_service(ws, "/rosapi/topic_type", {"topic": topic}) or {}
    msg_type = found.get("type")
    if not msg_type:
        sys.exit(f"{topic}: no such topic (or rosapi is not running)")
    print(f"{topic}  [{msg_type}]   Ctrl+C to stop")
    ws.send(json.dumps({"op": "subscribe", "topic": topic, "type": msg_type}))
    try:
        while True:
            try:
                reply = json.loads(ws.recv())
            except websocket.WebSocketTimeoutException:
                continue
            if reply.get("op") == "publish" and reply.get("topic") == topic:
                text = json.dumps(reply.get("msg"))
                print(text if len(text) <= MAX_PRINT else text[:MAX_PRINT] + " ...")
    except KeyboardInterrupt:
        pass


def main():
    try:
        ws = websocket.create_connection(f"ws://{ROBOT_IP}:{ROSBRIDGE_PORT}", timeout=5)
    except Exception as exc:
        sys.exit(f"Could not connect to rosbridge at {ROBOT_IP}:{ROSBRIDGE_PORT}: {exc}")
    ws.settimeout(1.0)
    try:
        if "--echo" in sys.argv:
            position = sys.argv.index("--echo") + 1
            if position >= len(sys.argv):
                sys.exit("--echo needs a topic name, e.g.  --echo /cmd_vel")
            echo(ws, sys.argv[position])
        else:
            list_topics(ws, next((a for a in sys.argv[1:] if not a.startswith("-")), "").lower())
    finally:
        ws.close()


if __name__ == "__main__":
    main()
