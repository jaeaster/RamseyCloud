#!/bin/bash
USERNAME="jdogg5566"
HOSTS="linux01.engr.ucsb.edu \
linux02.engr.ucsb.edu \
linux03.engr.ucsb.edu \
linux04.engr.ucsb.edu \
linux05.engr.ucsb.edu \
linux06.engr.ucsb.edu \
linux07.engr.ucsb.edu \
linux08.engr.ucsb.edu \
linux09.engr.ucsb.edu \
linux10.engr.ucsb.edu \
linux11.engr.ucsb.edu \
linux12.engr.ucsb.edu \
linux13.engr.ucsb.edu \
linux14.engr.ucsb.edu \
linux15.engr.ucsb.edu \
linux16.engr.ucsb.edu \
linux17.engr.ucsb.edu \
linux18.engr.ucsb.edu \
linux19.engr.ucsb.edu \
linux20.engr.ucsb.edu \
linux21.engr.ucsb.edu \
linux22.engr.ucsb.edu \
linux23.engr.ucsb.edu \
linux24.engr.ucsb.edu \
linux25.engr.ucsb.edu \
linux26.engr.ucsb.edu \
linux27.engr.ucsb.edu \
linux28.engr.ucsb.edu"

PYTHON="python3 /cs/student/jdogg5566/go/src/github.com/EasterAndJay/cloud/matrix.py"

START="nohup ${PYTHON} > /dev/null 2>&1 &"

for HOSTNAME in ${HOSTS} ; do
    if [ $1 == "kill" ]; then
      ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "ps -C python3 -o pid= | xargs kill"
    else
      ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "${START}"
    fi
done