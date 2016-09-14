from __future__ import unicode_literals
import codecs
import os
from unittest import TestCase
from obs_door43.obs_door43 import OBSDoor43


class TestOBSDoor43(TestCase):

    def setUp(self):
        """
        Runs before each test
        """
        self.cleanTargetDir()

    def tearDown(self):
        """
        Runs after each test
        """
        pass

    @classmethod
    def cleanTargetDir(cls):
        target_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'target')
        for file_name in [f for f in os.listdir(target_dir) if not f.endswith('.gitignore')]:
            os.remove(os.path.join(target_dir, file_name))

    @classmethod
    def setUpClass(cls):
        """
        Called before tests in this class are run
        """
        pass

    @classmethod
    def tearDownClass(cls):
        """
        Called after tests in this class are run
        """
        cls.cleanTargetDir()

    def test_run(self):

        this_dir = os.path.dirname(os.path.realpath(__file__))
        test_source_location = 'file://' + os.path.join(this_dir, 'source')
        test_output_location = os.path.join(this_dir, 'target')
        test_template = 'file://' + os.path.join(this_dir, 'source', 'obs_template.html')

        with OBSDoor43(test_source_location, test_output_location, test_template, True) as obs:
            obs.run()

        # should be 50 html files in test_output_location
        html_files = [f for f in os.listdir(test_output_location) if f.endswith('.html')]
        self.assertEqual(50, len(html_files))

        # check 50.html
        with codecs.open(os.path.join(test_output_location, '50.html'), 'r', 'utf-8-sig') as obs_file:
            html = obs_file.read()

        # check for language
        self.assertGreater(html.find('<html lang="en">'), -1)

        # check canonical
        self.assertGreater(html.find('<link href="https://live.door43.org/en/obs.html" rel="canonical">'), -1)

        # check for obs content from source file
        self.assertGreater(html.find('<div class="obs-content">'), -1)

        # check the title
        self.assertGreater(html.find('<title>Open Bible Stories</title>'), -1)
