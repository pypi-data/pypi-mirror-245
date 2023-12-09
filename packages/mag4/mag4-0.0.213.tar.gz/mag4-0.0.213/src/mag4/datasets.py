# requirements
import pandas as pd
import requests
from io import StringIO
import json


# Display the main database content
def display_datasets():
    return pd.read_csv('https://raw.githubusercontent.com/Hezel2000/cosmogeochemdata/master/Dataset_Overview.csv')

# Get a specific database
def get_data(dataset_name, property=None, type=None):
    base_url = 'https://raw.githubusercontent.com/Hezel2000/cosmogeochemdata/master/'
    # The file name here does not allow spaces or other characters
    df_dataset_overview = pd.read_csv(base_url + 'Dataset_Overview.csv')
    fil = (df_dataset_overview['available datasets'] == dataset_name) | (df_dataset_overview['abbreviated name'] == dataset_name)
    db_name = df_dataset_overview[fil]['available datasets'].values[0]

    if property is None:
        # In the following requests is used, as this allows for spacs or other characters in the file name   
        if type is None or type == 'dataframe':
            csv_url = base_url + 'csv/' + db_name + '.csv'
            resp = requests.get(csv_url)
            if resp.status_code == 200:
                return pd.read_csv(StringIO(resp.text))
            else:
                return print('404 – Download failed')
        elif type == 'json':
            return print('to be implemented')
        else:
            return print('type not available')
    elif property is not None:
        json_url = base_url + 'json/' + db_name + '.json'
        resp = requests.get(json_url)
        metadata = json.loads(resp.text)
        if property == 'properties':
            return list(metadata.keys())[:-1]
        # the following property can be combined with the 'type' attribute
        elif property == 'all metadata':
            all_metadata = {key: value for key, value in list(metadata.items())[:-1]}
            if type is None or type == 'dataframe':
                df_all_metadata = pd.DataFrame(list(all_metadata.items()), columns=['Key', 'Value'])
                return df_all_metadata
            elif type == 'json':
                return all_metadata
            else:
                return print('type not available')
        else:
            json_url = base_url + 'json/' + db_name + '.json'
            resp = requests.get(json_url)
            metadata = json.loads(resp.text)
            return metadata[property]


# Convert a csv into a json file with metadata
def write_json_file(file_name, file_path=None, description=None, references=None, source=None, license=None):
    dataset = pd.read_csv(file_path + '/' + file_name + '.csv').dropna().to_dict()

    json_file = {
        "description": description,
        "references": references,
        "dois": dois,
        "source": source,
        "license": license,
        "date": date,
        "version": version,
        "dataset": dataset
    }

    if file_path is not None:
        with open(file_path + '/' + file_name + ".json", "w") as outfile:
            json.dump(json_file, outfile)
    else:
        with open(os.getcwd() + '/' + file_name + ".json", "w") as outfile:
            json.dump(json_file, outfile)

