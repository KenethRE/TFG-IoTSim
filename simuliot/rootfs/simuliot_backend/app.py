from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from threading import Thread
from signal import pthread_kill, SIGINT

import simuliot
app = Flask(__name__)
sock = SocketIO(app, debug=True, cors_allowed_origins="*", async_mode='eventlet')

# Routes
# GET /devices

devices = []
devicesCurrentSession = []
device_thread = Thread(target = simuliot.start_session, args = (devicesCurrentSession,))
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
    device = next((device for device in devicesCurrentSession if device['id'] == device_id), None)
    if device:
        return jsonify(device)
    else:
        simuliot.logger.error('Device not found. id: ' + str(device_id))
        return jsonify({"error": "Device not found"}), 404

# POST /devices
@app.route('/devices', methods=['POST'])
def add_device():
    new_device = request.get_json()
    devicesCurrentSession.append(new_device)
    return jsonify(new_device), 201

@app.route('/store-session', methods=['GET'])
def store_session():
    ## Check if the table DevicesSession exists. If not, create it
    try:
        conn = simuliot.connect_db()
        if conn is not None:
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS CURRENTDEVICESESSION (id INTEGER PRIMARY KEY, name TEXT, type TEXT, location TEXT, value TEXT)")

        ## Store the current session in the database. The current session is stored in the devicesCurrentSession list
            for device in devicesCurrentSession:
                cur.execute("INSERT INTO DEVICES (id, name, type, location, value) VALUES (?, ?, ?, ?, ?)", (device['UUID'], device['name'], device['type'], device['location'], device['value']))
            conn.commit()
            cur.close()
            conn.close()
    except Exception as e:
        simuliot.logger.critical('SQL Error: ' + str(e))
        return "A database error has occured.", 500

    return "Session has been stored." + jsonify(devicesCurrentSession), 201

@app.route('/retrieve-session', methods=['GET'])
def retrieve_session():
    try:
        conn = simuliot.connect_db()
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM CURRENTDEVICESESSION")
            rows = cur.fetchall()
            for row in rows:
                device = {
                    "id": row[0],
                    "name": row[1],
                    "type": row[2],
                    "location": row[3],
                    "value": row[4]
                }
                devicesCurrentSession.append(device)
            cur.close()
            conn.close()
    except Exception as e:
        simuliot.logger.critical('SQL Error: ' + str(e))
        return "A database error has occured.", 500

    return jsonify(devicesCurrentSession), 200

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
    device_thread.start()
    device_thread.join()
    return "Session has been started", 200

@app.route('/kill-session',  methods=['GET'])
def kill_session():
    pthread_kill(device_thread.ident, SIGINT)
    return "Session has been killed", 200

## Start a websocket server to send MQTT to front
@sock.on('device_event')
def handle_device_event():
    # We obtain the data from MQTT
    
    simuliot.logger.debug('Sent data in websocket: ' + str(data))
    emit('device_event', data, broadcast=True)

if __name__ == "__main__":
    app.run('127.0.0.1', 8088, debug=True)