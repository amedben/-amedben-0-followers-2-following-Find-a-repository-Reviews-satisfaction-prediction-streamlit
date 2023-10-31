# Ecommerce Satisfaction Prediction Web App

This web application is designed to predict ecommerce satisfaction based on review text. It includes features for statistical insights, satisfaction prediction, and web scraping of Amazon product reviews. Additionally, it uses the OpenAI API to generate responses based on user feedback.

## Table of Contents

- [Architecture](#Architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)

## Architecture
![App arch](arch.png)
## Features

### 1. Dashboard for Statistical Insights

- Visualizes statistical insights and patterns from the training data.
- Provides charts, graphs, and relevant statistics to help users understand the data.

### 2. Prediction Page

- Allows users to input review text.
- Enables the selection of prediction models.
- Predicts satisfaction based on the input and the chosen model.
- Generates responses based on the satisfaction prediction using the OpenAI API.

### 3. Web Scraping Page

- Utilizes a web scraper built with BeautifulSoup to scrape Amazon product reviews.
- Supports the prediction of satisfaction for each review using selected ML or DL models.
- Generates a mini dashboard to display results and insights from the scraped data.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/amedben/Reviews-satisfaction-prediction-streamlit
   ```
2. Change to the project directory:
   
   ```bash
   cd Reviews-satisfaction-prediction-streamlit
   ```
3. Install the required dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```
   
## Usage

1. Start the Streamlit web app:
   ```bash
   streamlit run 1_Homepage.py
   ```
2. Access the app through your web browser at http://localhost:8501.

## Screenshots
1. Homepage
   ![App Home](Home.png)
2. Statistical insight page
   ![App stats1](stats1.png)
   ![App stats2](stats2.png)
3. Predection page
   ![App pred1](pred1.png)
   ![App pred2](pred2.png)
   ![App pred3](pred3.png)
4. Scarpping page
   ![App scap1](scrap1.png)
   ![App scap2](scrap2.png)


