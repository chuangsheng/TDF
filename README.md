# TDF
__TDF is :Tools Distributed Framework__ (Based python3)

TDF used scene example:  
    You whant use nmap scan some IP and port(192.168.0.1-192.168.0.255,port 21-65535), if only one computer install a nmap,  target firewall must have alarms.
    If used some computer install more nmap, scan wide range target, you can do it.  
    __TDF can help you achieve your job.__
    TDF is a C/S program, based python version 3. next, shows you TDF work flow:   
    1. Based on __Nmap__ examples write your plugins, plugins classified into __server__ and __client__.  
    2. Server program read server plugins(Now,only support one server plugins), generated some __command string__, put __job task__.   
    3. Client program loop run read plugins, client plugins send info to server __get command string__.   
    4. Server program when client program get command string, set command string status(client id, start time...)   
    5. Client send command string to local plugins, plugins run it and send result to server.   
    6. Client continue load local plugins, get server task job,until the command string(with current plugins) status all finish(end time have value)   
    7. Server program every time check plugins status when get client program result, if __current plugins__ status is finish, send signal to plugins
    8. Server plugins get finish signal, to do something to closure.   __Welcome to perfect TDF with me!__
