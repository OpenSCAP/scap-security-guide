# platform = Red Hat Enterprise Linux 5
cut -d: -f6 /etc/passwd | sort -u | xargs setfacl --remove-all 2>/dev/null