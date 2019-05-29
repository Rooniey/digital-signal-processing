pluck = lambda d, *args: (d[arg] for arg in args)

def try_get(dict, key):
  try:
    return dict[key]
  except KeyError:
    return False