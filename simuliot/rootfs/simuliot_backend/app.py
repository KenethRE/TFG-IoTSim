from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from signal import pthread_kill, SIGINT
from threading import Thread
import json, os

import simuliot
import os
app = Flask(__name__)

# Routes
# GET /devices

devices = []
devicesCurrentSession = []

device_thread_pid = None

conn = simuliot.connect_db()
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
    new_devices = request.get_json()
    ## check if devicesCurrentSession is empty. If it is, then add the devices to the list
    if len(devicesCurrentSession) == 0:
        for device in new_devices:
            if device['Type'] == 'Thermometer':
                new_device = simuliot.getTempDevice(device['DeviceID'], device['Name'], device['Location'], device['Type'], True)
                devicesCurrentSession.append(new_device)
            elif device['Type'] == 'Switch_Config':
                new_device = simuliot.getSwitchConfigurableDevice(device['DeviceID'], device['Name'], device['Location'], device['Type'], None)
                devicesCurrentSession.append(new_device)
            elif device['Type'] == 'Switch':
                new_device = simuliot.getSwitchDevice(device['DeviceID'], device['Name'], device['Location'], device['Type'])
                devicesCurrentSession.append(new_device)
            elif device['Type'] == 'Water_Flow':
                new_device = simuliot.getFlowDevice(device['DeviceID'], device['Name'], device['Location'], device['Type'], 'Water_Flow')
                devicesCurrentSession.append(new_device)
            elif device['Type'] == 'Air_Flow':
                new_device = simuliot.getFlowDevice(device['DeviceID'], device['Name'], device['Location'], device['Type'], 'Air_Flow')
                devicesCurrentSession.append(new_device)
            elif device['Type'] == 'Thermo_Switch':
                new_device = simuliot.getTempSwitchDevice(device['DeviceID'], device['Name'], device['Location'], device['Type'])
                devicesCurrentSession.append(new_device)
            elif device['Type'] == 'US_Sensor':
                new_device = simuliot.getPresenceDevice(device['DeviceID'], device['Name'], device['Location'], device['Type'])
                devicesCurrentSession.append(new_device)
            elif device['Type'] == 'Volume_Sensor':
                new_device = simuliot.getSoundSensorDevice(device['DeviceID'], device['Name'], device['Location'], device['Type'])
                devicesCurrentSession.append(new_device)
            elif device['Type'] == 'Presence_Sensor':
                new_device = simuliot.getPresenceDevice(device['DeviceID'], device['Name'], device['Location'], device['Type'])
                devicesCurrentSession.append(new_device)
            elif device['Type'] == 'Sound_Sensor':
                new_device = simuliot.getSoundSensorDevice(device['DeviceID'], device['Name'], device['Location'], device['Type'])
                devicesCurrentSession.append(new_device)
            elif device['Type'] == 'Hub':
                new_device = simuliot.getHubDevice(device['DeviceID'], device['Name'], device['Location'], device['Type'])
                devicesCurrentSession.append(new_device)
            else:
                return jsonify({"error": "Invalid device type"}), 404
    else:
        return jsonify({"error": "Session already started. Please clear the session before adding new devices"}), 400
    return jsonify({"sucess":'Devices added to session. Awaiting save operation'}), 201

@app.route('/store-session', methods=['GET'])
def store_session():
    ## Check if the table DevicesSession exists. If not, create it
    try:
        conn = simuliot.connect_db()
        if conn is not None:
            cur = conn.cursor()
            
            ## Drop the table if it exists
            cur.execute("DROP TABLE IF EXISTS CURRENTDEVICESESSION")
            cur.execute("CREATE TABLE IF NOT EXISTS CURRENTDEVICESESSION (id TEXT PRIMARY KEY, name TEXT, type TEXT, location TEXT, value REAL)")

        ## Store the current session in the database. The current session is stored in the devicesCurrentSession list
            for device in devicesCurrentSession:
                sqlstring = "INSERT INTO CURRENTDEVICESESSION (id, name, type, location, value) VALUES ('{}', '{}', '{}', '{}', {})".format(str(device.UUID), str(device.deviceName), str(device.type), str(device.location), float(device.reading()["value"]))
                print (sqlstring)
                cur.execute(sqlstring)
            conn.commit()
            cur.close()
            conn.close()
    except Exception as e:
        simuliot.logger.critical('SQL Error: ' + str(e))
        return "A database error has occured.", 500

    return "Session has been stored.", 201

@app.route('/retrieve-session', methods=['GET'])
def retrieve_session():
    deviceSessionJSON = []
    try:
        for device in devicesCurrentSession:
            deviceSessionJSON.append({
                "id": device.UUID,
                "name": device.deviceName,
                "type": device.type,
                "location": device.location,
                "value": device.reading()["value"]
            }) ## Add device information to the list
        return jsonify(deviceSessionJSON), 200
    except Exception as e:
        simuliot.logger.critical('Session Retrieval Error: ' + str(e))
        return "An error has ocurred obtaining current session", 500

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
    ## Start the thread after sending http response
    global device_thread_pid 
    if device_thread_pid is not None:
        return "Session already started", 400
    device_thread_pid = os.fork()
    print(device_thread_pid)
    if device_thread_pid == 0:
        # Child process
        device_thread = Thread(target = simuliot.start, args = (devicesCurrentSession,))
        device_thread.start()
    else:
        # Parent process
        return "Session has been started", 200

@app.route('/kill-session',  methods=['GET'])
def kill_session():
    global device_thread_pid
    if device_thread_pid is None:
        return "No session to kill", 404
    simuliot.logger.info('Killing session {}'.format(device_thread_pid))
    if device_thread_pid != 0:
        pthread_kill(device_thread_pid, SIGINT)
        device_thread_pid = None
        devicesCurrentSession.clear()
        return "Session has been killed", 200

if __name__ == "__main__":
    app.run('127.0.0.1', 8088, debug=True)