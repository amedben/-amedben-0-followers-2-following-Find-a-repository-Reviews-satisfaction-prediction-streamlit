import streamlit as st
st.set_page_config(layout="wide")
st.title("Women's Clothing eCommerce Predictive Analytics Web App")
st.image('wawa.png')
st.header('Welcome to our app')
st.write("Welcome to the Women's Clothing eCommerce Review Sentiment Analysis App,a handy tool designed for research purposes. This app aids in analyzing customer sentiment in women's clothing product reviews, making it ideal for academic research projects. Whether you're a student or a researcher, our app simplifies the process of understanding customer satisfaction.")
st.subheader("Key Features:")
st.markdown("**Statistical Insights**: Access statistical graphs generated from the training dataset to support research. Allows to gain insights into market trends and consumer preferences, making your research more data-driven.")
st.markdown("**Prediction Page**: Enter a review and our app's machine learning models will predict customer satisfaction. This feature streamlines sentiment analysis for your research, allowing you to dig into customer feedback effortlessly, and also generate a response for the customer that adapts to their criticisms.")
st.markdown("**Amazon Review Scraper**: Stay ahead of the competition by harnessing the power of customer feedback.Enter an Amazon product link and our built-in web scraper will collect user reviews. Machine learning models then analyse these reviews to predict customer satisfaction, and generate a graphical report. Gain real-time insight into product performance and customer sentiment.")



st.sidebar.markdown('''
---
Made by [Bensaid Mohamed](mohamed2018bensaid@gmail.com/).
''')