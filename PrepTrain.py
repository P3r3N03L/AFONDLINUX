# coding: utf-8

###PrepTrain module who contains chkupdate, upgrade, cr_users et chge_hstnme functions###

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
web_hook_url = '<MYWEBHOOKURL>'

##Get the hostname and the IP of the targeted computer
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)

##The different messages send to the slack channel
slack_msg_no_upd = {'text':"Aucune mise à jour disponible pour le poste " + hostname + " IP " + IPAddr}
slack_msg_upg_ok = {'text':"Upgrade effectué pour le poste " + hostname + " IP " + IPAddr}
slack_msg_no_upd_file = {'text':"Erreur fichier upd.txt non trouvé pour le poste " + hostname + " IP " + IPAddr}
slack_msg_cr_users = {'text':"Comptes Admininfra et Student créés pour le poste " + hostname + " IP " + IPAddr}
slack_msg_cr_users_ko = {'text':"Comptes Admininfra et Student déjà présents le poste " + hostname + " IP " + IPAddr}
slack_msg_chge_hstnme = {'text':"Hostname changé pour le poste à l'addresse " + IPAddr}
slack_msg_reboot = {'text':"Le poste à l'addresse " + IPAddr + " va redémarrer "}

##Chkupdate function, check if updates are vailable and create the upd.txt report file
def chkupdate() :
	os.system("sudo apt-get -s --no-download --fix-missing dist-upgrade -V | grep '=>' | awk '{print$1}' >> /tmp/upd.txt")

chkupdate()

##Upgrade function, make the upgrade if the upd.txt exist and is larger than 0
def upgrade() :
    if os.path.exists(upd_path) and os.path.getsize(upd_path) > 0 :
        print ("Mises à jour disponibles, lancement de l'installation")
        os.system('sudo apt-get -y upgrade')
        requests.post(web_hook_url,data=json.dumps(slack_msg_upg_ok))
    elif os.path.exists(upd_path) and os.path.getsize(upd_path) == 0:
        print ("Aucune mise à jour en attente")
        requests.post(web_hook_url,data=json.dumps(slack_msg_no_upd))
    else :
        print ("Erreur : fichier upd.txt non trouvé")
        requests.post(web_hook_url,data=json.dumps(slack_msg_no_upd_file))

upgrade()

##Creation of users function, create admininfra and student credentials and folders
def cr_users() :
    if os.path.exists(std_path) and os.path.exists(adminf_path) :
        print ("Utilisateurs déjà présents")
        requests.post(web_hook_url,data=json.dumps(slack_msg_cr_users_ko))
    else :    
        print ("Création de l'utilisateur admininfra")
        os.system('sudo useradd -m -p $(openssl passwd -1 sprvsr) admininfra')
        os.system('sudo usermod -a -G sudo admininfra')
        os.system('sudo mkdir /home/admininfra/perso')
        os.system('sudo mkdir /home/admininfra/save')
        print ("Création de l'utilisateur Student")
        os.system('sudo useradd -m -p $(openssl passwd -1 aflstud) student')
        os.system('sudo mkdir /home/student/perso')
        os.system('sudo mkdir /home/student/save')
        requests.post(web_hook_url,data=json.dumps(slack_msg_cr_users))

cr_users()

##Change hostname function
def chge_hstnme() :
    print ("Sauvegarde du fichier host et du hostname")
    os.system('sudo cp /etc/hosts /home/hosts-old')
    os.system('sudo cp /etc/hostname /home/hostname-old')
    print ("changement du hostname")
    num = str(random.randint(1,100))
    prefix = ("AFL1DSK")
    new_hostname = (prefix + num)
    os.system('sudo hostnamectl set-hostname' + " " + new_hostname)
    os.system('$hostname')
    requests.post(web_hook_url,data=json.dumps(slack_msg_chge_hstnme))

chge_hstnme()

print ("Le poste va redémarrer pour appliquer les changements")
requests.post(web_hook_url,data=json.dumps(slack_msg_reboot))
os.system('reboot')

exit()

