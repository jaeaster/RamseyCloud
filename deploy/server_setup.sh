

# ssh -i ~/.ssh/joinify centos@169.231.235.24
# ssh -i ~/.ssh/joinify centos@$HOSTNAME

# BASE IMAGE = emi-d62c30c1
# server_v1 = emi-0371d977
# kube-base = emi-e7a11618
# euca-create-image i-e4121f1e -n kube-base --no-reboot

# docker run --publish 33957:33957 --name gossip_server --rm jeasterman/gossip_main &
# docker run --publish 57339:57339 --name ramsey_server --rm jeasterman/ramsey_main &
# euca-run-instances emi-e7a11618 -n 4 -k joinify -t m3.2xlarge
# euca-authorize default -p22 -s 0.0.0.0/0
# euca-authorize default -p33957 -s 0.0.0.0/0
# euca-authorize default -p57339 -s 0.0.0.0/

GOSSIP=`euca-describe-instances --filter "tag-value=gossip" | grep INSTANCE | cut -f 2`
GOSSIP_IPS=`euca-describe-instances --filter "tag-value=gossip" | grep INSTANCE | cut -d \t -f 9 | cut -f 2`
GOSSIP_CMD="docker run -d --publish 33957:33957 \
--name gossip_server jeasterman/gossip_main"
# euca-create-tags  i-f9e667aa i-f8110a2d i-ce358a60 --tag server=gossip

RAMSEY=`euca-describe-instances --filter "tag-value=ramsey" | grep INSTANCE | cut -f 2`
RAMSEY_IPS=`euca-describe-instances --filter "tag-value=ramsey" | grep INSTANCE | cut -d \t -f 9 | cut -f 2`
RAMSEY_CMD="docker run -d --publish 57339:57339 \
--name ramsey_server jeasterman/ramsey_main"
# euca-create-tags  i-b277624e i-561664c3 i-74d61083 --tag server=ramsey

USERNAME="centos"
SSH_STRING="-i ~/.ssh/joinify -o StrictHostKeyChecking=no"
ARISTOTLE_IDS=`euca-describe-instances --region=aristotle-ucsb | grep INSTANCE | cut -f 2`

for CLIENT in ${CLIENTS} ; do
 ssh -tt $SSH_STRING -l ${USERNAME} ${CLIENT} ${KUBE_CMD}
done

# "sudo groupadd docker && \
# sudo gpasswd -a ${USERNAME} docker && \
# sudo service docker restart"

# for IP in ${GOSSIP_IPS} ; do
#   echo ${IP}
#   ssh -tt $SSH_STRING -l ${USERNAME} ${IP} ${GOSSIP_CMD}
# done

# for IP in ${RAMSEY_IPS} ; do
#   echo ${IP}
#   ssh -tt $SSH_STRING -l ${USERNAME} ${IP} ${RAMSEY_CMD}
# done