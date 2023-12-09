# requirements
import pandas as pd
import json

# Convert a csv into a json file with metadata
def write_json_file(file_name, file_path=None, description=None, references=None, source=None, license=None):
    dataset = pd.read_csv(file_path + '/' + file_name + '.csv').dropna().to_dict()

    json_file = {
        "description": description,
        "references": references,
        "source": source,
        "license": license,
        "dataset": dataset
    }

    if file_path is not None:
        with open(file_path + '/' + file_name + ".json", "w") as outfile:
            json.dump(json_file, outfile)
    else:
        with open(os.getcwd() + '/' + file_name + ".json", "w") as outfile:
            json.dump(json_file, outfile)

