# coding: utf-8

####Created by Yannick MARTIN - yannickim@hotmail.com
####Last Modification : 07/04/2020


###RollBckTrain module who contains roll_users et roll_hstnme functions###

import requests
import json
import os
import socket
import boto3

##Specify the webhook uRL
web_hook_url = '<MYWEBHOOK URL>'

##Get the hostname and the IP of the targeted computer
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)

##The different messages sent to the slack channel
slack_msg_roll_users_sav = {'text':"Admininfra and Student personal folders from the workstation " + hostname + " IP " + IPAddr  + " saved "}
slack_msg_roll_users_del = {'text':"Admininfra and Student accounts and personal folders removed from the workstation " + hostname + " IP " + IPAddr}
slack_msg_roll_users_ko = {'text':"Admininfra and Student accounts and personal folders for the workstation " + hostname + " IP " + IPAddr + " not found"}
slack_msg_roll_hstnme = {'text':"Original hostname for the workstation " + hostname + " IP " + IPAddr + " restored"}
slack_msg_roll_hstnme_ko = {'text':"Hostname rollback files for the workstation " + hostname + " IP " + IPAddr + " not found or unusable"}
slack_msg_reboot = {'text':"The workstation at IP address " + IPAddr + " will reboot now "}

##Specify the hosts-old, hostname-old, student and admininfra files path
hst_path = "/home/hosts-old"
hstnme_path = "/home/hostname-old"
std_path = "/home/student"
adminf_path = "/home/admininfra"


##S3 configuration
s3_resource = boto3.resource("s3", region_name="eu-west-3")

##Save of personnal folders functions
print ("Saving personal folders")
os.system('tar -cjf /home/student/save/persosave.tar.gz /home/student/perso')
new_file_name = hostname + "-"
os.rename("/home/student/save/persosave.tar.gz","/home/student/save/" + new_file_name + "-PersoStdSave.tar.gz")

def save_std_folder() :
    if os.path.exists(std_path) :
        bucket_name = "myenterpriselan"
        std_file_path = '/home/student/save'
        my_bucket = s3_resource.Bucket(bucket_name)
        for path, subdirs, files in os.walk(std_file_path):
            path = path.replace("\\","/")
            directory_name = path.replace(std_file_path,"Personnal Save")
            for file in files:
                my_bucket.upload_file(os.path.join(path, file), directory_name+'/'+file)
    else :
        print ("Personal folder for Student account not found")
        requests.post(web_hook_url,data=json.dumps(slack_msg_roll_users_ko))

save_std_folder()

os.system('tar -cjf /home/admininfra/save/persosave.tar.gz /home/admininfra/perso')
new_file_name = hostname + "-"
os.rename("/home/admininfra/save/persosave.tar.gz","/home/admininfra/save/" + new_file_name + "-PersoAdmSave.tar.gz")

def save_adm_folder() :
    if os.path.exists(adminf_path) :
        bucket_name = "myenterpriselan"
        adm_file_path = '/home/admininfra/perso'
        my_bucket = s3_resource.Bucket(bucket_name)
        for path, subdirs, files in os.walk(adm_file_path):
            path = path.replace("\\","/")
            directory_name = path.replace(adm_file_path,"Personnal Save")
            for file in files:
                my_bucket.upload_file(os.path.join(path, file), directory_name+'/'+file)
    else :
        print ("Personal folder for Admininfra account not found")
        requests.post(web_hook_url,data=json.dumps(slack_msg_roll_users_ko))

save_adm_folder()                

##Roll_users function, delete admininfra and student users
def roll_users() :
    if os.path.exists(std_path) or os.path.exists(adminf_path) :
        print ("Deleting Admininfra and Student accounts and personal folders")
        os.system('sudo deluser admininfra')
        os.system('sudo rm -r /home/admininfra')
        os.system('sudo deluser student')
        os.system('sudo rm -r /home/student')
        requests.post(web_hook_url,data=json.dumps(slack_msg_roll_users_del))
    else :
        print ("Admininfra and Student accounts and personal folders not found")
        requests.post(web_hook_url,data=json.dumps(slack_msg_roll_users_ko))

roll_users()

##Roll_hstnme function, restore the original hostname of the computer
def roll_hstnme() :
    if os.path.exists(hst_path) and os.path.exists(hstnme_path) :
        print ("Starting hostname rollback")
        os.system('sudo mv /home/hosts-old /etc/hosts')
        os.system('sudo mv /home/hostname-old /etc/hostname')
        requests.post(web_hook_url,data=json.dumps(slack_msg_roll_hstnme))
    else :
        print ("Files for hostname rollback not found or unusable")
        requests.post(web_hook_url,data=json.dumps(slack_msg_roll_hstnme_ko))

roll_hstnme()
 
print ("The workstation will reboot now for applying changes")
requests.post(web_hook_url,data=json.dumps(slack_msg_reboot))
os.system('reboot')

exit()
