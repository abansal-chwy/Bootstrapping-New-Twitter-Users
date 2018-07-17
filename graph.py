import matplotlib.pyplot as plt
import pandas as pd


precision=pd.read_csv("plot_Prec.csv")


y=[]
for i in range(1,5):
    y.append(precision.iloc[0,i])
    print(precision.iloc[0,i])
x=[10,15,20,5]

plt.scatter(x,y,color="r")
plt.show()