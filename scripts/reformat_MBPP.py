import subprocess

import json


BASE_DIR = "/Users/pbharrin/Downloads/"
SOURCE_FILE = "mbpp.jsonl"


def format_ans(in_val) -> str:
    """Format the input for the YAML file"""
    if type(in_val) == str:
        raw_str = in_val.encode("unicode_escape")
        return f'"{raw_str}"'
    elif in_val is None:
        return "None"
    elif type(in_val) == list or type(in_val) == int:
        return str(in_val)
    else:
        raise Exception(f"no format for: {type(in_val)}")


def add_argument_test(fp, fun_name: str, test_in: str, test_out: str):
    """should look like this
    - type: check_executable_satisfies_function
      executable_name: "python currency.py"
      executable_arguments: "USD CAD 10"
      output_satisfies: "tf = lambda a : a.replace('.', '').isnumeric()"
    """
    ind = "     "
    fp.write(ind + f" - type: check_executable_satisfies_function\n")
    fp.write(ind + f"   executable_name: python {fun_name}.py\n")
    fp.write(ind + f"   executable_arguments: {test_in[0]}\n")
    pre = format_ans(test_out[0])
    fp.write(ind + f"   output_satisfies: tf = lambda a: a == {pre}\n")


def add_task(fp, task_num: str, question_str: str, test_json: dict):
    """should add these next two lines
    project_root: "projects/currency_converter"
    code_prompt: "Build a currency converter CLI tool in Python using an API for exchange rates.  The currency converter should be a python program named currency.py with three required arguments: base currency symbol, target currency symbol and base currency amount.  The currency converter will convert the amount in base currency amount to the target currency.  The output of the program should only be the amount of target currency.  For example the following command: `python currency.py USD CNY 1` should return a number like 7.5."
    """
    ind = "     "
    fp.write(f" - name: {task_num}\n")
    fp.write(f'   project_root: "projects/{task_num}"\n')
    fp.write(f"   code_prompt: |\n")
    for line in question_str.splitlines():
        fp.write(ind + line + "\n")
    fp.write(
        f"\n" + ind + f"The function created should be called: {test_json['fn_name']}\n"
    )
    fp.write(f"   expected_results:\n")


def find_ftn_name(code_body: str) -> str:
    for line in code_body.split("\r\n"):
        if line.startswith("def "):
            # TODO: parse out function name between first space and first (
            return


if __name__ == "__main__":
    fp = open("evals/new_code_MBPP_dataset.yaml", "w")  # output
    fp.write("evaluations:\n")

    for task_str in open(BASE_DIR + SOURCE_FILE).readlines()[:2]:
        ts = json.loads(task_str)
        print(f"formatting: {ts}")
        print("keys: ", list(ts.keys()))

        # keys: 'text', 'code', 'task_id', 'test_setup_code', 'test_list', 'challenge_test_list'
        # text = question prompt
        print("test_list: ", ts["test_list"])
        print("text: ", ts["text"])

        function_name = ts["code"]

        # open input_output.json
        # io_json = json.load(open(f"{BASE_DIR}{task_str}/input_output.json"))
        # print(io_json)

        # print("function name: ", io_json['fn_name'])

        # # write YAML
        # add_task(fp, task_str, question_text, io_json)
        # for i, _ in enumerate(io_json['inputs']):
        #     add_argument_test(fp,
        #                       io_json['fn_name'],
        #                       io_json['inputs'][i],
        #                       io_json['outputs'][i]
        #     )

    fp.close()

"""  minimum evaluation file
evaluations:
 - name: currency_converter
   project_root: "projects/currency_converter"
   code_prompt: "Build a currency converter CLI tool in Python using an API for exchange rates.  The currency converter should be a python program named currency.py with three required arguments: base currency symbol, target currency symbol and base currency amount.  The currency converter will convert the amount in base currency amount to the target currency.  The output of the program should only be the amount of target currency.  For example the following command: `python currency.py USD CNY 1` should return a number like 7.5."
   expected_results:
    - type: check_executable_exits_normally
      executable_name: "python currency.py"
      executable_arguments: "USD CAD 10"
    - type: check_executable_satisfies_function
      executable_name: "python currency.py"
      executable_arguments: "USD CAD 10"
      output_satisfies: "tf = lambda a : a.replace('.', '').isnumeric()"
"""
