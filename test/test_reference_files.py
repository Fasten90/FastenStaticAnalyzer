import unittest

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "pycparser"))

from FastenStaticAnalyzer import FileStaticAnalysis

class TestReferenceFiles(unittest.TestCase):

    def call_file_statis_analysis(self, source,
                                  preprocessor='gcc',
                                  # "-nostdinc",
                                  pre_arg=['-std=c11', "-E", r"-Ipycparser/utils/fake_libc_include"]
                                  ):
        preprocessed_file_path = source + '_ast_generated.txt'
        pycparser_ast_generated = source + '_preprocessed.c'

        file_analysis = FileStaticAnalysis(source,
                                   preprocessor, pre_arg,
                                   preprocessed_file_path,
                                   pycparser_ast_generated)
        return file_analysis.run()

    def test_ref_goto(self):
        source = 'test/test_goto.c'
        result = self.call_file_statis_analysis(source)
        assert result == []

    def test_ref_2(self):
        source = 'test/test_2/test.c'
        result = self.call_file_statis_analysis(source)
        assert result == []

    def test_ref_simple_without_stdio(self):
        source = 'test/test_simple_without_stdio/test_simple_without_stdio.c'
        result = self.call_file_statis_analysis(source)
        assert result == []

    def test_ref_stdio(self):
        source = 'test/test_stdio/test_stdio.c'
        result = self.call_file_statis_analysis(source)
        assert result == []


if __name__ == '__main__':
    unittest.main()

