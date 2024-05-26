from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import json, os
import thread_pool

import simuliot
import os
app = Flask(__name__)

# Routes
# GET /devices

devices = []
global devicesCurrentSession
devicesCurrentSession = []
global threads
threads = None


device_thread_pid = None

conn = simuliot.connect_db()

PID = os.getpid()
with open('simuliot_backend.pid', 'w') as f:
    f.write(str(PID))

try:
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT * FROM DEVICES")
        rows = cur.fetchall()
        for row in rows:
            device = {
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "manufacturer": row[3]
            }
            devices.append(device)
        cur.close()
        conn.close()
except Exception as e:
    simuliot.logger.critical('SQL Error: ' + str(e))


@app.route('/', methods=['GET'])
def index():
    return "SimulIOT Backend"


@app.route('/all-devices', methods=['GET'])
def get_all_devices():
    simuliot.logger.info('Request to get all devices')
    return jsonify(devices)

@app.route('/devices', methods=['GET'])
def get_devices():
    return jsonify(devicesCurrentSession)

# GET /devices/<id>/reading
@app.route('/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = next((device for device in devicesCurrentSession if device.deviceID == device_id), None)
    if device:
        return json.dumps(device.__dict__)
    else:
        simuliot.logger.error('Device not found. id: ' + str(device_id))
        return jsonify({"error": "Device not found"}), 404

# POST /devices
@app.route('/devices', methods=['POST'])
def add_device():
    global devicesCurrentSession
    devicesJson = request.get_json()
    ## check if devicesCurrentSession is empty. If it is, then add the devices to the list
    if len(devicesCurrentSession) == 0:
        devicesCurrentSession = simuliot.gen_devices(devicesJson)
    else:
        return jsonify({"error": "Session already started. Please clear the session before adding new devices"}), 400
    return jsonify({"sucess":'Devices added to session. Awaiting save operation'}), 201

@app.route('/store-session', methods=['GET'])
def store_session():
    global devicesCurrentSession
    ## Check if the table DevicesSession exists. If not, create it
    try:
        conn = simuliot.connect_db()
        if conn is not None:
            cur = conn.cursor()

            ## Drop the table if it exists
            cur.execute("DROP TABLE IF EXISTS CURRENTDEVICESESSION")
            cur.execute("CREATE TABLE IF NOT EXISTS CURRENTDEVICESESSION (id TEXT PRIMARY KEY, name TEXT, type TEXT, location TEXT)")

        ## Store the current session in the database. The current session is stored in the devicesCurrentSession list
            for device in devicesCurrentSession:
                sqlstring = "INSERT INTO CURRENTDEVICESESSION (id, name, type, location) VALUES ('{}', '{}', '{}', '{}')".format(str(device.UUID), str(device.deviceName), str(device.type), str(device.location))
                cur.execute(sqlstring)
            conn.commit()
            cur.close()
            conn.close()
    except Exception as e:
        simuliot.logger.critical('SQL Error Store Session: ' + str(e) + ' ' + str(sqlstring))
        return "A database error has occured.", 500

    return "Session has been stored.", 201

@app.route('/retrieve-session', methods=['GET'])
def retrieve_session():
    global devicesCurrentSession
    deviceSessionJSON = []
    try:
        for device in devicesCurrentSession:
            deviceSessionJSON.append({
                "id": device.UUID,
                "name": device.deviceName,
                "type": device.type,
                "location": device.location,
                "value": device.reading() if hasattr(device, 'reading') else None
            }) ## Add device information to the list
        return jsonify(deviceSessionJSON), 200
    except Exception as e:
        simuliot.logger.critical('Session Retrieval Error: ' + str(e))
        return "An error has ocurred obtaining current session", 500

@app.route('/api/session', methods=['GET']) ## Get the current session from DB
def get_session():
    deviceSessionJSON = []
    try:
        conn = simuliot.connect_db()
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM CURRENTDEVICESESSION")
            rows = cur.fetchall()
            for row in rows:
                deviceSessionJSON.append({
                    "id": row[0],
                    "name": row[1],
                    "type": row[2],
                    "location": row[3]
                })
            cur.close()
            conn.close()
    except Exception as e:
        simuliot.logger.critical('SQL Error: ' + str(e))
        return "An error has occured retrieving the session", 500
    return jsonify(deviceSessionJSON), 200

@app.route('/clear-session', methods=['DELETE'])
def clear_session():
    devicesCurrentSession.clear()
    return "Current session has been cleared.", 200

# PUT /devices/<id>
@app.route('/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = next((device for device in devices if device['UUID'] == device_id), None)
    if device:
        device.update(request.get_json())
        return jsonify(device)
    else:
        return jsonify({"error": "device not found"}), 404

# DELETE /devices/<id>
@app.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = next((device for device in devices if device['UUID'] == device_id), None)
    if device:
        devices.remove(device)
        return jsonify({"message": "Device removed from current session"}), 200
    else:
        return jsonify({"error": "Invalid request"}), 404


@app.route('/start-session', methods=['GET'])
def start_session():
    ## Call ThreadPool to start the session
    if len(devicesCurrentSession) == 0:
        return "No devices in session", 404
    global threads
    threads = thread_pool.ThreadPool(devicesCurrentSession)
    threads.start()
    return "Session has been started", 200

@app.route('/pause-session', methods=['GET'])
def pause_session():
    global threads
    if threads is None:
        return "No session to pause", 404
    threads.pause()
    return "Session has been paused", 200

@app.route('/resume-session', methods=['GET'])
def resume_session():
    global threads
    if threads is None:
        return "No session to resume", 404
    threads.resume()
    return "Session has been resumed", 200

@app.route('/kill-session',  methods=['GET'])
def kill_session():
    global threads
    if threads is None:
        return "No session to kill", 404
    simuliot.logger.info('Killing session with {} devices'.format(len(threads.threads)))
    if device_thread_pid != 0:
        threads.stop()
        devicesCurrentSession.clear()
        return "Session has been killed", 200

@app.route('/session-status', methods=['GET'])
def session_status():
    global threads
    if threads is None:
        return "No session running", 404
    return threads.status()

@app.route('/update_device_value', methods=['POST'])
def publish_device():
    device = next((device for device in devicesCurrentSession if device.UUID == request.get_json()['deviceID']), None)
    print (device)
    if device:
        device._publish(device.reading()['state_topic'], request.get_json()['value'])
        return "Device published", 200
    else:
        return "Device not found", 404


if __name__ == "__main__":
    app.run('127.0.0.1', 8088, debug=True)