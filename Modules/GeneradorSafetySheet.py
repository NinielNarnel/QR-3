def getSDS(cas_number):

    # Create a URL template with a placeholder for CAS number
    url_template = "https://www.sigmaaldrich.com/MX/es/search/{cas_placeholder}?focus=products&page=1&perpage=30&sort=relevance&term={cas_placeholder}&type=product"

    # Replace the placeholder with the specified CAS number
    modified_url = url_template.format(cas_placeholder=cas_number)

    # Return the modified URL
    return modified_url