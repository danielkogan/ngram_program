import nltk
import codecs
f=codecs.open("train.txt","r","utf_8_sig")
    
dct={}
while True:
    fd=f.readline()
    fd=fd.lower()
    if len(fd)==0:
        break
    token=nltk.word_tokenize(fd)

    """"ngram length"""
    n=3
    lang=token[0]
    """all ngrams in current read line"""
    line_ngrams=[]
    for n in [2,3,4]:
        for g in range(1, len(token),1):
            
            generated_ngrams = nltk.ngrams(token[g], n, pad_left=True, pad_right=True, pad_symbol=' ')
            ls=list(generated_ngrams)
            ln=len(ls)
            
            for i in range(len(ls)):
                a=''
                for k in ls[i]:
                    a+=k
                """print(a)"""
                line_ngrams.append(a)
                
        if lang in dct.keys():
            for i in line_ngrams:
                if i in dct[lang].keys():
                    dct[lang][i]+=1
                else:
                    dct[lang][i]=1
        else:
            dct[lang]={}
            for j in line_ngrams:
                if j in dct[lang].keys():
                    dct[lang][j]+=1
                else:
                    dct[lang][j]=1
    """print(dct)"""
    
f.close()
print(len(dct['en']))
print(dct.keys())

from collections import OrderedDict
r={}
for i in dct.keys():
    r[i]=list(OrderedDict(sorted(dct[i].items(), key=lambda x: x[1], reverse=True)))
    """OrderedDict returns dct2 sorted by value, list() returns list of OrderedDict's keys"""

r_short={}
for i in dct.keys():
    r_short[i]=r[i][1:300:1]
    
f1=codecs.open("test.txt","r","utf_8_sig")
f2=codecs.open("output.txt","w","utf_8_sig")
for yy in f1.readlines():
    rl=yy
    rl=rl.lower()
    wtokens=nltk.word_tokenize(rl)
    test_ngr=[]

    for g in range(0, len(wtokens)):
        for j in [2,3,4]:
            generated_ngrams = nltk.ngrams(wtokens[g], j, pad_left=True, pad_right=True, pad_symbol=' ')
            ls=list(generated_ngrams)
            
            for i in range(len(ls)):
                a=''
                for k in ls[i]:
                    a+=k    
                test_ngr.append(a)
    M=len(test_ngr)
    test_dict={}
    for i in test_ngr:
        test_dict[i]=test_ngr.count(i)
    test_dict_sorted=list(OrderedDict(sorted(test_dict.items(), key=lambda x: x[1], reverse=True)))

    mx=999999999999
    lng=''
    for language in r_short.keys():
        
        sm=0   
        for i in test_dict_sorted:
            
            if i in r_short[language]:
                sm+=abs(test_dict_sorted.index(i)-r_short[language].index(i))
            else:
                sm+=M
        if mx>=sm:
            
            mx=sm
            lng=language
    
    f2.write(lng.upper()+'\n')
f1.close()
f2.close()
