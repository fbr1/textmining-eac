import numpy as np

def EAC(D, N=45, low = 5,high = 30):
	"""Do Evidence Accumulation Clustering
	D= Matriz de distancia
	N= Numero de clusterings
	kinterval= Intervalo del cual elejir los k cluster aleatorios	
	"""		
	
	# Obtener dimensiones
	m,n = D.shape
	
	matrizCoAsoc = np.zeros((n, n))		
	
	for i in range(N):		
		# Elije valor aleatorio k entre low y high
		if(low!=high):
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
	
	return matrizCoAsoc
	
	

def PAM(D, k, tmax = 100):	
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
	
