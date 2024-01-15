import requests

def getFormula(user_cid):
    # Create a URL template with a placeholder for CID
    url_template = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{placeholder}/property/MolecularFormula/JSON"

    # Replace the placeholder with the specified CID
    modified_url = url_template.format(placeholder=user_cid)

    # Make an HTTP GET request to the URL
    response = requests.get(modified_url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract the molecular formula from the response data
        molecular_formula = data["PropertyTable"]["Properties"][0]["MolecularFormula"]
        return molecular_formula
    else:
        return "N/A"

def getName(user_cid):
    # Create a URL template with a placeholder for CID
    url_template = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{placeholder}/property/Title/JSON"

    # Replace the placeholder with the specified CID
    modified_url = url_template.format(placeholder=user_cid)

    # Make an HTTP GET request to the URL
    response = requests.get(modified_url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract the name from the response data
        name = data["PropertyTable"]["Properties"][0]["Title"]
        return name
    else:
        return "N/A"
