#!/bin/bash
SSHD_CONFIG="/etc/ssh/sshd_config"

if grep -q "^LoginGraceTime" $SSHD_CONFIG; then
	sed -i "s/^LoginGraceTime.*/LoginGraceTime 30/" $SSHD_CONFIG
else
	echo "LoginGraceTime 30" >> $SSHD_CONFIG
fi