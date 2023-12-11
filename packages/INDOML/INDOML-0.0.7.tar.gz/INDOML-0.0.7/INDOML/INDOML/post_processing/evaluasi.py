import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score
from random import sample
sns.set()

def elbow_method(model,start_cluster:int,end_cluster:int,data:np.ndarray):
    x = []
    y = []

    for x_ in range(start_cluster,end_cluster):
        
        k = model(x_)
        k.fit(data)
        insersia = k.inersia_
        x.append(x_)
        y.append(insersia)
    
    plt.plot(x,y,marker='o',linestyle='--')
    plt.title("Optimal Jumlah Cluster")
    plt.xlabel("cluster")
    plt.ylabel("Sum Square Error")
    plt.tight_layout()
    plt.show()

def hopkins_statistik(x:np.ndarray,n_neighbors:int=2):
    
    n = len(x)
    nei = NearestNeighbors(n_neighbors=n_neighbors).fit(x)

    sli = sample(range(0,n,1),n)
    rand_data = [x[i] for i in sli]
    u_distances = nei.kneighbors(x, n_neighbors=n_neighbors)[0][:, -1]
    w_distances = nei.kneighbors(rand_data, n_neighbors=n_neighbors)[0][:, -1]

    hop = np.sum(u_distances)/(np.sum(u_distances)+np.sum(w_distances))

    return hop

def visual_silhoutte(model,start_cluster:int,end_cluster:int,data:np.ndarray):
    no_cluster = []
    siluette_score = []
    for n in range(start_cluster,end_cluster):
        k = model(n)
        k.fit_predict(data)
        label = k.label__
        siluette_score.append(silhouette_score(data,label))
        no_cluster.append(n)
    
    plt.plot(no_cluster,siluette_score,marker='o',linestyle='--')
    plt.title("Optimal Jumlah Cluster")
    plt.xlabel("cluster")
    plt.ylabel("Silhouette Score")
    plt.tight_layout()
    plt.show()

def visual_silhoutte_dbms(model,title:str,xlabel:str,start:int,end:int,step:int,data:np.ndarray,minpts:int=None,epsilon:int=None):
    no_cluster = []
    siluette_score = []
    if epsilon and not minpts:
        for n in range(start,end,step):
            k = model(epsilon,n)
            k.fit_predict(data)
            label = k.label_
            siluette_score.append(silhouette_score(data,label))
            no_cluster.append(n)
    elif minpts and not epsilon:
        while start!=end:
            k = model(start,minpts)
            k.fit_predict(data)
            label = k.label_
            siluette_score.append(silhouette_score(data,label))
            no_cluster.append(start)
            start += step
    
    plt.plot(no_cluster,siluette_score,marker='o',linestyle='--')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Silhouette Score")
    plt.tight_layout()
    plt.show()

def silhoutte_skor(label:np.ndarray,data:np.ndarray):
    return silhouette_score

