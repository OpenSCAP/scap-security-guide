# platform = multi_platform_rhel

# Include source function library.
INCLUDE_SHARED_REMEDIATION_FUNCTIONS

replace_or_append '/etc/ssh/sshd_config' '^KerberosAuthentication' 'no' '$CCENUM' '%s %s'
