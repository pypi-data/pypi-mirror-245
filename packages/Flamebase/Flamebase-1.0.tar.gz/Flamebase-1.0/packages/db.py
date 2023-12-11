import requests
import json
import ngrok 
import Database

prebase_url = open("ngrok_tunnel.txt", "r").read()
base_url = str(prebase_url) + "/data"
path = ""
ref_path = ""

def run():
    Database.run()
    
def init():
    global base_url, prebase_url
    if open("ngrok_api_key.txt", "r").read() != "":
        api_key = open("ngrok_api_key.txt", "r").read()
    else:
        print("Database isn't initialized! Run: Flamebase.initialize.init_app(your data) to initialize it.")
        open("error.txt", "w").write("Database is not initialized!")
        return
    client = ngrok.Client(api_key)
    for t in client.tunnels.list():
        open("ngrok_tunnel.txt","w").write(str(t.public_url))
        open("error.txt", "w").write("")
        return
    print("Database is not online! Run: Flamebase.db.run() to start the database.")
    open("error.txt", "w").write("Database is not online!")
    return
        
def reference(key=None):
    global base_url
    if key == None:
        key = ""
    if open("error.txt", "r").read() != "":
        init()
    return Reference(key)

class Reference:
    def __init__(self,key):
        global path
        path = key

    def is_json_object(data):
        try:
            json_object = json.loads(data)
            if isinstance(json_object, dict):
                return True
            else:
                return False
        except ValueError:
            return False
       
    def set_dir(key):
        global path, ref_path
        payload = {'path': path}
        response = requests.post(base_url, json=payload)
        data = response.json()
        if ref_path != "":
            path = ref_path
    
    def get(key):
        global path, ref_path
        response = requests.get(base_url)
        data = response.json()
        if path != "":
            categories = path.split("/")
            for cat in categories:
                data = data.get(cat, {})
                if not data:
                    break
        formatted_data = json.dumps(data, indent=4)
        if ref_path != "":
            path = ref_path
        return formatted_data
    
    def set(key, value=None):
        global path, ref_path
        if value == None:
            Reference.set_dir("a")
            return
        elif Reference.is_json_object(value) == True:
            url = f'{base_url}/{path}'
            data = json.loads(value)
        else:
            path, name = path.rsplit("/", 1)
            url = f'{base_url}/{path}'
            data = {name: value}
        if url == f'{base_url}/':
            url = url[:-1]
        #headers = {"Content-Type": "application/json"}  # Set the Content-Type header
        response = requests.post(url, json=data)#, headers=headers)  # Use json parameter to send JSON data
        if ref_path != "":
            path = ref_path
            
    def delete(key):
        global path, ref_path
        url = f'{base_url}/{path}'
        response = requests.delete(url)
        if ref_path != "":
            path = ref_path
        
    def child(key, value):
        global ref_path, path
        ref_path = path
        key_path=path + "/" + value
        return Reference(key_path)