#!/usr/bin/env python

from test_cases import TestCases

with TestCases() as test:
    test.user_exists()
    test.file_exists('/etc/periodic/hourly/nntpd-sync')
    test.file_contains(file_name='/etc/periodic/hourly/nntpd-sync',
                       string_contents='ntpd -d -q -n -p uk.pool.ntp.org')
    test.file_exists('/etc/timezone')
    test.file_contains(file_name='/etc/timezone',
                       string_contents='Europe/London')
    test.package_exists('openntpd')
    test.package_exists('git')
    test.package_exists('ruby')
    test.package_exists('bash')
    test.package_exists('py-pip')
    test.pip_module_exists('awscli')
    test.ruby_gem_exists('inspec')
    test.has_env_var('PAGER')
    test.package_exists('groff')
    test.package_exists('jq')
