import re
from pprint import pprint
from collections import Counter


with open('tokenization-input-part-A.txt', 'r') as f:
    lines = f.read()

# lines = "RegExr u.s.a was created by gskinner.com, and is proudly hosted by Media Temple. Edit the Expression & Text to see matches. Roll over matches or the expression for details. PCRE & JavaScript flavors of RegEx are supported. Validate your expression with Tests mode.The side bar includes a Cheatsheet, full Reference, and Help. You can also Save & Share with the Community, and view patterns you create or favorite in My Patterns.Explore results with the Tools below. Replace & List output custom results. Details lists capture groups. Explain describes your expression in plain English."
#updated text tokenisation
sen  = re.sub(r'(?<!\d)\.(?!\d)', "", lines) #1(a) revised regular expression with back references
sen = sen.replace("'","") #1(b)
sen = sen.lower() #1(d)
matches = re.findall(r'[^\n\r"_()-/:,!.? ]+', sen) #1(c)

#removing stopwords
with open('stopwords.txt', 'r') as f:
    stopwords = f.read()  
stopwords = stopwords.split()
res = []
for a in matches:
  if a not in stopwords:
    res.append(a)

vowels = ['a', 'e', 'i','o', 'u']

# res= ['stresses','misses', 'gaps', 'jeeps', 'cried', 'ties'] porter stemming step 1a 
# porter stemming step 1a
res2 = []
for i in res:
    k = i
    if(len(i)>3):
        if(i[-1]=='s'):
            if(i[-2] not in vowels and i[-2:] != 'ss'):
                k = i[:-1]
    if(len(i)==4):
        if(i[-3:]=='ies' or i[-3:]=='ied'):
            k = i[:-1]
    if(len(i)>4):
        if(i[-4:]=='sses'):
            k = i[:-2]
        if(i[-3:]=='ies' or i[-3:]=='ied'):
            k = i[:-2]
    res2.append(k)


# res2 = ['agreed', 'goateedly','sauteedly','toupeedly', 'decreedly' ]
# res2 = ['pirating', 'abling', 'hoping']
#porter stemming step 1b
res3 = []
for i in res2:
    k = i
    if(len(i)>3):
        if(i[-3:]=='eed'):
            for j in range(len(i[:-3])):
                if i[j] in vowels:
                    if i[j+1] not in vowels:
                        k = i[:-1]
                        break
    if(len(i)>4):
        if(i[-2:]=='ed'):
            for j in range(len(i[:-2])):
                if i[j] in vowels:
                    k = i[:-2]
                    if(k[-2:]=='at' or k[-2:]=='bl' or k[-2:]=='iz'):
                        k = k + 'e'
                        break
                    elif (k[-1]==k[-2]) and (k[-2:]!='ll' or k[-2:]!='ss' or k[-2:]!='zz'):
                        k = k[:-1]
                        break
                    elif len(k) < 4:
                        k = k + 'e'
                        break
        if(i[-4:]=='edly'):
            for j in range(len(i[:-4])):
                if i[j] in vowels:
                    k = i[:-4]
                    if(k[-2:]=='at' or k[-2:]=='bl' or k[-2:]=='iz'):
                        k = k + 'e'
                        break
                    elif (k[-1]==k[-2]) and (k[-2:]!='ll' or k[-2:]!='ss' or k[-2:]!='zz'):
                        k = k[:-1]
                        break
                    elif len(k) < 4:
                        k = k + 'e'
                        break
        if(i[-3:]=='ing'):
            for j in range(len(i[:-3])):
                if i[j] in vowels:
                    k = i[:-3]
                    if(k[-2:]=='at' or k[-2:]=='bl' or k[-2:]=='iz'):
                        k = k + 'e'
                        break
                    elif (k[-1]==k[-2]) and (k[-2:]!='ll' or k[-2:]!='ss' or k[-2:]!='zz'):
                        k = k[:-1]
                        break
                    elif len(k) < 4:
                        k = k + 'e'
                        break
    if(len(i)>5):
        if(i[-5:]=='eedly'):
            for j in range(len(i[:-5])):
                if i[j] in vowels:
                    if i[j+1] not in vowels:
                        k = i[:-3]
                        break
        if(i[-5:]=='ingly'):
            for j in range(len(i[:-5])):
                if i[j] in vowels:
                    k = i[:-5]
                    if(k[-2:]=='at' or k[-2:]=='bl' or k[-2:]=='iz'):
                        k = k + 'e'
                        break
                    elif (k[-1]==k[-2]) and (k[-2:]!='ll' or k[-2:]!='ss' or k[-2:]!='zz'):
                        k = k[:-1]
                        break
                    elif len(k) < 4:
                        k = k + 'e'
                        break
    res3.append(k)


def first_vowel(s):
    for index, char in enumerate(s):
        if char in 'aeiou':
            return index

# print(lines)
# print(sen)
# print(str(res))
print(str(res3))
# print(words)
# lines = lines.replace(".", "")
# spaces = r"\s+"
# abrv = r"\b(?:[A-Z].[A-Z]*){2,}"

# matches = re.findall(r'(([A-Z][.])+)', lines)
# matches = re.findall(r'([a-zA-Z](\.[a-zA-Z])+)\.', lines)
# sen = re.sub('([a-zA-Z](\.[a-zA-Z])+)\.', r'[a-zA-Z]([a-zA-Z]+)' , lines)