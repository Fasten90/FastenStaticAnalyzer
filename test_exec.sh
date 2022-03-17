echo "Test Exec" 

python FastenStaticAnalyzer.py --source="test/test_goto.c" --prepocessor="gcc" --preprocessor_args=""
python FastenStaticAnalyzer.py --source="test/test_2/test.c" --prepocessor="gcc" --preprocessor_args=""
python FastenStaticAnalyzer.py --source="test/test_simple_without_stdio/test_simple_without_stdio.c" --prepocessor="gcc" --preprocessor_args=""
python FastenStaticAnalyzer.py --source="test/test_stdio/test_stdio.c" --prepocessor="gcc" --preprocessor_args=""
