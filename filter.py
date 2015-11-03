import scipy.spatial as spa
import numpy as np
import re
from unicodedata import normalize
from collections import defaultdict

def filtertweets():  

    # Leer tweets
    tweets = open("tweets.csv").read().splitlines()

    # Limpiar tweets
    for i in range(len(tweets)):
        tweets[i] = clean(tweets[i]) 
        
    # Remover repetidos
    seen = set()
    cleaned = []
    for item in tweets:
        if item not in seen:
            seen.add(item)
            cleaned.append(item)
            
    #Remover articulos,pronombres y preposiciones
    for i in range(len(cleaned)):
        cleaned[i] = removerArtProPre(cleaned[i])

    # Remover palabras menos usadas
    total = 0
    d = defaultdict(int)
    for tweet in cleaned:
        for word in tweet:
            d[word] += 1
            total += 1
            
    freq_ord = [(word,count) for word, count in sorted(d.items(),key=lambda k_v: (k_v[1], k_v[0]),reverse=True)]

    wordsFiltered = []
    freqFiltered = []

    for i in range(len(freq_ord)):    
        if( freq_ord[i][1]/total <0.0005 ):        
            wordsFiltered = [x[0] for x in freq_ord[:i]]
            freqFiltered = [x[1] for x in freq_ord[:i]]
            break
            
    for i in range(len(cleaned)):        
        cleaned[i] = [x for x in cleaned[i] if x in wordsFiltered]    
        
        
    try:        
        saveFile = open('filtered.csv','w')        
        for tw in cleaned:            
            saveFile.write(' '.join(tw)+'\n')
        saveFile.close()
    except Exception as e:
        print("error: {0}".format(e))        
      
    D = matrizDistancia(cleaned,wordsFiltered)
    
    return  D,cleaned,wordsFiltered,freqFiltered


# TODO reescribir        
def matrizDistancia(tweets,words):    
    n=len(words)
    D = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if(i != j):
                cantConjunta = 0
                cantAparI = 0
                
                for tweet in tweets:
                    if(words[i] in tweet):
                        cantAparI += 1
                        if(words[j] in tweet):
                            cantConjunta +=1
                
                D[i,j] = cantConjunta/cantAparI
    return D
                

def clean(text):
    
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')
    #Remover url, RT y Menciones(@)
    text = re.sub(r"(RT)|((@[_A-Za-z0-9]+))|(\w+:\/\/\S+)", "", text)   
    
    #Remover caracteres extraños
    result = []
    for word in _punct_re.split(text.lower()):        
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        word = word.decode('utf-8')
        if word:            
            result.append(word)    
    return ' '.join(result)
    

def removerArtProPre(text):
    preposiciones = ['a','ante','bajo','con','contra','de','desde','durante',
                     'en','entre','hacia','hasta','mediante','para','por','segun',
                     'sin','sobre','tras']    
    
    articulos = ['el','la','los','las','un','una','unos','unas','lo','al','del']
    
    pronombres = ['yo','mi','conmigo','tu','vos','usted','ti','contigo','el','ella',
                  'ello','si','consigo','nosotros','nosotras','ustedes','ellos',
                  'ellas','si','consigo','vosotros','vosotras','me','nos','te','se',
                  'os','lo','la','le','los','las','les','mio','mia','mios','mias',
                  'tuyo','tuya','tuyos','tuyas','suyo','suya','su','suyas','suyos',
                  'nuestro','nuestra','nuestras','nuestros','vuestro','vuestros',
                  'vuestra','vuestras','suyo','suya','suyos','suyas','este','esta',
                  'esto','estos','estas','ese','esa','eso','esos','esas','aquel',
                  'aquella','aquello','aquellas','aquellos','que','cual','cuales',
                  'donde','quien','como','quienes','cuyo','cuyos','cuanto','cuanta',
                  'cuantos','cuantas','bastante','alguno','cualquiera','nadie',
                  'ninguno','otro','quienquiera']
    varios = ['y','es','no','va','q','x','era']
              
    filtro = set(preposiciones+articulos+pronombres+varios)    
    
    result = []
    for word in text.split(' '):
        if(word not in filtro):
            result.append(word)
    return result

