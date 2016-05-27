# platform = SUSE Enterprise 12
# CAUTION: This remediation script will remove portreserve
#	   from the system, and may remove any packages
#	   that depend on portreserve. Execute this
#	   remediation AFTER testing on a non-production
#	   system!

# Include source function library.
. /usr/share/scap-security-guide/remediation_functions

package_command remove portreserve
