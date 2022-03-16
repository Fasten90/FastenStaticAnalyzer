import unittest

from FastenStaticAnalyzer import FileStaticAnalysis

class TestReferenceFiles(unittest.TestCase):

    def call_file_statis_analysis(self, source,
                                  preprocessor='gcc',
                                  pre_arg=["-E", r"-Ipycparser/utils/fake_libc_include"]
                                  ):
        preprocessed_file_path = source + '_ast_generated.txt'
        pycparser_ast_generated = source + '_preprocessed.c'

        file_analysis = FileStaticAnalysis(source,
                                   preprocessor, pre_arg,
                                   preprocessed_file_path,
                                   pycparser_ast_generated)
        return file_analysis.run()

    def test_split(self):
        source = 'test/test_goto.c'
        result = self.call_file_statis_analysis(source)
        assert result == []


if __name__ == '__main__':
    unittest.main()

