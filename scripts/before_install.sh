#!/bin/bash
export FOLDER=/var/werewolf

if [ -d $FOLDER ]
then
 rm -rf $FOLDER
fi

mkdir -p $FOLDER