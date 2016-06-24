#!/usr/bin/python3

import time
import subprocess
import os

applicant_id = "sdfhdsfjdhfjhkadf"
max_num = 5

nmap_dir='/home/null/SecTools/nmap-7.12/nmap'
ISO_TIME_FORMAT = '%Y-%m-%d%H:%M:%S'

def run(cmd_string):
    nmap_result_filename = 'nmap_' + time.strftime(ISO_TIME_FORMAT, time.localtime())+'.xml'
    nmapcmd = nmap_dir+ cmd_string + ' -oX='+nmap_result_filename
    subprocess.call(nmapcmd,shell=True)
    f = open(nmap_result_filename, 'r')
    content= f.read()
    f.close()
    return content
