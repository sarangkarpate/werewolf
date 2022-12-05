#!/bin/bash
export FOLDER=/var/werewolf

if [ -d $FOLDER ]
then
 rm -rf $FOLDER
fi

mkdir -p $FOLDER

# if this is a clean installation, the line below exits with code 1
# exit 0 allows the script to be seen as successful by the caller during deployment
pkill -f role_assignment.py
exit 0
