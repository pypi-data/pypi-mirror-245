#####################################
######## CLASS LEARNING #############
#####################################

class learning:
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
        print("Feature Importance Learning: Completed")
        
        return feat_importances_all,acc_report