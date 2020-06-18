import requests
import json
import time
from bs4 import BeautifulSoup

from schema import Schema, And, Use, Optional, Regex
import schemas

URL = "https://quantamixsolutions.com/blog/65/how-to-turn-your-website-into-an-organic-growth-machine"
URL_TIMEOUT = 10.0

def get_data(address):
    """
    A function that takes a url as input, finds all the wanted scripts in the html source and returns them
    in json format
    """
    try:
        # Make get request for address
        result = requests.get(address, timeout = URL_TIMEOUT)

        # Retrieve source code and keep only the <script> with correct type tags
        src = result.content
        soup = BeautifulSoup(src, "html.parser")
        scripts = soup.find_all("script", type = "application/ld+json")

        # Transform string to json format
        for i in range(len(scripts)):
            scripts[i] = json.loads(scripts[i].string, strict = False)
        return scripts   
    except:
        return None

def validate_data(data):
    results = {"errors": 0, "wrong/unknown type": 0}
    for i in range(len(data)):
        if data[i]["@type"] not in schemas.all_schemas.keys() or "@type" not in data[i].keys():
            print(f"Script #{i} has a wrong/unknown type")
            results["wrong/unknown type"] += 1
            continue
        validated = schemas.all_schemas[data[i]["@type"]].is_valid(data[i])
        if validated:
            if data[i]["@type"] not in results.keys():
                results[data[i]["@type"]] = 1
            else:
                results[data[i]["@type"]] += 1
        else:
            results["errors"] += 1
        print(f"Script #{i} of type {data[i]['@type']} validates {validated}")
    return results

if __name__ == "__main__":
    data = get_data(URL)

    if data == None:
        print("Something went wrong with the connection")
    else:
        start_time = time.time()
        result = validate_data(data)
        print(f"Time: {time.time() - start_time}")
        print(result)
