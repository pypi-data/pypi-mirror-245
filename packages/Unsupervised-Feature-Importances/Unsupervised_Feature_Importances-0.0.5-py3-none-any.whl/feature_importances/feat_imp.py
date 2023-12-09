
####################################
########## FEAT IMP ################
####################################

def feat_imp(df,y):
    from class_cluster import autocluster

    #get the K value
    n = autocluster.auto_elbow_search(df.select_dtypes(exclude ='object'))    
    #get the cluster values with df
    df_1 = autocluster.kmeanscluster(df,n)
    
    #compute feat importance
    from class_learning import learning
    feat_df,accuracy_report= learning.supervised_learning(df_1,y)
    
    return feat_df, accuracy_report

