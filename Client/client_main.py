#!/usr/bin/python3

import os
import socket
import json
import base64

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9996

def loop_load_plugins():
    while True:
        for filename in os.listdir("plugins"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            clientPluginName = os.path.splitext(filename)[0]
            clientPlugin = __import__("plugins." + clientPluginName, fromlist=[clientPluginName])
            send_content = [{'oper_type': "REQUEST", 'applicant_id': clientPlugin.applicant_id, 'plugin_name': clientPluginName,
                            'max_num': clientPlugin.max_num}]
            try:
                socket_result = send(send_content)
                content_list = json.loads(socket_result)
                run_plugins(clientPlugin, clientPluginName, content_list)
            except Exception as err:
                print(err)


def send(send_content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))
    s.sendall(json.dumps(send_content).encode('utf-8'))

    socket_result = s.recv(1024*100).decode('utf-8')
    s.close()
    return socket_result

def run_plugins(clientPlugin, clientPluginName, content_list):
    send_content = []
    for str in content_list:
        result = clientPlugin.run(str["cmd_string"])
        if not(result):
            result = ""
        send_content.append({'oper_type': "RESPONSE", 'uuid': str["uuid"], 'result': result, 'applicant_id': clientPlugin.applicant_id, 'plugin_name': clientPluginName})
    send(send_content)




if __name__ == '__main__':
    loop_load_plugins()
