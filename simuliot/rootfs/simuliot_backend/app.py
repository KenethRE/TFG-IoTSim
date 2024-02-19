from flask import Flask, jsonify, request
import simuliot
app = Flask(__name__)

#Execute DB connection
conn = simuliot.connect_db()

devices = []

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

# Routes
# GET /devices
@app.route('/devices', methods=['GET'])
def get_devices():
    return jsonify(devices)

# GET /devices/<id>
@app.route('/devices/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in devices if book['id'] == book_id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

# POST /devices
@app.route('/devices', methods=['POST'])
def add_book():
    new_book = request.get_json()
    devices.append(new_book)
    return jsonify(new_book), 201

# PUT /devices/<id>
@app.route('/devices/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((book for book in devices if book['id'] == book_id), None)
    if book:
        book.update(request.get_json())
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

# DELETE /devices/<id>
@app.route('/devices/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = next((book for book in devices if book['id'] == book_id), None)
    if book:
        devices.remove(book)
        return jsonify({"message": "Book deleted"})
    else:
        return jsonify({"error": "Invalid request"})

if __name__ == "__main__":
    app.run('127.0.0.1', 8088, debug=True)