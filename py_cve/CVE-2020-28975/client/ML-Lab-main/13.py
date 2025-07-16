import pandas as pd
from sklearn.tree import DecisionTreeClassifier,plot_tree
from sklearn.metrics import accuracy_score,classification_report
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
data=pd.read_csv("weather_forecast (2).csv")
print(f"Number of data points: {data.shape[0]}")
print(data.head())
data=pd.get_dummies(data,drop_first=True)
x=data.drop("Play_Yes",axis=1)
y=data["Play_Yes"]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

clf=DecisionTreeClassifier(criterion="entropy",random_state=42)

clf.fit(x_train,y_train)
plt.figure(figsize=(12,8))
plot_tree(clf,filled=True,feature_names=x.columns,class_names=["No","Yes"])
plt.show()
pred=clf.predict(x_test)
acc=accuracy_score(y_test,pred)
report=classification_report(y_test,pred)
print(f"Accuracy:{acc}")
print(f"Report\n{report}")
