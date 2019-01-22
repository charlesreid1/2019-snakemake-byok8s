#!/bin/bash
#
# Install minikube
# 
# https://github.com/kubernetes/minikube

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
        && sudo install minikube-linux-amd64 /usr/local/bin/minikube
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install kubernetes-cli
    brew cask install minikube
 else
    echo "I pity the foo who use your operating system"
fi

