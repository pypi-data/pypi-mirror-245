from src.translator_testing_model.datamodel.pydanticmodel import TestAsset, TestCase, TestSuite, TestMetadata
import csv
import json
import os
import requests


def parse_tsv(filename):
    """
    Parse a TSV file and return a list of dictionaries.

    :param filename: The path to the TSV file.
    :return: A list of dictionaries, where each dictionary represents a row in the TSV.
    """
    with open(filename, newline='', encoding='utf-8') as tsvfile:
        # Use csv.DictReader, specifying the delimiter as a tab
        reader = csv.DictReader(tsvfile, delimiter='\t')

        # Convert the reader into a list of dictionaries
        return list(reader)


# Functions to create TestAssets, TestCases, and TestSuite
def create_test_assets_from_tsv(test_assets):
    assets = []
    for row in test_assets:
        if row.get("Relationship") == "":
            continue
        ta = TestAsset(id=row.get("id").replace(":", "_"),
                       name=row.get("OutputName").replace(" ", "_") + "_" + row.get("Relationship").lower() + "_" + row.get("InputName (user choice)").replace(" ", "_"),
                       description=row.get("OutputName").replace(" ", "_") + "_" + row.get("Relationship").lower() + "_" + row.get("InputName (user choice)").replace(" ", "_"),
                       input_id=row.get("InputID, node normalized"),
                       predicate_name=row.get("Relationship").lower(),
                       predicate_id="biolink:"+row.get("Relationship").lower(),
                       output_id=row.get("OutputID"),
                       expected_output="NeverShow",
                       test_metadata=TestMetadata(id=1),
                       )
        ta.input_name = row.get("InputName (user choice)")
        if row.get("GitHubIssue") != "" and row.get("GitHubIssue") is not None:
            tmd = TestMetadata(id=1,
                               test_source="SMURF",
                               test_reference=row.get("GitHubIssue"),
                               test_objective="AcceptanceTest")
            ta.test_metadata = tmd
        else:
            tmd = TestMetadata(id=1,
                               test_source="SMURF",
                               test_objective="AcceptanceTest")
            ta.test_metadata = tmd
        ta.output_name = row.get("OutputName")
        ta.runner_settings = [row.get("Settings").lower()]
        if row.get("Expected Result / Suggested Comparator") == "4_NeverShow":
            ta.expected_output = "NeverShow"
        elif row.get("Expected Result / Suggested Comparator") == "3_BadButForgivable":
            ta.expected_output = "BadButForgivable"
        elif row.get("Expected Result / Suggested Comparator") == "2_Acceptable":
            ta.expected_output = "Acceptable"
        elif row.get("Expected Result / Suggested Comparator") == "1_TopAnswer":
            ta.expected_output = "TopAnswer"
        else:
            ta.expected_output = "NeverShow"

        if row.get("Well Known") == "yes":
            ta.well_known = True
        else:
            ta.well_known = False
        assets.append(ta)

    return assets


def create_test_cases_from_test_assets(test_assets, test_case_model):
    # Group test assets based on input_id and relationship
    grouped_assets = {}
    for test_asset in test_assets:
        key = (test_asset.input_id, test_asset.predicate_name)
        if key not in grouped_assets:
            grouped_assets[key] = []
        grouped_assets[key].append(test_asset)

    # Create test cases from grouped test assets
    test_cases = []
    for idx, (key, assets) in enumerate(grouped_assets.items()):
        test_case_id = f"TestCase_{idx}"
        descriptions = '; '.join(asset.description for asset in assets)
        test_case = test_case_model(id=test_case_id,
                                    name="what " + key[1] + " " + key[0],
                                    description=descriptions,
                                    test_env="ci",
                                    components=["ars"],
                                    test_case_objective="AcceptanceTest",
                                    test_assets=assets,
                                    test_case_runner_settings=["inferred"]
                                    )
        if test_case.test_assets is None:
            print("test case has no assets", test_case)

        if test_case.test_case_objective == "AcceptanceTest":
            test_input_id = ""
            test_case_predicate_name = ""
            for asset in assets:
                test_input_id = asset.input_id
                test_case_predicate_name = asset.predicate_name

            test_case.test_case_input_id = test_input_id
            test_case.test_case_predicate_name = test_case_predicate_name
            test_case.test_case_predicate_id = "biolink:" + test_case_predicate_name
            test_cases.append(test_case)

    return test_cases


def create_test_suite_from_test_cases(test_cases, test_suite_model):
    test_suite_id = "TestSuite_1"
    test_cases_dict = {test_case.id: test_case for test_case in test_cases}
    tmd = TestMetadata(id=1,
                          test_source="SMURF",
                          test_objective="AcceptanceTest")
    return test_suite_model(id=test_suite_id, test_cases=test_cases_dict, test_metadata=tmd)


if __name__ == '__main__':

    # Reading the TSV file
    tsv_file_path = 'pf_test_assets_2023_11_28.tsv'
    print(f"Error: The file {tsv_file_path} does not exist in the directory {os.getcwd()}.")
    tsv_data = parse_tsv(tsv_file_path)

    # Create TestAsset objects
    test_assets = create_test_assets_from_tsv(tsv_data)
    for asset in test_assets:
        if asset.test_metadata is None or asset.test_metadata == "":
            print(asset)

    # Create TestCase objects
    test_cases = create_test_cases_from_test_assets(test_assets, TestCase)
    for case in test_cases:
        if case.test_assets is None or case.test_assets == "":
            print(case)
    #
    # Assemble into a TestSuite
    test_suite = create_test_suite_from_test_cases(test_cases, TestSuite)
    #
    # Convert to JSON and save to file
    test_suite_json = test_suite.json(indent=4)

    suite_json_output_path = 'test_suite_output.json'

    with open(suite_json_output_path, 'w') as file:
        file.write(test_suite_json)

    for i, item in enumerate(test_cases):
        file_prefix = item.id
        filename = f"{file_prefix}.json"
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(item.dict(), file, ensure_ascii=False, indent=4)

    for i, item in enumerate(test_assets):
        file_prefix = item.id
        filename = f"{file_prefix}.json"
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(item.dict(), file, ensure_ascii=False, indent=4)

    url = 'https://raw.githubusercontent.com/TranslatorSRI/Benchmarks/main/config/benchmarks.json'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response content as JSON
        data = response.json()
        for k, v in data.items():
            tmd = TestMetadata(id=1,
                               test_source="SMURF",
                               test_objective="QuantitativeTest")
            ta = TestAsset(id=k,
                            name=k,
                            description=k,
                            test_metadata=tmd
                            )
            tc = TestCase(id=k,
                          name=k,
                          description=k,
                          test_assets=[ta],
                          test_env="ci",
                          components=["ars"],
                          test_case_objective="QuantitativeTest",
                          )
            file_prefix = k
            filename = f"{file_prefix}.json"
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(tc.dict(), file, ensure_ascii=False, indent=4)

    else:
        print(f'Failed to retrieve the file. Status code: {response.status_code}')
