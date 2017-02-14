# platform = Red Hat Enterprise Linux 6
INCLUDE_SHARED_REMEDIATION_FUNCTIONS
populate var_accounts_user_umask

grep -q umask /etc/csh.cshrc && \
  sed -i "s/umask.*/umask $var_accounts_user_umask/g" /etc/csh.cshrc
if ! [ $? -eq 0 ]; then
    echo "umask $var_accounts_user_umask" >> /etc/csh.cshrc
fi
