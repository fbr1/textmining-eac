import numpy as np
import scipy.cluster.hierarchy as hr
import scipy.spatial as spa
import clustering
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
from sklearn.cluster import AgglomerativeClustering

class cluster:	
	def __init__(self,k):
		# Leer datos desde archivo [Temporal]
		data = np.genfromtxt('iris.data',delimiter=',')
		temp= spa.distance.pdist(data,'euclidean')
		D = spa.distance.squareform(temp)			
		#
		m,n = D.shape
		coasocMatrix = clustering.EAC(D,100)
		self.distanceMatrix = np.ones(n) - coasocMatrix	
		#	
		
		self.x = hr.linkage(self.distanceMatrix,method='complete')
		self.z = AgglomerativeClustering(n_clusters=k, linkage='ward').fit(self.distanceMatrix)
		self.nodes = hr.fcluster(self.x, 4,'distance') - np.ones(n,dtype=np.int8)
		print(self.nodes)
		print(self.z.labels_)
		print(self.getSilluete())
		plt.ion()		
	def getDendogram(self):
		hr.dendrogram(self.x)
		plt.show()	
	def getSilhouette(self):
		return metrics.silhouette_score(self.distanceMatrix , self.nodes, metric='precomputed')
	

	def getPrecision(self):			
		originalClusters = np.genfromtxt('orCL.data',delimiter=',',dtype=None)
		print (originalClusters)
		print(self.nodes)
		J =self.z.labels_	
		print (J)
		Clusters = {}	
		target_names = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
		#print(metrics.classification_report(originalClusters, J, target_names=target_names))     
		
		for i in range(np.amin(J),np.amax(J)):
			print(i)
			a = np.where(J==i)
			Clusters[i] = a
		print(Clusters) 	   


