import subprocess

import json

INTRO_TASKS = [
    "4004",
    "4058",
    "4063",
    "4065",
    "4100",
    "4108",
    "4117",
    "4155",
    "4164",
    "4182",
    "4193",
    "4195",
    "4211",
    "4217",
    "4241",
    "4249",
    "4270",
    "4275",
    "4281",
    "4293",
    "4333",
    "4347",
    "4350",
    "4356",
    "4409",
    "4426",
    "4431",
    "4450",
    "4465",
    "4484",
    "4498",
    "4505",
    "4507",
    "4514",
    "4544",
    "4553",
    "4586",
    "4610",
    "4662",
    "4663",
    "4667",
    "4677",
    "4681",
    "4704",
    "4716",
    "4741",
    "4750",
    "4786",
    "4787",
    "4801",
    "4855",
    "4862",
    "4864",
    "4870",
    "4873",
    "4890",
    "4897",
    "4952",
    "4966",
    "4984",
]
INTERVIEW_TASKS = [
    "0004",
    "0013",
    "0033",
    "0056",
    "0073",
    "0074",
    "0089",
    "0091",
    "0124",
    "0131",
    "0139",
    "0162",
    "0166",
    "0183",
    "0186",
    "0191",
    "0199",
    "0205",
    "0249",
    "0253",
    "0268",
    "0274",
    "0300",
    "0304",
    "0341",
    "0342",
    "0413",
    "0427",
    "0434",
    "0466",
    "0467",
    "0496",
    "0501",
    "0511",
    "0537",
    "0564",
    "0571",
    "0575",
    "0579",
    "0592",
    "0597",
    "0626",
    "0637",
    "0676",
    "0704",
    "0728",
    "0757",
    "0765",
    "0788",
    "0794",
    "0804",
    "0805",
    "0811",
    "0829",
    "0879",
    "0904",
    "0915",
    "0925",
    "0937",
    "0948",
    "0954",
    "0955",
    "0972",
    "0985",
    "0989",
    "1018",
    "1019",
    "1033",
    "1046",
    "1076",
    "1133",
    "1140",
    "1141",
    "1145",
    "1146",
    "1149",
    "1168",
    "1185",
    "1221",
    "1232",
    "1256",
    "1257",
    "1280",
    "1285",
    "1299",
    "1317",
    "1347",
    "1380",
    "1392",
    "1393",
    "1418",
    "1444",
    "1448",
    "1458",
    "1489",
    "1517",
    "1533",
    "1573",
    "1635",
    "1653",
    "1668",
    "1672",
    "1721",
    "1736",
    "1748",
    "1756",
    "1759",
    "1775",
    "1777",
    "1825",
    "1850",
    "1863",
    "1865",
    "1870",
    "1875",
    "1906",
    "1917",
    "1956",
    "1962",
    "1967",
    "1976",
    "2024",
    "2049",
    "2062",
    "2092",
    "2093",
    "2097",
    "2106",
    "2172",
    "2176",
    "2203",
    "2231",
    "2246",
    "2264",
    "2266",
    "2295",
    "2326",
    "2328",
    "2332",
    "2342",
    "2361",
    "2369",
    "2407",
    "2408",
    "2418",
    "2455",
    "2463",
    "2511",
    "2515",
    "2516",
    "2535",
    "2585",
    "2623",
    "2629",
    "2642",
    "2651",
    "2662",
    "2668",
    "2673",
    "2698",
    "2701",
    "2709",
    "2735",
    "2742",
    "2752",
    "2759",
    "2765",
    "2787",
    "2802",
    "2832",
    "2835",
    "2844",
    "2858",
    "2885",
    "2897",
    "2923",
    "2932",
    "2945",
    "2973",
    "2980",
]
COMPETITION_TASKS = [
    "3017",
    "3019",
    "3054",
    "3062",
    "3063",
    "3066",
    "3070",
    "3077",
    "3083",
    "3097",
    "3117",
    "3135",
    "3161",
    "3186",
    "3209",
    "3220",
    "3286",
    "3287",
    "3323",
    "3335",
    "3353",
    "3355",
    "3371",
    "3375",
    "3376",
    "3388",
    "3404",
    "3411",
    "3433",
    "3441",
    "3445",
    "3470",
    "3481",
    "3484",
    "3548",
    "3557",
    "3605",
    "3609",
    "3634",
    "3635",
    "3671",
    "3679",
    "3709",
    "3754",
    "3769",
    "3792",
    "3798",
    "3799",
    "3804",
    "3810",
    "3819",
    "3823",
    "3836",
    "3843",
    "3849",
    "3876",
    "3913",
    "3934",
    "3972",
    "3974",
]

BASE_DIR = "/Users/pbharrin/Downloads/APPS/train/"


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


if __name__ == "__main__":
    all_tasks = INTRO_TASKS + INTERVIEW_TASKS + COMPETITION_TASKS

    fp = open("evals/new_code_APPS_dataset.yaml", "w")
    fp.write("evaluations:\n")

    for task_str in INTRO_TASKS[:9]:
        print(f"formatting: {task_str}")

        # open the question.txt
        question_text = open(f"{BASE_DIR}{task_str}/question.txt").read()
        print(f"question text: {question_text}")

        # open input_output.json
        io_json = json.load(open(f"{BASE_DIR}{task_str}/input_output.json"))
        print(io_json)

        print("function name: ", io_json["fn_name"])

        # write YAML
        add_task(fp, task_str, question_text, io_json)
        for i, _ in enumerate(io_json["inputs"]):
            add_argument_test(
                fp, io_json["fn_name"], io_json["inputs"][i], io_json["outputs"][i]
            )

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
