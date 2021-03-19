
def id_in_response(response:dict, has_site_id:bool=False):
    """Check if there is an \"id\" property with \"uuid\" and optionally 
    \"site\" sub-properties in the response dict""" 
    id_keys = {"uuid"}
    if has_site_id:
        id_keys.add("site")
    
    return (
        "id" in response.keys() and
        id_keys.issubset(response["id"].keys())
    )
