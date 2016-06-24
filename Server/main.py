#!/usr/bin/python3

import socket
import threading
import time
import json
import base64

from taskList import TaskList

lock = threading.Lock()

SERVER_PORT = 9996
LISTEN_NUM = 10
clientIPList = ['127.0.0.1', '192.168.0.10']

serverRun = True
ISO_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def receive(client_socket, clientAddr):
    
    try:
    
        clentContent_JSON = json.loads(client_socket.recv(1024*1000).decode('utf8'))

        if len(clentContent_JSON) > 0:
            oper_type = clentContent_JSON[0]["oper_type"]
            applicant_id = clentContent_JSON[0]["applicant_id"]
            plugin_name = clentContent_JSON[0]["plugin_name"]
            if oper_type == "REQUEST":
                max_num = clentContent_JSON[0]["max_num"]
                lock.acquire()
                try:
                    unAssignedTaskList = []
                    unAssignedTaskIndexList = task_list.getUnAssignedTaskIndex(plugin_name, max_num)

                    for index in unAssignedTaskIndexList:
                        taskmodule = task_list.allTaskList[index]
                        taskmodule.applicant_id = applicant_id
                        taskmodule.start_time = time.strftime(ISO_TIME_FORMAT, time.localtime())
                        task_list.modifyTask(index, taskmodule)
                        unAssignedTaskList.append(
                            {'uuid': taskmodule.uuid, 'cmd_string': taskmodule.cmd_string})

                    send(client_socket, unAssignedTaskList)

                finally:
                    lock.release()
            elif oper_type == "RESPONSE":
                for str_temp in clentContent_JSON:
                    uuid = str_temp["uuid"]
                    lock.acquire()
                    try:
                        index = task_list.getUnCompletedTaskIndexByUUID(uuid)
                        taskmodule = task_list.allTaskList[index]
                        taskmodule.end_time = time.strftime(ISO_TIME_FORMAT, time.localtime())
                        taskmodule.result = clentContent_JSON[0]["result"]
                        task_list.modifyTask(index, taskmodule)

                        task_list.handle_response(taskmodule)

                    finally:
                        lock.release()

                send(client_socket, [{'status': "OK"}])

                if (task_list.completedAllTask(clentContent_JSON[0]["plugin_name"])):
                    task_list.completed_signal(clentContent_JSON[0]["plugin_name"])

    except Exception as err:
        print(err)


def send(client_socket, result_list):
    client_socket.sendall(json.dumps(result_list).encode('utf-8'))


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', SERVER_PORT))
    server_socket.listen(LISTEN_NUM)
    print("Server Start Done.  listen in the port:"+str(SERVER_PORT) )
    while serverRun:
        (client_socket, client_addr) = server_socket.accept()
        if client_addr[0] in clientIPList:
            server_thread = threading.Thread(target=receive, args=(client_socket, client_addr))
            server_thread.daemon = True
            server_thread.start()

    server_socket.close()


if __name__ == '__main__':
    print("TDF Server starting......")
    task_list = TaskList()
    task_list.init_task_list()
    server()
