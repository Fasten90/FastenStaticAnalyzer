import unittest

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "pycparser"))

import FastenStaticAnalyzer


class TestSystem(unittest.TestCase):

    def test_system_call_1(self):
        # E.g. python FastenStaticAnalyzer.py --source="test/test_1_goto/test_goto.c" --prepocessor="gcc" --preprocessor_args=""
        # Note: argv0 is the name of script
        test_dir = os.path.dirname(__file__)
        root_dir = os.path.join(test_dir, '..')
        source_file_path = os.path.join(root_dir, 'test/test_1_goto/test_goto.c')
        os.chdir(root_dir)
        sys.argv = ['FastenStaticAnalyzer.py', '--source={}'.format(source_file_path), '--preprocessor=gcc']  # , '--preprocessor_args=""'
        FastenStaticAnalyzer.main()

    def test_system_call_2(self):
        # Cannot debug
        import subprocess
        subprocess.call(
            'python FastenStaticAnalyzer.py --source="test/test_1_goto/test_goto.c" --preprocessor="gcc" --preprocessor_args=""',
            shell=True)

    def test_system_call_3(self):
        # Cannot debug
        import subprocess
        subprocess.call(
            'python FastenStaticAnalyzer.py --source="test/test_system_call_3/test.c" --delete_temporary_files',
            shell=True)


if __name__ == '__main__':
    unittest.main()

