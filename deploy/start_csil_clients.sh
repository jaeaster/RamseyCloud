#!/bin/bash

USERNAME="jdogg5566"
HOSTS=`cat hosts.txt`

PYTHON="/cs/student/jdogg5566/go/src/github.com/EasterAndJay/cloud/client/Main.py"

START="nohup ${PYTHON} > /dev/null 2>&1 &"

for HOSTNAME in ${HOSTS} ; do
    if [ $1 == "kill" ]; then
      ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "ps -C python -o pid= | xargs kill"
    else
      ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "${START}"
    fi
done
