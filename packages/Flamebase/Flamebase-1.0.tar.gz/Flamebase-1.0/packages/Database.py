from flask import Flask, request, jsonify
import ngrok
import json

def run():
    #token = "2JOz7AoXkzAYvacIHpCYQRayKU3_4byKqjLzCg8bS2iDni1Ya"
    token = open("token.txt", "r").read()
    port = open("port.txt", "r").read()
    tunnel = ngrok.connect(port, authtoken=token)
    print(tunnel.url()," port:",port)

app = Flask(__name__)
database = {}  # In-memory data storage, replace with your preferred database management system

class Database:
    def __init__(self):
        self.file_path = 'database.json'  # JSON file path

    def reference(self, path):
        return self._get_data(path)

    def _get_data(self, path):
        keys = path.split('/')
        data = database
        for key in keys:
            if key in data:
                data = data[key]
            else:
                return None
        return data

    def create_directory(self, path):
        keys = path.split('/')
        parent = database
        for key in keys:
            if key not in parent:
                parent[key] = {}
            parent = parent[key]
        self._save_to_json()  # Save data to JSON file
        return {'message': 'Directory created successfully'}

    def get_entire_database(self):
        return database

    def create_data(self, path, name, value):
        parent = self.reference(path)
        if parent is not None and isinstance(parent, dict):
            parent[name] = value
            self._save_to_json()  # Save data to JSON file
            return {'message': 'Data created successfully'}
        else:
            return {'error': 'Path not found or not a directory'}

    def _save_to_json(self):
        with open(self.file_path, 'w') as file:
            json.dump(database, file)

db = Database()

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(database)

@app.route('/data', methods=['POST'])
def create_directory():
    path = request.get_json().get('path')
    if path is not None:
        return jsonify(db.create_directory(path))
    else:
        return jsonify({'error': 'No path provided'})

@app.route('/data/<path:path>', methods=['GET'])
def get_data_by_path(path):
    if path == '/':
        return jsonify(db.get_entire_database())

@app.route('/data/<path:path>', methods=['POST'])
def create_data(path):
    data = request.get_json()
    if isinstance(data, dict):
        parent = db.reference(path)
        if parent is not None and isinstance(parent, dict):
            for name, value in data.items():
                parent[name] = value
            db._save_to_json()  # Save data to JSON file
            return jsonify({'message': 'Data created successfully'})
        else:
            return jsonify({'error': 'Path not found or not a directory'})
    else:
        return jsonify({'error': 'Invalid data format'})

@app.route('/data/<path:path>', methods=['PUT'])
def update_data(path):
    data = request.get_json()
    existing_data = db.reference(path)
    if existing_data is not None:
        keys = path.split('/')
        parent = database
        for key in keys[:-1]:
            parent = parent[key]
        parent[keys[-1]] = data
        db._save_to_json()  # Save data to JSON file
        return jsonify({'message': 'Data updated successfully'})
    else:
        return jsonify({'error': 'Path not found'})

@app.route('/data/<path:path>', methods=['DELETE'])
def delete_data(path):
    existing_data = db.reference(path)
    if existing_data is not None:
        keys = path.split('/')
        parent = database
        for key in keys[:-1]:
            parent = parent[key]
        del parent[keys[-1]]
        db._save_to_json()  # Save data to JSON file
        return jsonify({'message': 'Data deleted successfully'})
    else:
        return jsonify({'error': 'Path not found'})

if __name__ == '__main__':
    app.run()