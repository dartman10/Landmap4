import requests
import json
import re

from pprint import pprint


API_URL = "https://api.opensea.io/api/v1/assets"
OUTPUT_FILE = "data/assets.json"

# For a key inside another key, put a space between key names.
KEYS = [
    "name",
    "asset_contract address"
]


n = 0
land_assets = []
try:
    # Reads through 50 queries at a time
    while True:
        querystring = {
            "order_direction": "desc",
            "limit": "49",
            "offset": str(n),
            "collection": "sandbox"
        }

        response = requests.request("GET", API_URL, params=querystring)

        # Loop through each asset (as a dict)
        for asset in json.loads(response.text)["assets"]:
            # REGEX: LAND (xx, yy)
            if re.search("^[LAND \(].*,.*\)$", asset["name"]):
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
