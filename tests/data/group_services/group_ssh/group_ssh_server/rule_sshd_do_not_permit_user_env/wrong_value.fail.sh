#!/bin/bash
#
# profiles = xccdf_org.ssgproject.content_profile_ospp

if grep -q "^PermitUserEnvironment" /etc/ssh/sshd_config; then
	sed -i "s/^PermitUserEnvironment.*/PermitUserEnvironment yes/" /etc/ssh/sshd_config
else
	echo "PermitUserEnvironment yes" >> /etc/ssh/sshd_config
fi
