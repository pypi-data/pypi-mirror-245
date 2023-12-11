import numpy as np
from statistics import mode

class Ensemble:
    def __init__(self,model:list):
        self.__model = model
        self.__label:np.ndarray = None
    
    def bagging_fit(self,x:np.ndarray,y:np.ndarray):
        record_x = [i for i in range(len(x))]
        predict_model = {}
        predict = []

        for m in self.__model:
            data_x = []
            data_y = []
            for _  in range(len(x)):
                rd_c = np.random.choice(record_x,1,replace=True)
                data_x.append(data_x[rd_c])
                data_y.append(data_y[rd_c])
            
            m.fit_predict(x,y)
            predict_model[m.nama] = m.label__
        
        count = 0
        
        while count < len(x):
            temp_pred = []
            for key in predict_model.keys():
                temp_pred.append(predict_model[key][count])
            predict.append(mode(temp_pred))
            count += 1
        
        self.__label = np.array(predict)
    
    def fit_predict_bagging(self,x:np.ndarray,y:np.ndarray):
        self.bagging_fit(x,y)
        return self.__label

        
            
            
            


            





        
