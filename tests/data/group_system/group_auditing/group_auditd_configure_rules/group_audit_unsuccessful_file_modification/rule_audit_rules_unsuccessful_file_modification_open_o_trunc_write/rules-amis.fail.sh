#!/bin/bash

# profiles = xccdf_org.ssgproject.content_profile_ospp

sed '3,4d' ../audit_open_o_trunc_write.rules > /etc/audit/rules.d/open-o_trunc_write.rules
