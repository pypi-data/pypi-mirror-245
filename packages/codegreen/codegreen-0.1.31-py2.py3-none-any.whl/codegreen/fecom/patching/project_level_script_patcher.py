import ast
import argparse
from codegreen.fecom.patching.patching_config import PROJECT_PATH, TOOL_INSTALLATION_PATH

# parser = argparse.ArgumentParser()
# parser.add_argument("input_files", type=argparse.FileType("r"))
# args = parser.parse_args()

def project_level_patcher(script_path_to_be_patched,meta_data):
    # Step1: Create an AST from the client python code
    global sourceCode
    # global args
    with open(script_path_to_be_patched, 'r') as file:
        sourceCode = file.read()
    tree = ast.parse(sourceCode)

    # create nodes to add before and after the method call
    before_execution_call = (
        "start_times_INSERTED_INTO_SCRIPT = before_execution_INSERTED_INTO_SCRIPT(enable_skip_calls = False)"
    )
    global before_execution_call_node
    before_execution_call_node = ast.parse(before_execution_call)

    after_execution_call = (
        "after_execution_INSERTED_INTO_SCRIPT(start_times=start_times_INSERTED_INTO_SCRIPT, experiment_file_path=EXPERIMENT_FILE_PATH, enable_skip_calls = False)"
    )
    global after_execution_call_node
    after_execution_call_node = ast.parse(after_execution_call)
    with open(TOOL_INSTALLATION_PATH / 'patching/project_level_patch_imports.py', "r") as source:
        cm = source.read()
        cm_node = ast.parse(cm)
        tree.body.insert(0, before_execution_call_node)
        tree.body.insert(0, cm_node)
        tree.body.insert(len(tree.body), after_execution_call_node)
    
    # Step6: Unparse and convert AST to final code
    # print(ast.unparse(tree))
    patched_code = ast.unparse(tree)

    # Write the patched code back to the file
    with open(script_path_to_be_patched, 'w') as file:
        file.write(patched_code)


# if __name__ == "__main__":
#     main()