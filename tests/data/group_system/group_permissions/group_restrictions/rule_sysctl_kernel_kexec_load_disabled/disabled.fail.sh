#!/bin/bash
#
# profiles = xccdf_org.ssgproject.content_profile_ospp

. ../sysctl.sh

sysctl_set_kernel_setting_to kexec_load_disabled 0
