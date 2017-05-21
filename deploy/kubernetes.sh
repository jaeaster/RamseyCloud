#!/bin/bash

# See https://kubernetes.io/docs/getting-started-guides/kubeadm/
# For kubeadm reference

# kube-base = emi-e7a11618
MASTER="169.231.235.73"

CLIENTS="169.231.235.174 \
169.231.235.98 \
169.231.235.156 \
169.231.235.121"

KUBE_CMD="sudo kubeadm join --token 0aac58.d93c22380864aac6 10.1.2.183:6443 --skip-preflight-checks"

sudo su -
kubeadm init
exit
sudo cp /etc/kubernetes/admin.conf $HOME/
sudo chown $(id -u):$(id -g) $HOME/admin.conf
export KUBECONFIG=$HOME/admin.conf
# Install Romana CNI networking addon
kubectl apply -f https://raw.githubusercontent.com/romana/romana/master/containerize/specs/romana-kubeadm.yml

for CLIENT in ${CLIENTS} ; do
 ssh -tt $SSH_STRING -l ${USERNAME} ${CLIENT} ${KUBE_CMD}
done