import sys
from pathlib import Path

# default arguments
arg1, arg2 = "README.ipynb", "README.md"

# read arguments from command line if any is given
if len(sys.argv) > 1 :
  arg1 = sys.argv[1]
  if len(sys.argv) == 3: arg2 = sys.argv[2]
  else: arg2 = Path(arg1).with_suffix('.md')

# scan ipynb file (json format), process markdown parts
with open(arg2, 'w') as outfile, open(arg1, 'r') as infile:
  state = 'outside markdown'
  for line in infile:
    if line[-2] == ']' and state == 'in markdown': state = 'outside markdown'
    if state == 'in markdown':
      if   line[-5:-1] == '\\n",': line = line.lstrip()[1:-5].rstrip() + '\n'
      elif line[-4:-1] == '\\n"':  line = line.lstrip()[1:-4].rstrip() + '\n'
      elif line[-2] == '"':        line = line.lstrip()[1:-2].rstrip() + '\n'
      line = line.replace('\\"', '"') # change all \" to "
      outfile.write(line)

    if 'markdown' in line and state == 'outside markdown': state = 'markdown seen'
    if   'source' in line and state ==    'markdown seen': state = 'in markdown'
