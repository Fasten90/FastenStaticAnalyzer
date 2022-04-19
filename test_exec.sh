#!/bin/bash
set -e

echo "Test Exec"

python FastenStaticAnalyzer.py --help
python FastenStaticAnalyzer.py --source="test/test_1_goto/test_goto.c" --preprocessor="gcc" --preprocessor_args=""
python FastenStaticAnalyzer.py --source="test/test_2/test_2.c" --preprocessor="gcc" --preprocessor_args="-std=c99 -nostdinc -E -D_Atomic(_arg)=_arg -Ipycparser/utils/fake_libc_include"
python FastenStaticAnalyzer.py --source="test/test_simple_without_stdio/test_simple_without_stdio.c" --preprocessor="gcc" --preprocessor_args=""
python FastenStaticAnalyzer.py --source="test/test_stdio/test_stdio.c" --preprocessor="gcc" --preprocessor_args="-std=c99 -nostdinc -E -D_Atomic(_arg)=_arg -Ipycparser/utils/fake_libc_include"
python FastenStaticAnalyzer.py --source="test/test_system_call_3/test.c" --preprocessor="gcc" --preprocessor_args="" --delete_temporary_files --export_file=bla_result_2.txt
