#importing software libraries
import re
from collections import Counter
import matplotlib.pyplot as plt



# lines = "RegExr u.s.a was created by gskinner.com, and is proudly hosted by Media Temple. Edit the Expression & Text to see matches. Roll over matches or the expression for details. PCRE & JavaScript flavors of RegEx are supported. Validate your expression with Tests mode.The side bar includes a Cheatsheet, full Reference, and Help. You can also Save & Share with the Community, and view patterns you create or favorite in My Patterns.Explore results with the Tools below. Replace & List output custom results. Details lists capture groups. Explain describes your expression in plain English."
# 1. tokenisation
def tokenization(lines):
    sen  = re.sub(r'(?<!\d)\.(?!\d)', "", lines) #1(a) revised regular expression with back references // fixes all the abbrevations
    # sen  = re.sub(r'(([a-z]\.){2,})+', "", lines)
    sen = sen.replace("'","") #1(b) // removing apostrophes to keep all the contractions together
    sen = sen.lower() #1(d) //lowercase all the letters before tokenizing the document
    matches = re.findall(r'[^\n\r"_()-/:;,!.? ]+', sen) #1(c) //removes all the possible punctuations from the document, treating them as word seperators
    return matches 

# 2. removing stopwords
def stop_word_removal(matches):
    with open('stopwords.txt', 'r') as f:
        stopwords = f.read()  
    stopwords = stopwords.split() #stopword list given to us
    res = []
    for a in matches:
        if a not in stopwords: #ensuring our tokenised word is not a stopword 
            res.append(a)
    return res


# 3. Implementing first two steps of porter stemming
def porter_stemming(res):
    vowels = ['a', 'e', 'i','o', 'u']
    # res= ['stresses','misses', 'gaps', 'jeeps', 'cried', 'ties']  
    # res= ['feeding', 'being', 'doing', 'going', 'oping','sing'] 
    # res = ['hundred']
    # porter stemming step 1a
    res2 = []
    for i in res:
        k = i
        if(len(i)>3): 
            if(i[-1]=='s'): # gaps-> gap, stress -> stress
                for j in i[:-2]:
                    if(j in vowels and i[-2:] != 'ss'):
                        k = i[:-1]
        if(len(i)==4): # ties -> tie, cries-> cri
            if(i[-3:]=='ies' or i[-3:]=='ied'):
                k = i[:-1]
        if(len(i)>4):
            if(i[-4:]=='sses'): # stresses -> stress, misses -> miss
                k = i[:-2]
            if(i[-3:]=='ies' or i[-3:]=='ied'): # ties -> tie, cries-> cri
                k = i[:-2]
        res2.append(k)


    # res2 = ['agreed', 'goateedly','sauteedly','toupeedly', 'decreedly' ]
    # res2 = ['stressing', 'falling', 'hoping', 'sled', 'medly', 'falling']
    # res2 = ['whales']
    #porter stemming step 1b
    res3 = []
    for i in res2:
        k = i
        if(len(i)>3):
            if(i[-3:]=='eed'): # agreed -> agree, feed -> feed
                for j in range(len(i[:-3])):
                    if i[j] in vowels:
                        if i[j+1] not in vowels:
                            k = i[:-1]
                            break
        if(len(i)>4):
            if(i[-2:]=='ed'): # pirated -> pirate, sled -> sled
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
            if(i[-4:]=='edly'): # medly -> medly, supposedly -> suppose, 
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
            if(i[-3:]=='ing'): # pirating -> pirate, sing -> sing, falling  -> fall, dripping -> drip, hoping -> hope
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
            vocablen.append(count) #appending vocab count when it increases
        else:
            vocablen.append(count) #appending vocab count even when it doesnt increase 
        wordslen.append(i) #appending each timestamp to record increase in total words
    print(plt.plot(wordslen, vocablen))
    plt.show()

#main control of PART A
def parta():

    #opening input text file
    with open('tokenization-input-part-A.txt', 'r') as f:
        lines = f.read()
    # lines =" U.S.A. 92.3 hoping pha.r.ma" #defects

    #tokenization, stop-word removal, stemming
    matches = tokenization(lines)
    poststop = stop_word_removal(matches)
    poststem = porter_stemming(poststop)
    print(poststem)

    #writing results to text file
    file1 = open("tokenized.txt","w")
    for i in poststem:
        file1.write(i +"\n")
    file1 = open("tokenized.txt","r+") 
    return poststem

#main control of PART B
def partb():

    #opening input text file
    with open('tokenization-input-part-B.txt', 'r') as f:
        lines = f.read()
    
    #tokenization, stop-word removal, stemming
    matches = tokenization(lines)
    poststop = stop_word_removal(matches)
    poststem = porter_stemming(poststop)

    #most common words generation 
    track = Counter(poststem)
    mostcommon = track.most_common(300)

    
    #writing results to text file
    l = []
    file = open("terms.txt","w")
    for i in mostcommon:
        file.write(i[0]+ " " + str(i[1]) + "\n")
        l.append(i[0])
    l.sort()
    print(l)
    file = open("terms.txt","r+") 

    #graphing vocabulary growth
    graph = vocab_graph(poststem)
    return mostcommon

if __name__ == "__main__":
    parta()
    partb()






