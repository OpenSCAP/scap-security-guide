# platform = Red Hat Enterprise Linux 5
grep -i '^tls_cert' /etc/ldap.conf | grep -v "#" | awk '{ print $2 }' | xargs chown -R root