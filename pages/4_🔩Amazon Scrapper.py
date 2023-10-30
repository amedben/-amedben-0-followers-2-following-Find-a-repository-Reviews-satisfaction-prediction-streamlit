import streamlit as st
import scrapp
import base64
import chatgptapi
import predictt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
st.sidebar.markdown('''
---
Made by [Bensaid Mohamed](mohamed2018bensaid@gmail.com/).
''')
st.title("Amazon Scapping Page")
st.markdown("###### Past your amazon link here (must be in all reviews fromat)")
link=st.text_area("",label_visibility='hidden')
option = st.selectbox('',('Naive Bayes', 'GRU+BERT','LSTM+BERT','GPT'))

if st.button('Generate Results'):
    csv = scrapp.scrapeAmazonReviews(link, 1)
    #csv = reviews_df.to_csv(index=False)
    #b64 = base64.b64encode(csv.encode()).decode()
    #href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV File</a>'
    #st.markdown(href, unsafe_allow_html=True)
    csv= csv.dropna()
    if (option=='Naive Bayes'):
        csv['sentiment_score'] = csv['Review'].apply(predictt.predictnb)
    elif(option=='GRU+BERT'):
        csv['sentiment_score'] = csv['Review'].apply(predictt.predictgru)
    elif(option=='LSTM+BERT'):
        csv['sentiment_score'] = csv['Review'].apply(predictt.predictlstm)
    elif(option=='GPT'):
        csv['sentiment_score'] = csv['Review'].apply(chatgptapi.gptpredict)
    else:
        print('error')
    #csv['sentiment_score'] = csv['Review'].apply(predictt.predictnb)
    csv['Satisfaction'] = csv['sentiment_score'].apply(lambda x: 0 if x < 0.5 else 1)
    
    avg_rate = round(csv["Ratings"].mean(),2)
    persdata = int((csv.shape[0]))
    sat = round(((csv['Satisfaction'] == 1).sum()/csv.shape[0])*100,2)
    st.markdown('### Metrics')
    col1, col2, col3 = st.columns(3)
    col1.metric("Reviews Scraped:", f"{persdata}")
    col2.metric("Average Rating:", f"{avg_rate}","")
    col3.metric("Satisfaction:", f"{sat}%","")
    
    
    st.markdown('### Plots')

    fig1 = px.histogram(csv['Ratings'],
                    labels={'value': 'Ratings',
                            'count': 'Frequency',
                            'color': 'Rating'}, color=csv['Ratings'],
                                height=350, width=600
                            )
    fig1.update_layout(bargap=0.2)
    fig1.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig1.update_layout(showlegend=False)
    
    

    fig2 = px.pie(csv, names='Satisfaction', title=f'Pie Chart 1',hole=0.7,width=250, height=300)
    rating_counts = csv.groupby(['Ratings', 'Satisfaction']).size().unstack(fill_value=0).reset_index()

    labels = ['Satisfactied', 'Not Satisfactied']
    values = [csv[csv['Satisfaction'] == 1]['Satisfaction'].value_counts()[1],
          csv[csv['Satisfaction'] == 0]['Satisfaction'].value_counts()[0]]


    fig6 = go.Figure(data=[go.Pie(labels=labels, values=values, opacity=0.8,hole=0.7)],layout=go.Layout(width=350, height=350))
    fig6.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    fig6.update_layout(legend=dict(orientation='h'))



    fig3 = px.bar(rating_counts, x='Ratings', y=[0, 1], labels={0: 'No', 1: 'Yes'},barmode='group',width=800, height=500)
    fig3.update_layout(bargap=0.2)
    fig3.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    

    c1, c2= st.columns((7,3))

    with c1:
        st.markdown("###### Distrbuation of the Ratings")
        fig1
    with c2:
        st.markdown("###### Distrbuation of the Satisfaction")
        fig6

    st.markdown("###### Relationship between Ratings and Satisfaction")
    st.plotly_chart(fig3)
    st.markdown("###### Scrapping and predections Dataframe ")
    st.dataframe(csv)


    