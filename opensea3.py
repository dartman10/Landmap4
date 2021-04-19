import requests
import json
import re
import pandas as pd

from pprint import pprint


API_URL = "https://api.opensea.io/api/v1/assets"
OUTPUT_FILE = "data/assets.json"

# For a key inside another key, put a space between key names.
KEYS = [
    "name",
    #"permalink",
    #"asset_contract address",
    #"external_link",
    "traits"
    #"owner address",
    #"sell_orders"
]

n = 0
land_assets = []
try:
    # Reads through 50 queries at a time
    #while True:                                # dartman : comment out for testing only, to limit loops
        querystring = {
            "order_direction": "desc",
            "limit": "49",
            "offset": str(n),
            "token_ids": "22073",   # temporary, for single land testing
            "asset_contract_address":"0x50f5474724e0ee42d9a4e711ccfb275809fd6d4a"  # SandBox Land
        }

        response = requests.request("GET", API_URL, params=querystring)

        # Loop through each asset (as a dict)
        for asset in json.loads(response.text)["assets"]:
            land_assets.append(asset)

        n += 50
except:
    pass

# This will be filled with asset information that matches with the keys
bare_assets = []

split_keys = [k.split(" ") for k in KEYS]

for asset in land_assets:
    # Asset for the bare_assets list
    bare_asset = {}

    for fields in split_keys:
        current = asset[fields[0]]

        # Loops through each key in the fields
        for f in fields[1:]:
            current = current[f]

        new_key = "_".join(fields)
        bare_asset[new_key] = current

    bare_assets.append(bare_asset)

json_objects = json.loads(json.dumps(bare_assets))

with open(OUTPUT_FILE, "w") as json_file:
    json.dump(json_objects, json_file)

df_01 = pd.read_json(OUTPUT_FILE)

print('=======================')
print('SIZE = ', df_01.size)
print('=======================')
print('HEAD = ', df_01.head())
print('=======================')
print('TRAITS = ', df_01.traits)
print('=======================')

df_01 = df_01.loc[:, 'traits']
print('df_01[0] = ', df_01[0])

df_02 = pd.DataFrame(df_01[0])
print('----------------------------------')
df_02.set_index('trait_type', inplace=True)  # set index to column trait_type
print('----------------------------------')
print('df_02 follows')
print(df_02)
print('----------------------------------')
y = (df_02.loc[['y'],['value']])
yy = y.values[0]
yy = y.values[0]
print('y = ', yy[0])
print('----------------------------------')
x = (df_02.loc[['x'],['value']])
xx = x.values[0]
yxx = x.values[0]
print('x = ', xx[0])


# Generate this javascript line:
#  x = aValue; y = aValue; sandboxLink = aValue; drawbox(x,y);

# To load an api url result directly into a Dataframe
# url = "https://api.exchangerate-api.com/v4/latest/USD"
# df = pd.read_json(url)
