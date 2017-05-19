#!/bin/bash

# ssh -i ~/.ssh/joinify centos@169.231.235.28
# ssh -i ~/.ssh/joinify centos@$HOSTNAME

# BASE IMAGE = emi-d62c30c1
# server_v1 = emi-0371d977
# euca-create-image i-ef945dd0 -n server-v1 --no-reboot

# docker run --publish 33957:33957 --name gossip_server --rm jeasterman/gossip_main &
# docker run --publish 57339:57339 --name ramsey_server --rm jeasterman/ramsey_main &
# euca-run-instances emi-0371d977 -n 6 -k joinify -t m3.2xlarge
# euca-authorize default -p22 -s 0.0.0.0/0
# euca-authorize default -p33957 -s 0.0.0.0/0
# euca-authorize default -p57339 -s 0.0.0.0/0
GOSSIP=`euca-describe-instances --filter "tag-value=gossip" | grep INSTANCE | cut -f 2`
GOSSIP_IPS=`euca-describe-instances --filter "tag-value=gossip" | grep INSTANCE | cut -d \t -f 9 | cut -f 2`
# euca-create-tags  i-f9e667aa i-f8110a2d i-ce358a60 --tag server=gossip
RAMSEY=`euca-describe-instances --filter "tag-value=ramsey" | grep INSTANCE | cut -f 2`
RAMSEY_IPS=`euca-describe-instances --filter "tag-value=ramsey" | grep INSTANCE | cut -d \t -f 9 | cut -f 2`
# euca-create-tags  i-b277624e i-561664c3 i-74d61083 --tag server=ramsey

USERNAME="centos"
PYTHON="/home/centos/client/Main.py"
START="nohup ${PYTHON} > /dev/null 2>&1 &"
SSH_STRING="-i ~/.ssh/joinify -o StrictHostKeyChecking=no"
ARISTOTLE_IDS=`euca-describe-instances --region=aristotle-ucsb | grep INSTANCE | cut -f 2`

# for ID in ${ARISTOTLE_IDS} ; do
#  euca-terminate-instances $ID
# done

for IP in ${GOSSIP_IPS} ; do
  echo ${IP}
  ssh $SSH_STRING -l ${USERNAME} ${IP} "sudo nohup docker run --publish 33957:33957 --name gossip_server jeasterman/gossip_main &"
done

# for ID in ${ARISTOTLE_IDS} ; do
#   HOSTNAME=`euca-describe-instances  | grep $ID  | cut -f 4`
#   if [ $1 == "kill" ]; then
#     ssh $SSH_STRING -l ${USERNAME} ${HOSTNAME} "ps -C python -o pid= | xargs kill"
#   else
#     # scp -r $SSH_STRING client $USERNAME@$HOSTNAME:~
#     ssh $SSH_STRING -l ${USERNAME} ${HOSTNAME} "${START}"
#   fi
# done

# ECI_IDS=`euca-describe-instances --region=eci | grep INSTANCE | cut -f 2`

# for ID in ${ECI_IDS} ; do
#   HOSTNAME=`euca-describe-instances  | grep $ID  | cut -f 4`
#   if [ $1 == "kill" ]; then
#     ssh $SSH_STRING -l ${USERNAME} ${HOSTNAME} "ps -C python -o pid= | xargs kill"
#   else
#     # scp -r $SSH_STRING client $USERNAME@$HOSTNAME:~
#     ssh $SSH_STRING -l ${USERNAME} ${HOSTNAME} "${START}"
#   fi
# done