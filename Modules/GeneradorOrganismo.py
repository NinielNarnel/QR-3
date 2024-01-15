import requests

def getOrganism(user_cid):
    # Create a URL template with a placeholder for CID
    url_template = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{placeholder}/record/JSON"

    # Replace the placeholder with the specified CID
    modified_url = url_template.format(placeholder=user_cid)

    # Make an HTTP GET request to the URL
    response = requests.get(modified_url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract the name from the response data
        name = data["Record"]["RecordTitle"]

        # Extract the organism source name list
        source_name_list = data["Record"]["Section"][0]["Section"][0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]

        return f"{name} is a natural product found in {source_name_list}"
    else:
        return "N/A"