import re
from pprint import pprint


# with open('mdb.txt', 'r') as f:
#     lines = f.read()
#     words = lines.split(' ')
lines = "Hi there it's me! CONAN and C.O.N.A.N. is here."
spaces = r"\s+"
abrv = r"\b(?:[A-Z].[A-Z]*){2,}"

matches = re.findall(r'(([A-z][.])+)', lines)

print(matches)
    

# print(words)