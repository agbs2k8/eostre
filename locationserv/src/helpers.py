def drop_null_keys(obj):
    """Remove keys with None or empty list values from a dictionary"""
    return {key:value for key, value in obj.items() if value not in [None, []]}