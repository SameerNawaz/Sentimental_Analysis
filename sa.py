from flask import Flask, request, render_template, flash
import webbrowser
import csv
import subprocess

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split # function for splitting data to train and test sets

import nltk
from nltk.corpus import stopwords
from nltk.classify import SklearnClassifier

from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt

import string
from subprocess import check_output

app = Flask(__name__, static_url_path='/static')
app.secret_key = "donedeal"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def import_data_to_csv():
    if request.method == 'POST':
        if request.form['action'] == 'Import the data':
            #importing emotions and Feedback
            sentiment1 = request.form['emotions']
            text1 = request.form['feedback']
            if text1 == '':
                return render_template('index.html')
            rows = [[sentiment1,text1]]
   
            # name of csv file
            filename = 'Sentiment1.csv'
            
            # writing to csv file
            with open(filename, 'a') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows('\n')
                # writing the data rows
                csvwriter.writerows(rows)
                sa = pd.read_csv(filename)
                sa.to_csv('Sentiment1.csv', index=False)
            
            return render_template('index.html')
        elif request.form['action'] == 'Import the word':
            #importing Sentiment and words
            senti1 = request.form['words']
            word1 = request.form['newords']
            word1 = word1.replace(' ','')
            if word1 == '':
                return render_template('index.html')
            rows = [[senti1,word1]]
        
            # name of csv file
            filename = 'wordtesting.csv'
                # writing to csv file
            with open(filename, 'a') as f:
                # creating a csv writer object
                csvwriter = csv.writer(f,lineterminator='\r')
                csvwriter.writerows('\n')
                # writing the data rows
                csvwriter.writerows(rows)
            
            f.close()
                
        return render_template('index.html')

@app.route('/output.html', methods=['POST'])
def senti_output():
    if request.form['action'] == 'Generate WordCloud':
            #Importing data from csv file
            data = pd.read_csv('sentiment1.csv')
            # Keeping only the neccessary columns
            data = data[['text','sentiment']]

            # Splitting the dataset into train and test set
            train, test = train_test_split(data,test_size = 0.0)
            # Removing neutral sentiments
            train = train[train.sentiment != "Neutral"]
    
    
            train_pos = train[ train['sentiment'] == 'Positive']
            train_pos = train_pos['text']
            train_neg = train[ train['sentiment'] == 'Negative']
            train_neg = train_neg['text']
    
    
            #read only postive words from csv file
            posi = pd.read_csv('wordtesting.csv')
            posi = posi[['senti','word']]
            train, test = train_test_split(posi,test_size = 0.0)
            pw = train[train['senti'] == 'Positive']
            pw = pw['word']
            p = pw.tolist()
            positive = [item.lower() for item in p]
    
            #read only negative words from csv file
            neg = pd.read_csv('wordtesting.csv')
            neg = neg[['senti','word']]
            train, test = train_test_split(neg,test_size = 0.0)
            nw = train[train['senti'] == 'Negative']
            nw = nw['word']
            n = nw.tolist()
            negative =[item.upper() for item in n]
    
            #Function to create wordcloud of positive words
            def wordcloud_draw_pos(data1,data2, color = 'black'):
                words = data1.tolist() + data2.tolist()
        
                joined_pword = ' '.join(words)
                joined_nword = ' '.join(words)
        
                c_pword = joined_pword.split()
                c_nword = joined_nword.split()
        
                clean_pword = [item.lower(  ) for item in c_pword]
                cleaned_nword = [item.upper() for item in c_nword]
        
                new_list_pos = set(positive)& set(clean_pword)
                new_list_neg = set(negative)& set(cleaned_nword)
        
                cleaned_pword = ' '.join(new_list_pos)
                cleaned_nword = ' '.join(new_list_neg)
        
                clean_word = cleaned_pword + cleaned_nword
        
                wordcloud = WordCloud(stopwords=STOPWORDS,
                              background_color=color,
                              width=1600,
                              height=800
                              ).generate(clean_word)
                plt.imsave('static/images/New.png',wordcloud)
                
            #Creating wordcloud for All words
            wordcloud_draw_pos(train_pos,train_neg,'white')
    return render_template('output.html')

if __name__ == '__main__':

    app.run(debug=True)
