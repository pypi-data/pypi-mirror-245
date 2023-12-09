# requirements
import pandas as pd

base_url = 'https://raw.githubusercontent.com/Hezel2000/cosmogeochemdata/master/'

# Display the main database content
def display_databases():
    return pd.read_csv(base_url + 'GCCdata.csv')

def add_one(a):
    return a + 1