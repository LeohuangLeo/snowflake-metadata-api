def clean_data_type(data_type: str):
    # Find the index of "("
    index = data_type.find("(")
    
    # If "(" is found, slice to get only the part before it
    if index != -1:
        return data_type[:index]
    return data_type