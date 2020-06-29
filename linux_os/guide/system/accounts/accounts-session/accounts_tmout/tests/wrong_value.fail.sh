#!/bin/bash
#
# profiles = xccdf_org.ssgproject.content_profile_ospp

if grep -q "^TMOUT" /etc/profile.d/tmout.sh; then
	sed -i "s/^TMOUT.*/TMOUT=3600/" /etc/profile.d/tmout.sh
else
	echo "TMOUT=3600" >> /etc/profile.d/tmout.sh
fi
