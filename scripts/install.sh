#!/bin/bash
yum install -y python38 python38-pip python38-devel python-devel \
 openssl-devel libffi-devel gcc
cd /var/werewolf
python3 -m pip install -r requirements.txt
source /var/token.sh
sed -i "s/<PlaceHolder>/$TOKEN/g" config.json