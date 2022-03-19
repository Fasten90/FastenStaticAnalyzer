import unittest

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "pycparser"))

from FastenStaticAnalyzer import FileStaticAnalysis

class TestReferenceFiles(unittest.TestCase):

    def call_file_statis_analysis(self, source,
                                  preprocessor='gcc',
                                  pre_arg='-E'
                                  ):
        preprocessed_file_path = source + '_ast_generated.txt'
        pycparser_ast_generated = source + '_preprocessed.c'

        file_analysis = FileStaticAnalysis(source,
                                   preprocessor, pre_arg,
                                   preprocessed_file_path,
                                   pycparser_ast_generated)
        return file_analysis.run()

    def get_preprocessor_args_by_platform(self):
        from sys import platform
        if platform == "linux" or platform == "linux2":
            # linux
            return ['-std=c99',
             "-nostdinc",
             "-E",
             "-D_Atomic(_arg)=_arg",  # Important requirement. Without this I will get at Ubuntu:
            # pycparser.plyparser.ParseError: pycparser/utils/fake_libc_include/_fake_typedefs.h:175:24: before: atomic_bool
             r"-Ipycparser/utils/fake_libc_include"]
        elif platform == "darwin":
            # OS X
            raise Exception('Unsupported OS')
        elif platform == "win32":
            # Windows...
            return ['-std=c99',
                   "-nostdinc",
                   "-E",
                   #"-D_Atomic(_arg)=_arg", # Windows GCC does not require it
                   r"-Ipycparser/utils/fake_libc_include"]

    def test_ref_goto(self):
        source = 'test/test_goto.c'
        result = self.call_file_statis_analysis(source)
        assert result == []

    def test_ref_2(self):
        source = 'test/test_2/test.c'
        result = self.call_file_statis_analysis(source, preprocessor='gcc', pre_arg=self.get_preprocessor_args_by_platform())
        assert result == []

    def test_ref_simple_without_stdio(self):
        source = 'test/test_simple_without_stdio/test_simple_without_stdio.c'
        result = self.call_file_statis_analysis(source)
        assert result == []

    def test_ref_stdio(self):
        source = 'test/test_stdio/test_stdio.c'
        result = self.call_file_statis_analysis(source, preprocessor='gcc', pre_arg=self.get_preprocessor_args_by_platform())
        assert result == []


if __name__ == '__main__':
    unittest.main()

