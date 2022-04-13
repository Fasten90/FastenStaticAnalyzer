#!/bin/bash
echo "Test Exec"

python FastenStaticAnalyzer.py --source="test/test_1_goto/test_goto.c" --prepocessor="gcc" --preprocessor_args=""
python FastenStaticAnalyzer.py --source="test/test_2/test_2.c" --prepocessor="gcc" --preprocessor_args="-std=c99 -nostdinc -E -D_Atomic(_arg)=_arg -Ipycparser/utils/fake_libc_include"
python FastenStaticAnalyzer.py --source="test/test_simple_without_stdio/test_simple_without_stdio.c" --prepocessor="gcc" --preprocessor_args=""
python FastenStaticAnalyzer.py --source="test/test_stdio/test_stdio.c" --prepocessor="gcc" --preprocessor_args="-std=c99 -nostdinc -E -D_Atomic(_arg)=_arg -Ipycparser/utils/fake_libc_include"
