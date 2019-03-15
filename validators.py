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

def validate_input(values, fields):
    err_msg = ""
    for i in range(len(fields)):
        stripped = values[i].strip().strip('"')
        parsed = try_parse_field(fields[i])(stripped)
        if stripped == "":
            err_msg = err_msg + ('"%s" is a required field.\n\n' % fields[i])
        elif parsed == None:
            err_msg = err_msg + ('"%s": %s is not valid.\n\n' % (fields[i], values[i]))
    return err_msg