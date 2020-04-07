# coding: utf-8

####Created by Yannick MARTIN - yannickim@hotmail.com
####Last Modification : 07/04/2020


###This is the PrepTrain module who contains chkupdate, upgrade, cr_users et chge_hstnme functions

import requests
import json
import os
import socket
import random


##Specify the upd.text and users path
upd_path = "/tmp/upd.txt"
std_path = "/home/student"
adminf_path = "/home/admininfra"

##The webhook URL for Slack
web_hook_url = '<MYWEBHOOK URL>'

##Get the hostname and the IP of the targeted computer
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)

##The different messages send to the slack channel
slack_msg_no_upd = {'text':"No update available for the workstation " + hostname + " IP " + IPAddr}
slack_msg_upg_ok = {'text':"Upgrade done for the workstation " + hostname + " IP " + IPAddr}
slack_msg_no_upd_file = {'text':"Error, upd.txt files for the workstation " + hostname + " IP " + IPAddr + " not found"}
slack_msg_cr_users = {'text':"Admininfra and Student accounts for the workstation " + hostname + " IP " + IPAddr + " created and configured"}
slack_msg_cr_users_ko = {'text':"Admininfra and Student accounts already set for the workstation " + hostname + " IP " + IPAddr}
slack_msg_chge_hstnme = {'text':"Hostname changed for the workstation at IP address " + IPAddr}
slack_msg_reboot = {'text':"The workstation at IP address " + IPAddr + " will reboot now "}

##Chkupdate function, check if updates are vailable and create the upd.txt report file
def chkupdate() :
	os.system("sudo apt-get -s --no-download --fix-missing dist-upgrade -V | grep '=>' | awk '{print$1}' >> /tmp/upd.txt")

chkupdate()

##Upgrade function, make the upgrade if the upd.txt exist and is larger than 0
def upgrade() :
    if os.path.exists(upd_path) and os.path.getsize(upd_path) > 0 :
        print ("Updates available, starting upgrade now")
        os.system('sudo apt-get -y upgrade')
        requests.post(web_hook_url,data=json.dumps(slack_msg_upg_ok))
    elif os.path.exists(upd_path) and os.path.getsize(upd_path) == 0:
        print ("No updates available")
        requests.post(web_hook_url,data=json.dumps(slack_msg_no_upd))
    else :
        print ("Error, upd.txt file not found")
        requests.post(web_hook_url,data=json.dumps(slack_msg_no_upd_file))

upgrade()

##Creation of users function, create admininfra and student credentials and folders
def cr_users() :
    if os.path.exists(std_path) and os.path.exists(adminf_path) :
        print ("Users already set")
        requests.post(web_hook_url,data=json.dumps(slack_msg_cr_users_ko))
    else :    
        print ("Creation of the Admininfra user and repository")
        os.system('sudo useradd -m -p $(openssl passwd -1 sprvsr) admininfra')
        os.system('sudo usermod -a -G sudo admininfra')
        os.system('sudo mkdir /home/admininfra/perso')
        os.system('sudo mkdir /home/admininfra/save')
        print ("Creation of the Student user and repository")
        os.system('sudo useradd -m -p $(openssl passwd -1 aflstud) student')
        os.system('sudo mkdir /home/student/perso')
        os.system('sudo mkdir /home/student/save')
        requests.post(web_hook_url,data=json.dumps(slack_msg_cr_users))

cr_users()

##Change hostname function
def chge_hstnme() :
    print ("Saving hostname files")
    os.system('sudo cp /etc/hosts /home/hosts-old')
    os.system('sudo cp /etc/hostname /home/hostname-old')
    print ("Changing hostname")
    num = str(random.randint(1,100))
    prefix = ("AFL1DSK")
    new_hostname = (prefix + num)
    os.system('sudo hostnamectl set-hostname' + " " + new_hostname)
    os.system('$hostname')
    requests.post(web_hook_url,data=json.dumps(slack_msg_chge_hstnme))

chge_hstnme()

print ("The workstation will reboot now for applying changes")
requests.post(web_hook_url,data=json.dumps(slack_msg_reboot))
os.system('reboot')

exit()

