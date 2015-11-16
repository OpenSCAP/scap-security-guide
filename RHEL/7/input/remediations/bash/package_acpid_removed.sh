# platform = Red Hat Enterprise Linux 7
# CAUTION: This remediation script will remove acpid
#	   from the system, and may remove any packages
#	   that depend on acpid. Execute this
#	   remediation AFTER testing on a non-production
#	   system!

# Include source function library.
. /usr/share/scap-security-guide/remediation_functions

package_command remove acpid
