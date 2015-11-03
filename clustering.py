import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import matplotlib.cm as cm

def EAC(D, N, low,high):
    """Do Evidence Accumulation Clustering
    D= Matriz de distancia
    N= Numero de clusterings
    kinterval= Intervalo del cual elejir los k cluster aleatorios	
    Devuelve matriz de coasociacion
    """		
    
    # Obtener dimensiones
    m,n = D.shape
    
    matrizCoAsoc = np.zeros((n, n))
    
    for i in range(N):		
        # Elije valor aleatorio k entre low y high
        if(high != 0):
            k = np.random.randint(low,high)
        else: 
            k = low
        
        # Ejecuta PAM
        resultadosPam = PAM(D,k)		
        clusters = resultadosPam[1]		
        
        # Actualiza la matriz de co-asociación		
        for j in range(k):	
            for row in clusters[j]:				
                for column in clusters[j]:
                    if(row!=column):
                        matrizCoAsoc[row][column] = matrizCoAsoc[row][column] + 1/N
                    else:
                        matrizCoAsoc[row][column]=1
    
    return matrizCoAsoc	
	

def PAM(D, k, return_labels=False,tmax = 100):	
    """Do Partitioning Around Medoids
    D= Matriz de distancia
    k= Numero de clusters
    tmax= Numero maximo de iteraciones	
    """

    # Obtener dimensiones
    m,n = D.shape

    # Generar array de k indices aleatorios de medoides sin reposicion
    IndicesMedioides = np.sort(np.random.choice(n,k,False))	

    NuevoIndicesMedioides = np.copy(IndicesMedioides)

    Clusters = {}

    labels = []

    # Itera hasta tmax veces o hasta que converja
    for t in range(tmax):
            
        # Devuelve un array de tamaño n, donde el valor de cada uno es el índice del medioide mas cercano
        labels= np.argmin(D[:,IndicesMedioides], axis = 1)	
        
        # Utiliza los valores en labels para reorganizarlos en k clusters
        for i in range(k):
                Clusters[i] = np.where(labels==i)[0]
        
        # Actualiza los mediodes si el costo promedio de un elemento es menor que el existente
        for i in range(k):
            L = np.mean(D[np.ix_(Clusters[i],Clusters[i])],axis=1)	
            
            # Si el cluster esta vacio se deja el indice existente
            if (Clusters[i].size != 0):                
                j = np.argmin(L)
                NuevoIndicesMedioides[i] = Clusters[i][j]
            else:
                print(IndicesMedioides)
                print(Clusters)
                NuevoIndicesMedioides[i] = IndicesMedioides[i]
                
        np.sort(NuevoIndicesMedioides)
        
        # Verifica si converge 
        if np.array_equal(IndicesMedioides, NuevoIndicesMedioides):
            break
                        
        IndicesMedioides = np.copy(NuevoIndicesMedioides)
            
    else:
        # Actualiza los clusters por ultima vez
        labels = np.argmin(D[:,IndicesMedioides], axis = 1)
        for i in range(k):
            Clusters[i] = np.where(labels==i)[0]

    if(return_labels):
        return IndicesMedioides,Clusters,labels	
            
    return IndicesMedioides,Clusters

def Silhouette(D,labels,k):
    """
    Taken from SKlearn's plot kmeans example
    D = matriz de distancia
    k = numero de clusters
    """
    plt.ion()
    fig, ax1 = plt.subplots()
    fig.set_size_inches(18, 7)
    ax1.set_xlim([-0.1, 1])
    ax1.set_ylim([0, len(D) + (k + 1) * 10])
    
    sample_silhouette_values = metrics.silhouette_samples(D , labels, metric='precomputed')
    
    y_lower = 10
    
    for i in range(k):
        ith_cluster_silhouette_values = \
                sample_silhouette_values[labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.spectral(float(i) / k)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                                        0, ith_cluster_silhouette_values,
                                        facecolor=color, edgecolor=color, alpha=0.7)

        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        
        y_lower = y_upper + 10  
    
    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    silhouette_avg = metrics.silhouette_score(D , labels, metric='precomputed')	
    
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([]) 
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    
    plt.suptitle(("Silhouette analysis with n_clusters =",k," and average = ",silhouette_avg),
    fontsize=14, fontweight='bold')

    plt.show()
    
