import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def main():
    #just normal correlation analysis for all parameters vs. initial growth rate
    #
    # -> see if any really good correlations
    data = pd.read_csv('finalCleanDataextendedTry.csv')
    print(data)

    x = data.iloc[ : , range(1,12)]
    print(x)
    y = data["GrowthRate1"]

    # multivariate nonlinear regression
    model = LinearRegression()
    model.fit(x,y)

    print('Linear Regression')
    r_sq = model.score(x, y)
    print('coefficient of determination:', r_sq)
    print('intercept:', model.intercept_)
    print('slope:', model.coef_)

    '''
Machine and Deep Learning models - I think not good, because we have only twice as much data points, as we have countries (for the two growth rates)

#https://medium.com/datadriveninvestor/a-simple-guide-to-creating-predictive-models-in-python-part-2a-aa86ece98f86

#import clean merged data
#country, growthrate1, growthrat2, change date, [all the other variables]


#split in Train, Test, maybe Validation



from sklearn.model_selection import train_test_split

#splitting
X_train, X_test, y_train, y_test = train_test_split(feat, label, test_size=0.3)

#scale large data smaller
from sklearn.preprocessing import
sc_x = StandardScaler()
X_train = sc_x.fit_transform(X_train)
X_test = sc_x.fit_transform(X_test)

#support  vector machine using RBF Network
from sklearn.svm import SVC
support_vector_classifier = SVC(kernel='rbf')
support_vector_classifier.fit(X_train,y_train)
y_pred_svc = support_vector_classifier.predict(X_test)
from sklearn.metrics import confusion_matrix
cm_support_vector_classifier = confusion_matrix(y_test,y_pred_svc)
print(cm_support_vector_classifier,end='\n\n')

#Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier
random_forest_classifier = RandomForestClassifier()
random_forest_classifier.fit(X_train,y_train)
y_pred_rfc = random_forest_classifier.predict(X_test)
cm_random_forest_classifier = confusion_matrix(y_test,y_pred_rfc)
print(cm_random_forest_classifier,end="\n\n")

#Tensor Flow guide
#https://medium.com/datadriveninvestor/a-simple-guide-to-creating-predictive-models-in-python-part-2b-7be3afb5c557
'''

if __name__ == '__main__':
    main()