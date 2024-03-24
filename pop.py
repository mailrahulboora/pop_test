#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import panel as pn
import numpy as np
import hvplot.pandas
pn.extension()


# In[2]:


def db_population():
    df=pd.read_excel('pop.xlsx',sheet_name=0)
    for col in df.iloc[:,4:].columns.tolist():
        df[col]=df[col].apply(lambda x: np.nan if x=='..' else x)
    df.drop(columns=['2022 [YR2022]'],inplace=True)
    return df
df=db_population()
df.dropna(inplace=True)


# In[3]:


def grop_data_extractor(df,col,list):
    temp_df=pd.DataFrame()
    for con in list:
        temp_df=pd.concat([temp_df,df[df[col]==con]],ignore_index=True)
    new_df=pd.DataFrame()
    new_df['year']=[i for i in range(1990,2022)]
    for con in list:
        new_df[con]=temp_df[temp_df[col]==con].iloc[0,4:].values.squeeze()
    return new_df

marker_style=['.','o','v','^','<','>','1','2','3','4','s','p','*','h','H','X','d','D','+','_','|','x']
con_list=df['Country Name'].unique().tolist()
select=pn.widgets.MultiChoice(name='Select the Country', value=['India','China'],options=con_list)
size= pn.widgets.FloatSlider(name='Set Figure size', start=3, end=10, step=0.5, value=4)
def create_plot(symbol,size=4):
    #size=4
    fig,axes=plt.subplots(figsize=(size+1,size-1))
    for num,con in enumerate(symbol):
        axes.plot(range(1990,2022),df[df['Country Name']==con].iloc[:,4:].values.squeeze(),label=con,marker=marker_style[num])
    plt.xlabel('Year')
    plt.ylabel('% Population Gworth Rate')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.close(fig)
    return fig
    
def plot(symbol,size):
    data=grop_data_extractor(df,'Country Name',symbol)
    return data.hvplot.line(x='year',y=data.iloc[:,1:].columns.tolist(),ylabel='% Population Growth Rate',width=int(150*size),height=int(100*size))
    
layout=pn.Column(
    pn.Column(select),
    pn.Column(size),
    plot(select.value,size.value),
    create_plot(select.value,size.value))
def update(event):
    layout[-1].object=create_plot(select.value,size.value)
    layout[-2].object=plot(select.value,size.value)
select.param.watch(update,'value')
size.param.watch(update,'value')
layout.servable()
