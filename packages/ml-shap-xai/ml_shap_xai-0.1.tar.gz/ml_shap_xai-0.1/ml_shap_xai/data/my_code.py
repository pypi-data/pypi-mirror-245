"""
# EXPLAINABLE AI: SHAP ALGORITHM

### Importing Libraries Required
"""

!pip install shap
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

import numpy as np
import pandas as pd
np.random.seed(123)

import shap

import warnings
warnings.filterwarnings ('ignore')

"""### Importing Data"""

# Loading the data to work with
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target
df.head()

# Information about dataset
df.info()

"""### Training XGBoost"""

# Setting up the data for modelling
y=df['target'].to_frame() # define Y
X=df[df.columns.difference(['target'])] # define X
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42) # create train and test

# Building model - Xgboost
model = XGBClassifier(random_state=42,gpu_id=0) # build classifier Gradient Boosted decision trees
model.fit(X_train,y_train.values.ravel())

# Making prediction
y_pred = model.predict(X_test)

# Performance Measurement
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

"""### Shap explainer"""

explainer = shap.TreeExplainer(model)

"""### Storing Shap expected value"""

shap_values = explainer.shap_values(X)
expected_value = explainer.expected_value

"""### Explaining XGBoost AI using Shap explainer"""

shap.summary_plot(shap_values, X,title="SHAP summary plot")

shap.summary_plot(shap_values, X,plot_type="bar", feature_names=data.feature_names)