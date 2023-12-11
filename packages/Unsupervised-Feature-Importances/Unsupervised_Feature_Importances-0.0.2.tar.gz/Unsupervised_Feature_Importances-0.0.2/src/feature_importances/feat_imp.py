###################################
########  Cluster   ###############
###################################


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


#####################################
######## CLASS LEARNING #############
#####################################

def supervised_learning(X,target):
    print("Processing: Learning********")
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report
    import pandas as pd
    
    #define X and y
    y = X[target]
    X = X.drop(target,axis=1)

    #Split 
    x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.30)
    
    rf_model = RandomForestClassifier()
    rf_model.fit(x_train,y_train)
    yhat = rf_model.predict(x_test)
    #accuracies
    acc_report = pd.DataFrame(classification_report(yhat,y_test,output_dict=True))
    
    #feat import
    feat_imp_score = rf_model.feature_importances_
    feat_importances_all = pd.Series(feat_imp_score, index=X.columns).nlargest(30)
    
    del(rf_model,yhat,feat_imp_score)
    print("Feature Importance Learning: Completed")
    
    return feat_importances_all,acc_report
####################################
########## FEAT IMP ################
####################################

def compute(df):
    
    #get the K value
    n = auto_elbow_search(df.select_dtypes(exclude ='object'))    
    #get the cluster values with df
    df_1 = kmeanscluster(df,n)
    
    #compute feat importance
    feat_df,accuracy_report= supervised_learning(df_1,'cluster')
    
    return feat_df, accuracy_report

