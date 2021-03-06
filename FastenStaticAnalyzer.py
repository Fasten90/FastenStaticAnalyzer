import argparse
from enum import Enum
import sys
import os
import csv

# Import the pycparser lib
sys.path.append(os.path.join(os.path.dirname(__file__), "pycparser"))

from pycparser import c_ast, preprocess_file, parse_file # pylint: disable=wrong-import-position


func_declarations = set()
func_calls = set()
goto_used = set()
return_used = set()
func_calls_all = []

# Debug functions

DEBUG_AST = False

def debug_print(msg):
    print(msg)


class FileStaticAnalysisConfig():

    def __init__(self):

        self.CONFIG_LIST_UNUSED_FUNCTIONS = True

        self.CONFIG_LIST_CALL_LIST = True

        self.CONFIG_ANALYSE_GOTO = True

        self.CONFIG_ANALYSE_RETURN = True


class StaticAnalysisType(Enum):
    DEFAULT = 1
    OPTIONAL = 2


class FileStaticAnalysis():

    def __init__(self,
                 input_file_path,
                 preprocessor_path, preprocessor_args,
                 preprocessed_file_path, pycparser_ast_generated):
        self.__input_file_path = input_file_path
        self.__preprocessor_path = preprocessor_path
        self.__preprocessor_args = preprocessor_args
        self.__preprocessed_file_path = preprocessed_file_path
        self.__pycparser_ast_generated = pycparser_ast_generated


        self.__parse_result = None

        self.__config = FileStaticAnalysisConfig()
        self.__analysis_list = [
            {
                "name": "FuncDef",
                "type": StaticAnalysisType.DEFAULT,
                "config": None,
                "checker": self.FuncDef
            },
            {
                "name": "FuncCall",
                "type": StaticAnalysisType.DEFAULT,
                "config": None,
                "checker": self.FuncCall
            },
            {
                "name": "Unused functions",
                "type": StaticAnalysisType.OPTIONAL,
                "config": self.__config.CONFIG_LIST_UNUSED_FUNCTIONS,
                "checker": self.UnusedFunctions
            },
            {
                "name": "Call list",
                "type": StaticAnalysisType.OPTIONAL,
                "config": self.__config.CONFIG_LIST_CALL_LIST,
                "checker": self.CallList
            },
            {
                "name": "Goto",
                "type": StaticAnalysisType.OPTIONAL,
                "config": self.__config.CONFIG_ANALYSE_GOTO,
                "requirements": {"group": "Misra 2004", "rule": "Rule 14.4", "category": "required", "description": "The goto statement shall not be used"},
                "checker": self.Goto
            },
            {
                "name": "Return",
                "type": StaticAnalysisType.OPTIONAL,
                "config": self.__config.CONFIG_ANALYSE_RETURN,
                "requirements": {"group": "Misra 2004", "rule": "Rule 14.7", "category": "required", "description": "A function shall have a single point of exit at the end of the function"},
                "checker": self.Return
            }
        ]

        self.__analysis_result = []


    def run(self):

        if not os.path.exists(self.__input_file_path):
            raise Exception('Source file does not exist!')

        # Preprocess
        preprocessed_file_content = preprocess_file(
            self.__input_file_path,
            cpp_path=self.__preprocessor_path,
            cpp_args=self.__preprocessor_args)

        with open(self.__preprocessed_file_path, "w") as f:
            f.write(preprocessed_file_content)

        # Parse

        # Expect preprocessed file!
        self.__parse_result = parse_file(self.__preprocessed_file_path)
        # use_cpp=False, cpp_path='cpp', cpp_args='',
        #                parser=None
        # TODO: Test this: use_cpp=True - only for preprocessor

        parse_result_str = str(self.__parse_result)

        # Save the AST to file
        with open(self.__pycparser_ast_generated, "w") as f:
            f.write(parse_result_str)

        if DEBUG_AST:
            # Print AST
            print("##########################")
            for ast_item in self.__parse_result:
                print(str(ast_item))

            print("##########################")
            self.__parse_result.show()

        result_all = []

        # Execute checker
        for checker in self.__analysis_list:
            result = None
            if checker["type"] == StaticAnalysisType.DEFAULT:
                result = self.call_checker(checker)
            elif checker["type"] == StaticAnalysisType.OPTIONAL:
                if checker["config"]:
                    # Enabled, run
                    print("######################")
                    print("This checker is enabled, execute: {}".format(checker["name"]))
                    print("######################")
                    print("")
                    result = self.call_checker(checker)
                    print("")
                    print("This checker has finished: {}".format(checker["name"]))
                    print("-----------------------")
                    print("")
                else:
                    # Disabled
                    print("This checker has been disabled: {}".format(checker["name"]))
            else:
                raise Exception("Wrong StaticAnalysisType")
            if result:
                result_all.extend(result)

        return result_all


    def call_checker(self, checker):
        # Call the checker
        checker_result = checker["checker"]()
        res = []
        if checker_result:
            for item in checker_result:
                res.append({'checker': checker["name"], 'error': item})
        return res


    def FuncCall(self):
        checker_obj = FuncCallVisitor()
        checker_obj.visit(self.__parse_result)
        # Listing
        func_calls_str = "".join(str(item) + "\n" for item in func_calls)

        print("Func calls: (Called functions)")
        print(func_calls_str)


    def FuncDef(self):
        checker_obj = FuncDefVisitor()
        checker_obj.visit(self.__parse_result)

        # Listing
        func_def_str = "".join(item + "\n" for item in func_declarations)

        print("Func definitions: (Declared functions)")
        print(func_def_str)
        # print to file


    def UnusedFunctions(self):
        # Not used functions:
        print("######################")
        print("Not used functions:")
        func_not_used = func_declarations - func_calls
        func_not_used_str = "".join(item + "\n" for item in func_not_used)
        print(func_not_used_str)


    def CallList(self):
        # Try collect, an function where was called
        func_call_all_list = {}
        for an_func_call in func_calls_all:
            # Check keyword
            called_function = an_func_call[0]
            caller_function = an_func_call[1]
            if an_func_call[0] in func_call_all_list:
                # If is in, add this called function
                func_call_all_list[called_function].append(caller_function)
            else:
                # Not in, new
                func_call_all_list[called_function] = [caller_function]

        print("Calls")
        # ugly format
        # print(func_call_all_list)
        # for item in func_call_all_list.items():
        for key, value in func_call_all_list.items():
            print("'{}' called from:\n"
                  "{}".format(
                      key,
                      "".join(["  " + item.file + ":" + str(item.line) + "\n" for item in value])))


    def Goto(self):
        # Goto
        global goto_used
        goto_used = set()

        checker_obj = GotoVisitor()
        checker_obj.visit(self.__parse_result)

        goto_used_str = "".join(item + "\n" for item in goto_used)

        debug_print("Goto used: {}".format(goto_used_str))

        return goto_used


    def Return(self):
        # Return
        # TODO: Cannot check easily, which function' return
        # checker_obj = ReturnVisitor()
        # checker_obj.visit(parse_result)

        res = []

        def find_return_in_recursive(item_list):
            return_count = 0
            if isinstance(item_list, c_ast.Return):
                return 1
            for item in item_list:
                return_count += find_return_in_recursive(item)
            return return_count

        # Explore AST - for return
        for ast_item in self.__parse_result:
            # print(str(ast_item))
            if isinstance(ast_item, c_ast.FuncDef):
                # Explore the body
                function_name = ast_item.decl.name
                return_all_count = 0
                for body_item in ast_item.body:
                    # print(str(body_item))
                    # if isinstance(body_item, c_ast.Return):
                    #    return_all_count += 1
                    return_all_count += find_return_in_recursive(body_item)
                print("Function: '{}' has {} return".format(function_name, return_all_count))
                # Check result:
                if return_all_count > 1:
                    # Save as wrong
                    print('ISSUE: More return than 1')  # TODO: New function for this
                    res.append((function_name, return_all_count))

        # res will contains function_name - return count pairs (which are issues)
        return res


# Note: be careful, this was child of a pycparser class
class FuncCallVisitor(c_ast.NodeVisitor):

    def __init__(self):
        pass

    # Note: https://github.com/eliben/pycparser/blob/master/examples/func_calls.py
    def visit_FuncCall(self, node):
        # This was called by pycparser NodeVisitor automatically
        # TODO: Dont care which function
        print("Called '{}' function from '{}'".format(node.name.name, node.name.coord))

        global func_calls
        global func_calls_all
        func_calls.add(node.name.name)
        func_calls_all.append((node.name.name, node.name.coord))
        # Visit args in case they contain more func calls.
        if node.args:
            print("Called an another function from: '{}'".format(node.name.name))
            self.visit(node.args)  # Recursion


class FuncDefVisitor(c_ast.NodeVisitor):
    # Note: https://github.com/eliben/pycparser/blob/master/examples/func_defs.py
    def visit_FuncDef(self, node):
        # This was called by pycparser NodeVisitor automatically
        print("Function declaration: '{}' at '{}'".format(node.decl.name, node.decl.coord))

        global func_declarations
        func_declarations.add(node.decl.name)


# Goto checker
class GotoVisitor(c_ast.NodeVisitor):
    # Note: https://github.com/eliben/pycparser/blob/master/examples/func_defs.py
    def visit_Goto(self, node):
        # This was called by pycparser NodeVisitor automatically
        print("Goto used '{}' at '{}'".format(node.name, node.coord))

        global goto_used
        goto_used.add(node.name)


# Return checker
class ReturnVisitor(c_ast.NodeVisitor):
    def visit_Return(self, node):
        # This was called by pycparser NodeVisitor automatically
        #print("Return used '{}' at '{}'".format(node.name, node.coord))

        global return_used
        return_used.add(node.coord)


def export_result_by_source_file(result_list, source_file, export_filename='static_analysis_result.csv', extend=False):
    if result_list:
        # Create CSV
        mode = 'a' if extend else 'w'
        with open(export_filename, mode=mode, newline='', encoding='utf-8') as csv_file:
            # TODO: Extend with more field
            fieldnames = ['file_path', 'line', 'checker', 'error']
            # TODO: Workaround
            line = 0
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in result_list:
                writer.writerow({'file_path': source_file, 'line': line, 'checker': row['checker'], 'error': row['error']})
            print('Exported to {}'.format(export_filename))


def remove_temporary_file(file_path):
    print('Remove temporary file: {}'.format(file_path))
    os.remove(file_path)


def main():

    parser = argparse.ArgumentParser(description='Fasten Static Analyzer')

    parser.add_argument('--source', type=str,
                        help='Source file for analysis')
    parser.add_argument('--preprocessor', type=str,
                        help='Preprocessor\n'
                             'E.g.: gcc')
    parser.add_argument('--preprocessor_args', type=str,
                        help='Preprocessor args\n'
                             'E.g. -Iinc')
    parser.add_argument('--delete_temporary_files', action='store_true',
                        help='Remove temporary files (preprocessed files)')
    parser.add_argument('--export_file', type=str,
                        default='StaticAnalysisResult.csv',
                        help='Export file path')
    parser.add_argument('--extend_export_file', action='store_true',
                        default=False,
                        help='Extend export file. It is useful for more source files')

    args = parser.parse_args()

    # Example:
    # --source="../../AtollicWorkspace/FastenHomeAut/Src/Common/Helper/MathHelper.c"
    if not os.path.exists(args.source):
        raise Exception('Source file does not exist: {}'.format(args.source))
        # TODO: Support glob

    if not args.preprocessor:
        args.preprocessor = 'gcc'
        print('Use default preprocessor: {}'.format(args.preprocessor))

    # At general C compilers, the "-E" is the preprocessing. It is required for pycparser
    # now, pycparser git repository has been downloaded into this directory (pycparser dir)
    if args.preprocessor_args:
        args.preprocessor_args = args.preprocessor_args.split(' ') + ["-E", r"-Ipycparser/utils/fake_libc_include", r"-Iutils/fake_libc_include"]
    else:
        args.preprocessor_args = ["-E", r"-Ipycparser/utils/fake_libc_include", r"-Iutils/fake_libc_include"]

    preprocessed_path = args.source + '_preprocessed.c'

    ast_file_path = args.source + '_ast_generated.txt'

    file_analysis = FileStaticAnalysis(args.source,
                                       args.preprocessor, args.preprocessor_args,
                                       preprocessed_path,
                                       ast_file_path)

    analysis_result = file_analysis.run()
    print("Results: \n"
          "{}".format(analysis_result))

    export_result_by_source_file(analysis_result, args.source, export_filename=args.export_file, extend=args.extend_export_file)

    # If remove required
    if args.delete_temporary_files:
        remove_temporary_file(preprocessed_path)
        remove_temporary_file(ast_file_path)


if __name__ == "__main__":
    main()
