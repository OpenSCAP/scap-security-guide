# platform =  Webmin

# Include source function library.
. /usr/share/scap-security-guide/remediation_functions

WEBMIN_CONFIG_FILE="/etc/webmin/miniserv.conf"
replace_or_append "$WEBMIN_CONFIG_FILE" '^passwd_mode' '2' '@CCENUM@' '%s=%s'
