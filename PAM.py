import numpy as np
import scipy as sc
import numpy.random as rnd
import scipy.spatial as spa
import timing

def PAM(D, k, tmax = 100):
	# Leer datos desde archivo [Temporal]
	data = np.genfromtxt('iris.data',delimiter=',')
	temp= spa.distance.pdist(data,'euclidean')
	D = spa.distance.squareform(temp)
	
	# Obtener dimensiones
	m,n = D.shape
	
	# Generar array de k indices aleatorios de medoides 
	IndicesMedioides = np.sort(np.random.choice(n,k,False))	
	
	NuevoIndicesMedioides = np.copy(IndicesMedioides)
	
	Clusters = {}
	
	# Itera hasta tmax veces o hasta que converja
	for t in range(tmax):
		
		# Devuelve un array de tamaño n, donde el valor de cada uno es el índice del medioide mas cercano
		J= np.argmin(D[:,IndicesMedioides], axis = 1)		
		
		# Utiliza los valores en J para reorganizarlos en k clusters		
		for i in range(k):
			Clusters[i] = np.where(J==i)[0]
		
		# Actualiza los mediodes si el costo promedio de un elemento es menor que el existente
		for i in range(k):			
			L = np.mean(D[np.ix_(Clusters[i],Clusters[i])],axis=1)	
			
			# Si el cluster esta vacio se deja el indice existente
			if (Clusters[i].size != 0):				
				j = np.argmin(L)
				NuevoIndicesMedioides[i] = Clusters[i][j]
			else:
				NuevoIndicesMedioides[i] = IndicesMedioides[i]
			
		np.sort(NuevoIndicesMedioides)		
		
		# Verifica si converge 
		if np.array_equal(IndicesMedioides, NuevoIndicesMedioides):
			break		
				
		IndicesMedioides = np.copy(NuevoIndicesMedioides)		
		
	else:
		# Actualiza los clusters por ultima vez
		J= np.argmin(D[:,IndicesMedioides], axis = 1)		
		for i in range(k):
			Clusters[i] = np.where(J==i)[0]		
	
	return IndicesMedioides,Clusters	