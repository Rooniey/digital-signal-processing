def try_float(s):
    try: return float(s)
    except ValueError: 
        return None

def try_int(s):
    try: return int(s)
    except ValueError: 
        return None

def try_parse_field(field):
    if(field == 'n'):
        return try_int
    return try_float

def validate_input(fieldValues):
    err_msg = ""
    parsedValues = {}
    for k, v in fieldValues.items():
        stripped = v.strip().strip('"')
        parsedValues[k] = try_parse_field(k)(stripped)
        if stripped == "":
            err_msg = err_msg + ('"%s" is a required field.\n\n' % k)
        elif parsedValues[k] == None:
            err_msg = err_msg + ('"%s": %s is not valid.\n\n' % (k, v))
    return (err_msg, parsedValues)