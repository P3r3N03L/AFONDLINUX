# AFONDLINUX
LINUX TRAINING

This repository host the python files for the Linux training of AFONDLINUX organization.

These files will allow administrators to launch automated workstation preparation scripts, including :

- update/upgrade OS
- creation of specific users
- change of the hostname
- roll back with a save of the personnal folders to an AWS S3 bucket 

The scripts will also send notifications at each step to the slack channel of Myenterprise.

Prerequisites :

- Ubuntu 18.04
- AWS client 1.14.44
- Boto3
- Python 3.6.9
- Credentials for AWS S3 and Slack

