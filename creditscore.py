import pandas as pd
import pickle
from lightgbm import LGBMClassifier
from sklearn.metrics import precision_score, roc_auc_score

def X_y(data, label_name):
    X = data.drop(label_name,1)
    y = data[label_name]
    return X, y    

# def visualize(data):

# def feat_eng(data):
    
def score(y_true, y_pred, y_proba):
    prec = precision_score(y_true, y_pred)
    auroc = roc_auc_score(y_true, y_proba)
    
    print('Precision :', prec, '\nAuroc :', auroc)
    
    return prec, auroc
    
class Modelling:
    def __init__(self):
        self.varMode = {}
        self.uniq = {}
        self.indexDummy = None
        self.model = None
        self.threshold = None

    def fit_varmode_uniq(self, data):
        for i in data:
            if data[i].dtype=='O':
                self.varMode[i] = data[i].mode()[0]
                self.uniq[i] = data[i].dropna().unique()
            elif data[i].dtype.kind in ['i', 'f']:
                self.varMode[i] = data[i].median()
            else:
                print('column', i, data[i].dtype)
                print('dataype not decided yet!')
                break
                
        return self
    
    def transform_null(self, data):
        for col, val in self.varMode.items():
            data[col] = data[col].fillna(val)
        
        return data
        
    def fit_dummy(self, data):
        self.indexDummy = pd.get_dummies(data).columns
        
        return self
        
    def transform_dummy(self, data):
        data = pd.get_dummies(data)
        data = data.reindex(columns=self.indexDummy, fill_value=0)
        
        return data
    
    def fit_model(self, X, y):
        self.model = LGBMClassifier()
        self.model.fit(X, y)
        
        return self
        
class Predicting(Modelling):
    def __init__(self):
        try:
            with open('credit_score_model_and_assortments.pkl', 'rb') as f:
                pkl = pickle.load(f)
                self.varMode = pkl['varMode']
                self.uniq = pkl['uniq']
                self.indexDummy = pkl['indexDummy']
                self.model = pkl['model']
                self.threshold = pkl['threshold']
        except FileNotFoundError:
            raise FileNotFoundError('Where is the file?')
    
    def transform_not_uniq(self, data):
        for col, val in self.uniq.items():
            data[col] = data[col].map(lambda x: self.varMode[col] if x not in val else x)
        
        return data
    
    def predict_data(self, X):
        y_pred = self.model.predict(X)
        y_proba = self.model.predict_proba(X)[:,1]
        
        return y_pred, y_proba