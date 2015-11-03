import numpy as np
import scipy.cluster.hierarchy as hr
import scipy.spatial as spa
import clustering
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
import filter

class textMiningEac:
    def __init__(self,k,N,low,high=0):
        self.k = k

        # Leer datos desde archivo [Temporal]
        #data = np.genfromtxt('iris.data',delimiter=',')
        #temp= spa.distance.pdist(data,'euclidean')
        #self.D = spa.distance.squareform(temp)
        
        self.D,self.tweets,self.words,self.freq = filter.filtertweets()

        # Calcula la matriz de coasociacion
        self.loadEAC(N,low,high)       

    def loadEAC(self,N,low,high=0):
        """
        Genera de vuelta la matriz de coasociacion
        """
        m,n = self.D.shape
        coasocMatrix = clustering.EAC(self.D,N,low,high)
        print(coasocMatrix)
        self.EAC_D = np.ones(n) - coasocMatrix
            
    def startPAM(self):
        """
        Hace sobre PAM sobre la matriz de distancia del EAC
        """
        (a,b,self.labels) = clustering.PAM(self.EAC_D, self.k,True)	
        return self.labels

    def startHierarchical(self):
        """
        Hace clustering Jerarquico sobre la matriz de distancia del EAC
        """
        z = AgglomerativeClustering(n_clusters=self.k, linkage='ward').fit(self.EAC_D)
        self.labels = z.labels_	
        return self.labels
    
    def getClustersTweets(self):
        """
        Obtiene clusters en relacion a la frecuencia de aparicion de las palabras
        """
        labelsTweets = np.zeros(len(self.tweets),dtype=np.int)
        for i in range(len(self.tweets)):           
            
            acum = np.zeros(2)
            for j in range(len(self.labels)):
                
                # Si la palabra se encuentra en el tweet
                if(self.words[j] in self.tweets[i]):    
                    #Acumula el valor en el acumulador del indice del cluster
                    acum[self.labels[j]] += self.freq[j]  
                
            # Asigna el cluster con mayor valor acumulado
            labelsTweets[i] = np.argmax(acum)
        
        lista = labelsTweets.tolist()
        
        try:        
            saveFile = open('clustered.csv','w')        
            for i in range(len(self.tweets)):
                saveFile.write(str(lista[i])+': '+' '.join(self.tweets[i])+'\n')
            saveFile.close()
        except Exception as e:
            print("error: {0}".format(e))
            
        return labelsTweets

    def getPrecisionIris(self):		
        """
        Metodo de prueba
        Calcula una precision de acierto. No es fiable. 
        """
        
        #Lee los cluster originales
        originalClusters = np.genfromtxt('orCL.data',delimiter=',',dtype=None)
        
        results ={}
        
        j=0
        for i in range(50,151,50):
                # Encuentra el cluster con mayor frecuencia
                unique, counts = np.unique(self.labels[i-50:i], return_count=True)
                print(unique)
                print(counts)
                maxvalue = np.amax(counts)
                results[j]=maxvalue/50
                j=j+1
                
        print("Setosa= " + '%.2f' % results[0] + "\nVersicolor= " + '%.2f' % results[1] + "\nVirginica= " + '%.2f' % results[2])
        
    def getSilhouette(self):
        """
        Grafica silhouette
        """
        clustering.Silhouette(self.D,self.labels,self.k)