#
# Disable smartd.service for all systemd targets
#
systemctl disable smartd.service

#
# Stop smartd.service if currently running
#
systemctl stop smartd.service
