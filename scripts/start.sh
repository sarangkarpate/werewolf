#!/bin/bash
cd /var/werewolf
nohup python3 role_assignment.py > log.out 2>&1 &