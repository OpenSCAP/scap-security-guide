# platform = Red Hat Enterprise Linux 5
/sbin/iptables -A INPUT -j REJECT --reject-with icmp-host-prohibited
/sbin/iptables-save > /etc/sysconfig/iptables