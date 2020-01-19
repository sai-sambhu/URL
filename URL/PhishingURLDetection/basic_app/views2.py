from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

import pandas as pd


from urllib.request import urlopen
tag_list = ['a','<acronym','<abbr','<address','<bdi','<bdo','<blockquote','<cite',
            '<code','<del','<dfn','<ins','<kbd','<mark','<meter','<pre','<progress',
            '<q','<rp','<rt','<ruby','<s','<samp','<strong','<template','<time',
            '<var','<wbr','<textarea','<button','<select','<optgroup','<option',
            '<label','<fieldset','<legend','<datalist','<output','<b','<body','<big',
            '<br','<center','<dd','<dl','<dt','<em','<embed','<font','<form','<h1','<h2',
            '<h3','<h4','<h5','<h6','<head','<hr','<html','<i','<img','<input','<li',
            '<link','<marquee','<menu','<meta','<ol','<p','<small','<strike','<long',
            '<table','<td','<th','<title','<tr','<tt','<u','<ul','<iframe','<frame',
            '<frameset','<noframes','<map','<area','<canvas','<figcaption',
            '<figure','<svg','<picture','<audio','<source','<track','<video',
            '<nav','<header','<footer','<main','<section','<article','<aside','<detail','<dialog',
            '<summary','<data']



dataset = pd.read_csv('C:\\Users\\sambhu\\Desktop\\Desktop\\programming\\sai_Django\\PhishingURLDetection\\basic_app\\NEWDataset.csv')

X = dataset.iloc[:, 2:].values
y = dataset.iloc[:, 0].values

# Splitting the dataset into the Training set and Test set
from sklearn import model_selection
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting SVM to the Training set
from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, y_train)




def AddAdditionalInfo(i):
    if('http'not in i):
        i='http://'+i
    return i    

class IndexView(TemplateView):
    template_name = 'index.html'
def URL(request):
    
           
       if request.method=="POST":
           Count_tags=[]
           URLForm = request.POST['URL']
           i=AddAdditionalInfo(URLForm)
           print(i)
           try:
            response = urlopen(i)
            html = response.read()
            html=str(html)[2:-1]
            for i in range(len(tag_list)):
                    Count_tags.append(html.count(tag_list[i]))
                    pass
                    
            
            
            # Predicting the Test set results
            y_pred = classifier.predict([Count_tags])
            print(y_pred)
            Count_tags=[]  
            if y_pred[0]==1:
                y_pred='good'
            else:
               y_pred='bad'
            my_dict={'message':f"""Hi,\n
This is to confirm that the URL {URLForm} you have entered us to check for phishing websites  is {y_pred},Prediction by SVR.

Prediction Done.

Regards
Fraud Website Dectector

    
    """              }
           except:
               my_dict={'message':f"""Hi,\n
This is to confirm that the URL {URLForm} you have entered us to check for phishing websites Does not exists, please try with another 
website

Regards
Fraud Website Dectector


    
    """              }
               
           return render(request,'URLDetection.html',context=my_dict)
           pass
       else:
            return render(request,'URLDetection.html')
                   
    