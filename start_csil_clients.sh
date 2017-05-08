#!/bin/bash

USERNAME="jdogg5566"
HOSTS="csil-01.cs.ucsb.edu \
csil-02.cs.ucsb.edu \
csil-03.cs.ucsb.edu \
csil-04.cs.ucsb.edu \
csil-05.cs.ucsb.edu \
csil-06.cs.ucsb.edu \
csil-07.cs.ucsb.edu \
csil-08.cs.ucsb.edu \
csil-09.cs.ucsb.edu \
csil-10.cs.ucsb.edu \
csil-11.cs.ucsb.edu \
csil-12.cs.ucsb.edu \
csil-13.cs.ucsb.edu \
csil-14.cs.ucsb.edu \
csil-15.cs.ucsb.edu \
csil-16.cs.ucsb.edu \
csil-17.cs.ucsb.edu \
csil-18.cs.ucsb.edu \
csil-19.cs.ucsb.edu \
csil-20.cs.ucsb.edu \
csil-21.cs.ucsb.edu \
csil-22.cs.ucsb.edu \
csil-23.cs.ucsb.edu \
csil-24.cs.ucsb.edu \
csil-25.cs.ucsb.edu \
csil-26.cs.ucsb.edu \
csil-27.cs.ucsb.edu \
csil-28.cs.ucsb.edu \
csil-29.cs.ucsb.edu \
csil-30.cs.ucsb.edu \
csil-31.cs.ucsb.edu \
csil-32.cs.ucsb.edu \
csil-33.cs.ucsb.edu \
csil-34.cs.ucsb.edu \
csil-36.cs.ucsb.edu \
csil-37.cs.ucsb.edu \
csil-38.cs.ucsb.edu \
csil-39.cs.ucsb.edu \
csil-40.cs.ucsb.edu \
csil-41.cs.ucsb.edu \
csil-42.cs.ucsb.edu \
csil-43.cs.ucsb.edu \
csil-44.cs.ucsb.edu \
csil-45.cs.ucsb.edu \
csil-46.cs.ucsb.edu \
csil-47.cs.ucsb.edu \
csil-48.cs.ucsb.edu \
linux01.engr.ucsb.edu \
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

PYTHON="/cs/student/jdogg5566/go/src/github.com/EasterAndJay/cloud/the_matrix_evolution.py"

START="nohup ${PYTHON} > /dev/null 2>&1 &"

for HOSTNAME in ${HOSTS} ; do
    if [ $1 == "kill" ]; then
      ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "ps -C python -o pid= | xargs kill"
    else
      ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "${START}"
    fi
done
