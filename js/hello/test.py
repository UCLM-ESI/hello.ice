#!/usr/bin/prego

# The browser side can not be tested here, see ../../py/bidir-adapter/test.py
# for the server side (with a Python peer instead of the browser)

from prego import TestCase, Task, File, exists, context


class Hello(TestCase):
    def test_slice2js(self):
        context.cwd = '$testdir'
        build = Task('build')
        build.command('make clean all', timeout=30)
        build.assert_that(File('$testdir/printer.js'), exists())
        build.assert_that(File('$testdir/BidirAdapter.js'), exists())
