import re
from pprint import pprint
from collections import Counter
import matplotlib.pyplot as plt



# lines = "RegExr u.s.a was created by gskinner.com, and is proudly hosted by Media Temple. Edit the Expression & Text to see matches. Roll over matches or the expression for details. PCRE & JavaScript flavors of RegEx are supported. Validate your expression with Tests mode.The side bar includes a Cheatsheet, full Reference, and Help. You can also Save & Share with the Community, and view patterns you create or favorite in My Patterns.Explore results with the Tools below. Replace & List output custom results. Details lists capture groups. Explain describes your expression in plain English."
#updated text tokenisation
def tokenization(lines):
    sen  = re.sub(r'(?<!\d)\.(?!\d)', "", lines) #1(a) revised regular expression with back references
    sen = sen.replace("'","") #1(b)
    sen = sen.lower() #1(d)
    matches = re.findall(r'[^\n\r"_()-/:,!.? ]+', sen) #1(c)
    return matches 

#removing stopwords
def stop_word_removal(matches):
    with open('stopwords.txt', 'r') as f:
        stopwords = f.read()  
    stopwords = stopwords.split()
    res = []
    for a in matches:
        if a not in stopwords:
            res.append(a)
    return res

def porter_stemming(res):
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
    # res2 = ['stressing', 'falling', 'hoping']
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
                        elif (k[-1]==k[-2]) and k[-2:]!='ll' and k[-2:]!='ss' and k[-2:]!='zz':
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
                        elif (k[-1]==k[-2]) and k[-2:]!='ll' and k[-2:]!='ss' and k[-2:]!='zz':
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
                        elif (k[-1]==k[-2]) and k[-2:]!='ll' and k[-2:]!='ss' and k[-2:]!='zz':
                            k = k[:-1]
                            break
                        elif len(k) < 4:
                            k = k + 'e'
                            break
        res3.append(k)
    return res3
    
def vocab_graph(matches):
    count = 0
    vocablen = []
    wordslen = []
    vocab = set()
    for i in range(len(matches)):
        if(matches[i] not in  vocab):
            vocab.add(matches[i])
            count += 1
            vocablen.append(count)
        else:
            vocablen.append(count)
        wordslen.append(i)
    print(plt.plot(wordslen, vocablen))
    plt.show()

def parta():
    #main control of PART A
    with open('tokenization-input-part-A.txt', 'r') as f:
        lines = f.read()
    matches = tokenization(lines)
    poststop = stop_word_removal(matches)
    poststem = porter_stemming(poststop)
    file1 = open("tokenized.txt","w")
    for i in poststem:
        file1.write(i +"\n")
    file1 = open("tokenized.txt","r+") 
    # print(file1.read())

def partb():
    #main control of PART B
    with open('tokenization-input-part-B.txt', 'r') as f:
        lines = f.read()

    matches = tokenization(lines)
    poststop = stop_word_removal(matches)
    poststem = porter_stemming(poststop)
    track = Counter(poststem)
    mostcommon = track.most_common(300)
    print(mostcommon)
    file = open("terms.txt","w")
    for i in mostcommon:
        file.write(i[0]+ " " + str(i[1]) + "\n")
    file = open("terms.txt","r+") 
    graph = vocab_graph(poststem)

if __name__ == "__main__":
    parta()
    partb()









