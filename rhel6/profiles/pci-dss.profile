documentation_complete: true

title: 'PCI-DSS v3 Control Baseline for Red Hat Enterprise Linux 6'

description: 'This is a *draft* profile for PCI-DSS v3.'

selections:
    - var_password_pam_unix_remember=4
    - var_account_disable_post_pw_expiration=90
    - var_accounts_passwords_pam_faillock_deny=6
    - var_accounts_passwords_pam_faillock_unlock_time=1800
    - sshd_idle_timeout_value=15_minutes
    - var_password_pam_minlen=7
    - var_password_pam_minclass=2
    - var_accounts_maximum_age_login_defs=90
    - service_auditd_enabled
    - grub_legacy_audit_argument
    - auditd_data_retention_num_logs
    - auditd_data_retention_max_log_file
    - auditd_data_retention_max_log_file_action
    - auditd_data_retention_space_left_action
    - auditd_data_retention_admin_space_left_action
    - auditd_data_retention_action_mail_acct
    - auditd_audispd_syslog_plugin_activated
    - audit_rules_time_adjtimex
    - audit_rules_time_settimeofday
    - audit_rules_time_stime
    - audit_rules_time_clock_settime
    - audit_rules_time_watch_localtime
    - audit_rules_usergroup_modification
    - audit_rules_networkconfig_modification
    - file_permissions_var_log_audit
    - file_ownership_var_log_audit
    - audit_rules_mac_modification
    - audit_rules_dac_modification_chmod
    - audit_rules_dac_modification_chown
    - audit_rules_dac_modification_fchmod
    - audit_rules_dac_modification_fchmodat
    - audit_rules_dac_modification_fchown
    - audit_rules_dac_modification_fchownat
    - audit_rules_dac_modification_fremovexattr
    - audit_rules_dac_modification_fsetxattr
    - audit_rules_dac_modification_lchown
    - audit_rules_dac_modification_lremovexattr
    - audit_rules_dac_modification_lsetxattr
    - audit_rules_dac_modification_removexattr
    - audit_rules_dac_modification_setxattr
    - audit_rules_login_events
    - audit_rules_session_events
    - audit_rules_unsuccessful_file_modification
    - audit_rules_privileged_commands
    - audit_rules_media_export
    - audit_rules_file_deletion_events
    - audit_rules_sysadmin_actions
    - audit_rules_kernel_module_loading
    - audit_rules_immutable
    - service_ntpd_enabled
    - ntpd_specify_remote_server
    - ntpd_specify_multiple_servers
    - rpm_verify_permissions
    - rpm_verify_hashes
    - install_hids
    - rsyslog_files_permissions
    - rsyslog_files_ownership
    - rsyslog_files_groupownership
    - ensure_logrotate_activated
    - package_aide_installed
    - disable_prelink
    - aide_build_database
    - aide_periodic_cron_checking
    - account_unique_name
    - gid_passwd_group_same
    - accounts_password_all_shadowed
    - no_empty_passwords
    - display_login_attempts
    - account_disable_post_pw_expiration
    - accounts_passwords_pam_faillock_deny
    - accounts_passwords_pam_faillock_unlock_time
    - gconf_gnome_screensaver_idle_delay
    - gconf_gnome_screensaver_idle_activation_enabled
    - gconf_gnome_screensaver_lock_enabled
    - gconf_gnome_screensaver_mode_blank
    - sshd_set_idle_timeout
    - cracklib_accounts_password_pam_minlen
    - cracklib_accounts_password_pam_dcredit
    - cracklib_accounts_password_pam_ucredit
    - cracklib_accounts_password_pam_lcredit
    - accounts_passwords_pam_unix_remember
    - accounts_maximum_age_login_defs
    - ensure_redhat_gpgkey_installed
    - ensure_gpgcheck_globally_activated
    - ensure_gpgcheck_never_disabled
    - security_patches_up_to_date
    - smartcard_auth
    - set_password_hashing_algorithm_systemauth
    - set_password_hashing_algorithm_logindefs
    - set_password_hashing_algorithm_libuserconf
    - file_owner_etc_shadow
    - file_groupowner_etc_shadow
    - file_permissions_etc_shadow
    - file_owner_etc_group
    - file_groupowner_etc_group
    - file_permissions_etc_group
    - file_owner_etc_passwd
    - file_groupowner_etc_passwd
    - file_permissions_etc_passwd
    - file_owner_grub_conf
    - file_groupowner_grub_conf
    - package_libreswan_installed
