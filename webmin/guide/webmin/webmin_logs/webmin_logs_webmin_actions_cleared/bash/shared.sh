# platform =  Webmin

# Include source function library.
. /usr/share/scap-security-guide/remediation_functions

WEBMIN_CONFIG_FILE="/etc/webmin/config"
replace_or_append "$WEBMIN_CONFIG_FILE" '^logclear' '0' '@CCENUM@' '%s=%s'
