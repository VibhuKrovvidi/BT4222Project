# BT4222Project

## Datasets

| Dataset  | Description |
| ------------- | ------------- |
| reg_scraped_output.csv | Scraped reviews which includes 1) review 2) date 3) stars 4) restaurant |
| sent_datasets > total_sentiment_data.pkl | Processed Full Dataset used for model training|
| sent_datasets > sent_train.pkl | Processed Training Dataset used for model training |
| sent_datasets > sent_validate.pkl | Processed Validation Dataset used for model training |
| sent_datasets > sent_test.pkl | Processed Test Dataset used for model training |
| Clause Polarity Predictions (CNN).csv | Predictions of Clause Polarity using CNN |
|predicteddata_forEDA.csv| CNN predictions of 5 randomly chosen restaurants for EDA |

## Python Notebooks/Scripts


| Notebook/Script  | Description |
| ------------- | ------------- |
| scraping > scrape.py  | Python script used to scrape reviews from Google Reviews  |
| BT4222_Processing.ipynb  | Processes scraped data through feature-descriptor extraction, word embeddings, feature categorization and sentiment analysis|
| EDA.ipynb | Conducts exploratory data analysis for processed data and predictions from CNN Model| 
|BT4222_Sentiment.ipynb|Tried implementing machine learning models to predict clause polarity|
|CNN Clause Polarity.ipynb| Preprocesses data and implements CNN Model to predict clause polarity|
|Model_Comparison.ipynb | Predicts clause polarity using other Neural Network Models (LSTM, Bi-LSTM, GRU, simple RNN)|
|BT4222_Regression.ipynb | Implements regression on star ratings using categories we obtained|




 


