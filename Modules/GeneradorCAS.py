import requests
import re

def getCAS(cid):
    """Extracts the longest CAS number associated with a specific chemical compound using the PubChem API.

    Args:
        cid (str): The PubChem CID of the compound.

    Returns:
        str: The longest CAS number found or None if none were found.
    """
    # URL to obtain the list of synonyms related to the CID in JSON format
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/JSON"

    # Regular expression to find CAS numbers in any format
    cas_pattern = r'\d{1,5}(?:-\d{1,2}-\d{1,2})?'

    # Initialize a variable to store the longest CAS number found
    longest_cas_number = None

    # Make an HTTP GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        synonyms = data["InformationList"]["Information"][0]["Synonym"]

        # Iterate through the list of related substances and search for CAS numbers
        for synonym in synonyms:
            matches = re.findall(cas_pattern, synonym)
            if matches:
                for match in matches:
                    if longest_cas_number is None or len(match) > len(longest_cas_number):
                        longest_cas_number = match

        return longest_cas_number

    return None