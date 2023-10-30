import pandas as pd
import numpy as np
import plotly_express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

st.title("Statistical Insights")
@st.cache_data
def get_data():
    df = pd.read_csv('Womens Clothing E-Commerce Reviews.csv')
    df = df.drop(['Unnamed: 0', 'Clothing ID'], axis=1)
    df = df.dropna(subset=['Review Text', 'Division Name', 'Department Name', 'Class Name'], axis=0)
    df = df.reset_index(drop=True)
    return df

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df=get_data()

st.sidebar.header("Filter The Data Here:")

clas = st.sidebar.multiselect(
    "Select the Class Name:",
    options=df["Class Name"].unique(),
    default=df["Class Name"].unique()
)

department = st.sidebar.multiselect(
    "Select the Department Name:",
    options=df["Department Name"].unique(),
    default=df["Department Name"].unique()
)

division = st.sidebar.multiselect(
    "Select the Division Name:",
    options=df["Division Name"].unique(),
    default=df["Division Name"].unique()
)

rec = st.sidebar.multiselect(
    "Recommended yes(1) or not(0):",
    options=df["Recommended IND"].unique(),
    default=df["Recommended IND"].unique()
)

age = st.sidebar.slider('Specify the age range',18,99, value=[18,99])


df_selection = df.query("`Class Name` == @clas & `Department Name` == @department & `Recommended IND`==@rec & @age[1]>= Age >= @age[0]")


avg_rat = round(df_selection["Rating"].mean(),2)
avg_age = int(df_selection["Age"].mean())
persdata = round((df_selection.shape[0]/df.shape[0])*100,2)

st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Average Rating:", f"{avg_rat} ⭐","")
col2.metric("Average Age:", f"{avg_age}","")
col3.metric("Data Selected:", f"{persdata}%",f"{df_selection.shape[0]}")

st.markdown('### Plots')


fig1 = px.histogram(df_selection['Rating'],
                   labels={'value': 'Rating',
                           'count': 'Frequency',
                           'color': 'Rating'}, color=df_selection['Rating'],
                            height=350, width=600
                           )
fig1.update_layout(bargap=0.2)
fig1.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig1.update_layout(showlegend=False)



fig2=px.histogram(df_selection, x = df_selection['Class Name'], color=df_selection['Class Name'],height=350, width=350)
fig2.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig2.update_layout(bargap=0.2, showlegend=False)


fig3=px.histogram(df_selection, x = df_selection['Department Name'], color=df_selection['Department Name'],height=350, width=300)
fig3.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig3.update_layout(bargap=0.2, showlegend=False)

labels = ['Initmates', 'General', 'General Petite']
values = [
    (df['Division Name'] == 'Initmates').sum(),
    (df['Division Name'] == 'General').sum(),
    (df['Division Name'] == 'General Petite').sum()
]


fig4 = go.Figure(data=[go.Pie(labels=labels, values=values,hole=0.7)],layout=go.Layout(width=350, height=350))
fig4.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig4.update_layout(legend=dict(orientation='h'))


fig5 = px.histogram(df_selection['Age'], marginal='box',
                   labels={'value': 'Age'},height=500, width=1000)

fig5.update_traces(marker=dict(line=dict(color='#000000', width=2)))
#fig5.update_layout(title_text='Distribution of the Age of the Customers',title_x=0.5, title_font=dict(size=10))

labels = ['Recommended', 'Not Recommended']
values = [df_selection[df_selection['Recommended IND'] == 1]['Recommended IND'].value_counts()[1],
          df_selection[df_selection['Recommended IND'] == 0]['Recommended IND'].value_counts()[0]]


fig6 = go.Figure(data=[go.Pie(labels=labels, values=values, opacity=0.8,hole=0.7)],layout=go.Layout(width=350, height=350))
fig6.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig6.update_layout(legend=dict(orientation='h'))

age_range = [10, 20, 30, 40, 50, 60, 70, 80, 90]
age_labels = ['10to19', '20to29', '30to39', '40to49', '50to59', '60to69', '70to79', '80to89', '90to99']

# Create 'AgeGroup' column based on age ranges
for idx in range(len(age_range)):
    df_selection.loc[
        np.logical_and(df_selection['Age'] >= age_range[idx], df_selection['Age'] <= age_range[idx] + 9),
        'AgeGroup'
    ] = age_labels[idx]


grouped_df = df_selection.groupby(['AgeGroup', 'Department Name']).size().reset_index(name='Count')


fig7 = px.bar(grouped_df, x='AgeGroup', y='Count', color='Department Name',
             labels={'AgeGroup': 'Age Group', 'Count': 'Count', 'Department Name': 'Department'},
             barmode='group',
             height=400, width=800)
fig7.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig7.update_layout(bargap=0.2, showlegend=False)


fig8 = px.histogram(df_selection['Rating'], color=df_selection['Recommended IND'],
                   labels={'value': 'Rating',
                           'color': 'Recommended?'},
                            height=350, width=900)
fig8.update_layout(bargap=0.2)
fig8.update_traces(marker=dict(line=dict(color='#000000', width=2)))
#fig8.update_layout(title_text='Relationship between Ratings and Recommendation',title_x=0.5, title_font=dict(size=20))
fig8.update_layout(barmode='group')

df_selection['text_length'] = df_selection['Review Text'].apply(len)
bin_ranges = [0, 50, 100, 200, 400, 600]


fig9 = px.histogram(df_selection, x='text_length', nbins=len(bin_ranges) - 1, range_x=[min(bin_ranges), max(bin_ranges)]
                   ,height=600, width=900)
fig9.update_layout(bargap=0.5)
fig9.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig9.update_xaxes(title_text='Text Length Range')
fig9.update_yaxes(title_text='Frequency')
#fig9.update_layout(title_text='Review Text lenght',title_x=0.5, title_font=dict(size=20))
fig9.update_xaxes(tickvals=bin_ranges, ticktext=[f'{bin_ranges[i]}-{bin_ranges[i+1]}' for i in range(len(bin_ranges)-1)])




c1, c2 = st.columns((7,3))
c3, c4 ,c5 = st.columns((3,3,4))
with c1:
    st.markdown("###### Distrbuation of the Ratings")
    fig1
with c2:
    st.markdown("###### Distribution of the Recommendations")
    fig6

st.markdown("###### Relationship between Ratings and Recommendation")
st.plotly_chart(fig8)
st.markdown("###### Distribution of the Age of the Customers")
st.plotly_chart(fig5)
st.markdown("###### Department Count by Age Group")
st.plotly_chart(fig7)


with c3:
    st.markdown("###### Distribution of the Divisons")
    fig4
with c4:
    st.markdown("###### Distrbuation of the Departments")
    fig3
with c5:
    st.markdown("###### Distrbuation of the Classes")
    fig2
    
st.markdown("###### Review Text lenght")
st.plotly_chart(fig9)

st.markdown("###### Dataframe")
st.dataframe(df_selection)

st.sidebar.markdown('''
---
Made by [Bensaid Mohamed](mohamed2018bensaid@gmail.com/).
''')