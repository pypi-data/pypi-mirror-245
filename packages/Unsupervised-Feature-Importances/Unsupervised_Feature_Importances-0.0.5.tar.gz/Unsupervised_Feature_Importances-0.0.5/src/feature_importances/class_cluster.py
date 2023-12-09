###################################
########  Cluster   ###############
###################################

class autocluster:
    def auto_elbow_search(data):
        print("Processing: Auto Elow**********")
        from sklearn.cluster import KMeans
        wcss = []
        K = range(1,10) #get the cluster range
        for no_of_clusters in K:
            k_model = KMeans(n_clusters = no_of_clusters)
            k_model.fit(data)
            wcss.append(k_model.inertia_)
            
        
        
        #function to calculate distance from a and b in 2-d
        def calc_distance(x1,y1,a,b,c):
            import math
            d = abs((a* x1 + b* y1 +c))/ (math.sqrt(a *a+b *b))
            return d
    
        a = wcss[0] - wcss[8]
        b = K[8]-K[0] 
        c1 = K[0] * wcss[8]
        c2 = K[8] * wcss[0]
        c = c1-c2
    
                 
        distance_of_points_from_line = []
        for k in range(9):
            distance_of_points_from_line.append(calc_distance(K[k],
                                                              wcss[k],a,b,c))
            result = distance_of_points_from_line.index(max(distance_of_points_from_line))+1
        
        return result 
    
    def kmeanscluster(df_1, n):
        print("Processing: Kmeans**********")
        from sklearn.cluster import KMeans
        import pandas as pd
        # Fitting K-Means to the dataset
        kmeans_model = KMeans(n_clusters =n, init = 'k-means++', random_state = 0)
        #Predicting with new data
        y_kmeans = kmeans_model.fit_predict(df_1)
        df_1 = pd.concat([pd.DataFrame(y_kmeans).reset_index(drop=True),df_1],axis=1)
        df_1.rename(columns={0:'cluster'},inplace=True)
        
        return df_1

