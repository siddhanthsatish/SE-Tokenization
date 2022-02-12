#importing software libraries
import re
from collections import Counter
import matplotlib.pyplot as plt


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
    plt.plot(wordslen, vocablen)
    plt.show()

#main control of PART A
def parta():
    
    #opening input text file
    with open('tokenization-input-part-A.txt', 'r') as f:
        lines = f.read()

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

def unit_tests():
    # small example taken here to show the the testing of the code
    assert tokenization('My name is S.E.I.N.F.E.L.D. I am a Comedian.') == ['my', 'name', 'is', 'seinfeld', 'i', 'am', 'a', 'comedian'], "should be ['my', 'name', 'is', 'seinfeld', 'i', 'am', 'a', 'comedian']"
    assert tokenization('Seinfeld has 200,000,000 dollars.') == ['seinfeld', 'has', '200','000', '000', 'dollars'], "should be ['seinfeld', 'has', '200','000', '000', 'dollars']"
    print('Tokenization Works!')

    assert stop_word_removal(['my', 'name', 'is', 'seinfeld', 'i', 'am', 'a', 'comedian']) == ['name', 'seinfeld', 'comedian'], "should be ['name', 'seinfeld', 'comedian']"
    assert stop_word_removal(['seinfeld', 'has', '200','000', '000', 'dollars']) == ['seinfeld', '200', '000', '000', 'dollars'], "should be ['seinfeld', '200', '000', '000', 'dollars']"
    print('Stopword Removal Works!')

    assert porter_stemming(['name', 'seinfeld', 'comedian']) == ['name', 'seinfeld', 'comedian'], "should be ['name', 'seinfeld', 'comedian']]"
    assert porter_stemming(['seinfeld', '200', '000', '000', 'dollars']) == ['seinfeld', '200', '000', '000', 'dollar'], "should be ['seinfeld', '200', '000', '000', 'dollars']"
    print('Stemming Works!')
    

if __name__ == "__main__":
    print('PART A Results -->')
    parta()
    print('PART B Results -->')
    partb()
    unit_tests() 

