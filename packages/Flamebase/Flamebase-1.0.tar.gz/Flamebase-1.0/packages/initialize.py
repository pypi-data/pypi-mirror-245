import json

def init_app(data):
    jdata = json.loads(data)
    open("token.txt", "w").write(str(jdata['auth_token']))
    open("port.txt", "w").write(str(jdata['db_port']))
    open("ngrok_api_key.txt", "w").write(str(jdata['api_key']))