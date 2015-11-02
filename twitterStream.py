from twython import TwythonStreamer

class MyStreamer(TwythonStreamer):
    cant = 1
    _count = 0
    tweets = []
    def on_success(self, data): 
        self._count = self._count + 1 
        if 'text' in data:
            tweet = ' '.join(data['text'].splitlines())
            print (tweet)
            self.tweets.append(tweet)
        if (self._count == self.cant):
            self.disconnect()

    def on_error(self, status_code, data):
        print (status_code)
        self.disconnect()        
        
def startStream(termino,cant):
    """
    termino: palabra a filtrar
    cant: cantidad maximas de tweets a buscar
    """
    # Necesita un archivo txt que contenga en la primera linea la clave Consumer Key, 
    # en la segunda Consumer Secret, tercera Access Token y cuarta Access Token Secret
    keys = open("TwitterKeys.txt").read().splitlines()    
    stream = MyStreamer(keys[0],keys[1],keys[2],keys[3])
    
    stream.cant = cant
    stream.statuses.filter(track=termino)
    
    #Escribe los archivos al disco
    try:        
        saveFile = open('tweets.csv','w')        
        for tweet in stream.tweets:            
            saveFile.write(tweet+'\n')
        saveFile.close()
    except Exception as e:
        print("error: {0}".format(e))

