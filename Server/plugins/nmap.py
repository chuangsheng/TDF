from taskModule import TaskModule
import ipaddress


def init_task_list():
    TASK_LIST = []
    PLUGINS_NAME = "nmap"

    port_tuple = ('80','8080')

    '''
    target_ip = ipaddress.ip_network('192.168.14.0/24').hosts()
    for port in port_tuple:
        for ip in target_ip:
            CMD_STRING = " -sV -O -Pn -p" + port + " " + str(ip)
            TASK_LIST.append(TaskModule(PLUGINS_NAME, CMD_STRING))
    '''
    
    for port in port_tuple:
        CMD_STRING =  " -sV -O -Pn -p" + port + " 192.168.0.1"
        TASK_LIST.append(TaskModule(PLUGINS_NAME, CMD_STRING))

    return TASK_LIST


def handle_response(task_module):
    f = open("nmap.xml", 'a')
    f.write(task_module.result + "\n")
    f.close()


def completed_signal(plugin_name):
    f = open("nmap.xml", 'a')
    f.write(plugin_name+" is done" + "\n")
    f.close()
