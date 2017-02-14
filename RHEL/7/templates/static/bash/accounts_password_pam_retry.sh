# platform = Red Hat Enterprise Linux 7
INCLUDE_SHARED_REMEDIATION_FUNCTIONS
populate var_password_pam_retry

if grep -q "retry=" /etc/pam.d/system-auth; then   
	sed -i --follow-symlinks "s/\(retry *= *\).*/\1$var_password_pam_retry/" /etc/pam.d/system-auth
else
	sed -i --follow-symlinks "/pam_pwquality.so/ s/$/ retry=$var_password_pam_retry/" /etc/pam.d/system-auth
fi
