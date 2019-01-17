from unittest import TestCase
from subprocess import call, Popen, PIPE
import os
import shutil, tempfile
from os.path import isdir, join


"""
test banana

this test will run bananas with the test
config and params provided in the test dir.

this test will also show how to run tests where
failure is expected (i.e., checking that we handle
invalid parameters).

each test has a unittest TestCase defined.
pytest will automatically find these tests.
"""


class TestBananas(TestCase):
    """
    simple bananas test class

    This uses the subprocess PIPE var
    to capture system input and output,
    since we are running bananas from the
    command line directly using subprocess.
    """
    @classmethod
    def setUpClass(self):
        """
        set up a bananas workflow test.

        we are using the existing test/ dir
        as our working dir, so no setup to do.

        if we were expecting the user to provide
        a Snakefile, this is where we would set
        up a test Snakefile.
        """
        pass

    def test_hello(self):
        """
        test hello workflow
        """
        command_prefix = ['bananas','workflow-hello']

        params = ['params-amy','params-beth']

        pwd = os.path.abspath(os.path.dirname(__file__))

        for param in params:
            
            command = command_prefix + [param]

            p = Popen(command, cwd=pwd, stdout=PIPE, stderr=PIPE).communicate()
            p_out = p[0].decode('utf-8').strip()
            p_err = p[1].decode('utf-8').strip()

            self.assertIn('details',p_out)

            # clean up
            call(['rm','-f','hello.txt'])


    @classmethod
    def tearDownClass(self):
        """
        clean up after the tests
        """
        pass

