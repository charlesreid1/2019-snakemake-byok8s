from unittest import TestCase
from subprocess import call, Popen, PIPE
import os
import shutil, tempfile
from os.path import isdir, join


"""
test byok8s

This tests the byok8s command line utility,
and assumes you have already set up your
k8s cluster using e.g. minikube.
"""


class TestByok8s(TestCase):
    """
    simple byok8s test class

    This uses the subprocess PIPE var
    to capture system input and output,
    since we are running byok8s from the
    command line directly using subprocess.
    """
    @classmethod
    def setUpClass(self):
        """
        set up a byok8s workflow test.
        """
        pass

    def test_hello(self):
        """
        test hello workflow
        """
        command_prefix = ['byok8s','workflow-zeta']

        params = ['params-red','params-blue']

        pwd = os.path.abspath(os.path.dirname(__file__))

        for param in params:
            
            command = command_prefix + [param]

            p = Popen(command, cwd=pwd, stdout=PIPE, stderr=PIPE).communicate()
            p_out = p[0].decode('utf-8').strip()
            p_err = p[1].decode('utf-8').strip()

            self.assertIn('details',p_out)

            # clean up
            call(['rm','-f','*.txt'])


    @classmethod
    def tearDownClass(self):
        """
        clean up after the tests
        """
        pass

