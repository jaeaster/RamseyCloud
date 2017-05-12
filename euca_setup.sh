#!/bin/bash

# ssh -i ~/.ssh/joinify centos@$HOSTNAME

# euca-run-instances emi-d62c30c1 -n 38 -k joinify -t m1.medium
# euca-authorize default -p22 -s 0.0.0.0/0
USERNAME="centos"
PYTHON="/home/centos/client/Main.py"
START="nohup ${PYTHON} > /dev/null 2>&1 &"
SSH_STRING="-i ~/.ssh/joinify -o StrictHostKeyChecking=no"
ARISTOTLE_IDS=`euca-describe-instances --region=aristotle-ucsb | grep INSTANCE | cut -f 2`

for ID in ${ARISTOTLE_IDS} ; do
  HOSTNAME=`euca-describe-instances  | grep $ID  | cut -f 4`
  if [ $1 == "kill" ]; then
    ssh $SSH_STRING -l ${USERNAME} ${HOSTNAME} "ps -C python -o pid= | xargs kill"
  else
    # scp -r $SSH_STRING client $USERNAME@$HOSTNAME:~
    ssh $SSH_STRING -l ${USERNAME} ${HOSTNAME} "${START}"
  fi
done

ECI_IDS=`euca-describe-instances --region=eci | grep INSTANCE | cut -f 2`

for ID in ${ECI_IDS} ; do
  HOSTNAME=`euca-describe-instances  | grep $ID  | cut -f 4`
  if [ $1 == "kill" ]; then
    ssh $SSH_STRING -l ${USERNAME} ${HOSTNAME} "ps -C python -o pid= | xargs kill"
  else
    # scp -r $SSH_STRING client $USERNAME@$HOSTNAME:~
    ssh $SSH_STRING -l ${USERNAME} ${HOSTNAME} "${START}"
  fi
done