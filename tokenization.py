import re
from pprint import pprint
from collections import Counter


with open('tokenization-input-part-A.txt', 'r') as f:
    lines = f.read()

# lines = "RegExr u.s.a was created by gskinner.com, and is proudly hosted by Media Temple. Edit the Expression & Text to see matches. Roll over matches or the expression for details. PCRE & JavaScript flavors of RegEx are supported. Validate your expression with Tests mode.The side bar includes a Cheatsheet, full Reference, and Help. You can also Save & Share with the Community, and view patterns you create or favorite in My Patterns.Explore results with the Tools below. Replace & List output custom results. Details lists capture groups. Explain describes your expression in plain English."

sen  = re.sub(r'(?<!\d)\.(?!\d)', "", lines) #1(a) revised regular expression with back references
sen = sen.replace("'","") #1(b)
sen = sen.lower() #1(d)
matches = re.findall(r'[^\n\r"_()-/:,!.? ]+', sen) #1(c)

with open('stopwords.txt', 'r') as f:
    stopwords = f.read()
    
stopwords = stopwords.split()
# # print(stopwords)
# res = list((Counter(matches)-Counter(stopwords)).elements())

res = []
for a in matches:
  if a not in stopwords:
    res.append(a)

# print(lines)
# print(sen)
print(str(res))
# print(words)
# lines = lines.replace(".", "")
# spaces = r"\s+"
# abrv = r"\b(?:[A-Z].[A-Z]*){2,}"

# matches = re.findall(r'(([A-Z][.])+)', lines)
# matches = re.findall(r'([a-zA-Z](\.[a-zA-Z])+)\.', lines)
# sen = re.sub('([a-zA-Z](\.[a-zA-Z])+)\.', r'[a-zA-Z]([a-zA-Z]+)' , lines)