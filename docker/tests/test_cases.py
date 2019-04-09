import pwd
import os
import subprocess

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Logger:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self):
        print("{}Tests started{}".format(self.OKBLUE, self.ENDC))

    def print_pass(self, message):
        out = "[Pass] {}{} {}{}".format(self.OKGREEN, u'\u2713', message, self.ENDC)
        print(out.encode('utf-8'))

    def print_fail(self, message):
        out = "[Fail] {}{} {}{}".format(self.FAIL, u'\u2718', message, self.ENDC)
        print(out.encode('utf-8'))


class TestCases:
    FAIL_EXIT = 0
    tests = 0
    errors = 0
    logging = None

    def __init__(self):
        self.FAIL_EXIT = -1
        self.logging = Logger()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("[Complete] {}{} tests ran{}"
              .format(self.logging.BOLD, self.tests, self.logging.ENDC))
        self.logging.print_pass("{} passed".format(self.tests - self.errors))
        if self.errors > 0:
            self.logging.print_fail("{} failed".format(self.errors))
            exit(self.FAIL_EXIT)

    @staticmethod
    def _file_exists(file_name):
        return os.path.exists(file_name)

    def _increment_tests(self):
        self.tests += 1

    def _increment_errors(self):
        self.errors += 1

    @staticmethod
    def _string_contains(needle, haystack):
        return needle in haystack

    def user_exists(self, user_name='tools'):
        self._increment_tests()
        try:
            pwd.getpwnam(user_name)
            self.logging.print_pass(message='User "{}" found'
                                    .format(user_name))
        except KeyError:
            self.logging.print_fail(message='User "{}" not found'
                                    .format(user_name))
            self._increment_errors()

    def file_exists(self, file_name):
        self._increment_tests()
        if self._file_exists(file_name):
            self.logging.print_pass(message='File "{}" exists'
                                    .format(file_name))
        else:
            self.logging.print_fail(message='File "{}" not found'
                                    .format(file_name))
            self._increment_errors()

    def package_exists(self, package_name):
        self._increment_tests()
        try:
            result = subprocess.check_output(['apk', 'info', package_name])
            if self._string_contains('installed size', result):
                self.logging.print_pass('Package "{}" installed'
                                        .format(package_name))
            else:
                self.logging.print_fail(message='Package "{}" not found'
                                        .format(package_name))
                self._increment_errors()
        except subprocess.CalledProcessError:
            self.logging.print_fail(message='Package "{}" not found'
                                    .format(package_name))
            self._increment_errors()

    def pip_module_exists(self, module_name):
        self._increment_tests()
        try:
            result = subprocess.check_output(['pip', 'freeze'])

            if self._string_contains(module_name, result):
                self.logging.print_pass('Pip module "{}" installed'
                                        .format(module_name))
            else:
                self.logging.print_fail(message='Pip module "{}" not found'
                                        .format(module_name))
                self._increment_errors()
        except subprocess.CalledProcessError:
            self.logging.print_fail(message='Pip command failed to run')
            self._increment_errors()

    def ruby_gem_exists(self, gem_name):
        self._increment_tests()
        try:
            result = subprocess.check_output(['gem', 'list', '--local'])

            if self._string_contains(gem_name, result):
                self.logging.print_pass('Ruby gem "{}" installed'
                                        .format(gem_name))
            else:
                self.logging.print_fail(message='Ruby gem "{}" not found'
                                        .format(gem_name))
                self._increment_errors()
        except subprocess.CalledProcessError:
            self.logging.print_fail(message='Gem command failed to run')
            self._increment_errors()

    def file_contains(self, file_name, string_contents):
        self._increment_tests()

        if self._file_exists(file_name):
            try:
                with open(file_name, 'r') as file_contents:
                    contents = file_contents.read()

                if not self._string_contains(string_contents, contents):
                    raise ValueError('Contents not found')

                self.logging.print_pass('Contents "{}" found in "{}"'
                                        .format(string_contents, file_name))
            except ValueError:
                self.logging.print_fail(message='"{}" not found in "{}"'
                                        .format(string_contents, file_name))
                self._increment_errors()

            except:
                self.logging.print_fail(message='Could not read contents from "{}"'
                                        .format(file_name))
                self._increment_errors()

        else:
            self.logging.print_fail(message='File "{}" not found'
                                    .format(file_name))
            self._increment_errors()

    def has_env_var(self, env_var):
        self._increment_tests()
        try:
            result = subprocess.check_output(['env'])
            if not self._string_contains(env_var, result):
                self.logging.print_fail('Environment var "{}" not set'
                                        .format(env_var))
                self._increment_errors()
            else:
                self.logging.print_pass('Environment var "{}" set'
                                        .format(env_var))
        except subprocess.CalledProcessError as e:
            self.logging.print_fail(message='Env command failed to run: {}'.format(e.message))
            self._increment_errors()

