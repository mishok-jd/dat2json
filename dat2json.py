import tokenize
import token
import json
from StringIO import StringIO
import os

# dat2json source code

# get cwd
cwd = os.getcwd()

# fixlazyjson
def fixLazyJson (in_text):
  tokengen = tokenize.generate_tokens(StringIO(in_text).readline)

  result = []
  for tokid, tokval, _, _, _ in tokengen:
    # fix unquoted strings
    if (tokid == token.NAME):
      if tokval not in ['true', 'false', 'null', '-Infinity', 'Infinity', 'NaN']:
        tokid = token.STRING
        tokval = u'"%s"' % tokval

    # fix single-quoted strings
    elif (tokid == token.STRING):
      if tokval.startswith ("'"):
        tokval = u'"%s"' % tokval[1:-1].replace ('"', '\\"')

    # remove invalid commas
    elif (tokid == token.OP) and ((tokval == '}') or (tokval == ']')):
      if (len(result) > 0) and (result[-1][1] == ','):
        result.pop()

    # fix single-quoted strings
    elif (tokid == token.STRING):
      if tokval.startswith ("'"):
        tokval = u'"%s"' % tokval[1:-1].replace ('"', '\\"')

    result.append((tokid, tokval))

  return tokenize.untokenize(result)

# opening .dat file
datmap = param1 + ".dat"

def json_decode (json_string, *args, **kwargs):
  try:
    json.loads (json_string, *args, **kwargs)
  except:
    json_string = fixLazyJson (json_string)
    json.loads (json_string, *args, **kwargs)

datmap_fixed = json_decode(datmap)

# save .json file
with open(param1 + '.json', 'w') as f:
    json.dump(datmap_fixed, f, sort_keys=True, indent=2)
