import numpy as np
import scipy.spatial as spa
import clustering

def main():

	# Leer datos desde archivo [Temporal]
	data = np.genfromtxt('iris.data',delimiter=',')
	temp= spa.distance.pdist(data,'euclidean')
	D = spa.distance.squareform(temp)	
	return clustering.EAC(D)
    

if __name__ == "__main__":
    main()