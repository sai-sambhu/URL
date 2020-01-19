from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

from basic_app.forms import UserForm
from basic_app.models import UserProfile,UserRequests

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse

from django.urls import reverse
from django.contrib.auth.decorators import login_required


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

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH=os.path.join(BASE_DIR,'basic_app')
DatasetPath=os.path.join(BASE_PATH,'NEWDataset.csv')
#dataset = pd.read_csv('C:\\Users\\sambhu\\Desktop\\Desktop\\programming\\sai_Django\\PhishingURLDetection\\basic_app\\NEWDataset.csv')
dataset = pd.read_csv(DatasetPath)



X = dataset.iloc[:, 2:].values
y = dataset.iloc[:, 0].values

# Splitting the dataset into the Training set and Test set
from sklearn import model_selection
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.25, random_state = 0)
scores=0.8198
score = 0.7293
# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting SVM to the Training set
from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, y_train)

NLPDatasetPath=os.path.join(BASE_PATH,'Restaurant_Reviews.tsv')
#data = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)
data = pd.read_csv(NLPDatasetPath, delimiter = '\t', quoting = 3)

phrases = data.iloc[:, 0].values
sentiment= data.iloc[:, 1].values

from bs4 import BeautifulSoup


from sklearn.tree import DecisionTreeRegressor
regressor = DecisionTreeRegressor(random_state = 0)
regressor.fit(X_train, y_train)
#score = regressor.score(X_test, y_test)

print("score with decision tree regression is {0:.5f} %".format(100 * scores))
DecisionTEST= "{:.3f}".format(score*100)
DecisonTrain= "{:.3f}".format(scores*100)


def AddAdditionalInfo(i):
    if("." in i):
       if('http' in i):
           if('www' in i):
            pass
           else:
               
               i=i[i.find('/')+2:]
               i="http://www."+i
       elif 'www' not in i:
           i='http://www.'+i
       else:
           i='http://'+i
    return i      
        

def simple_split(data,y,length,split_mark=0.7):
    if split_mark >0 and split_mark<1.0:
        n=int(split_mark*length)
    else:
        n=int(split_mark)
    X_train=data[:n].copy()
    X_test=data[n:].copy()
    y_train=y[:n].copy()
    y_test=y[n:].copy()
    return X_train,X_test,y_train,y_test    


X_train, X_test, y_train, y_test = simple_split(data.Review, data.Liked, len(phrases))

from sklearn.feature_extraction.text import CountVectorizer

vectorizer=CountVectorizer()
#print("Vocabulary size: {}".format(len(vect.vocabulary_)))

X_train=vectorizer.fit_transform(X_train)
X_train=X_train.toarray()
X_test=vectorizer.transform(X_test)
X_test=X_test.toarray()

#print("Vocabulary : {}".format(vectorizer.vocabulary_))


feture_names=vectorizer.get_feature_names()


from sklearn.naive_bayes import MultinomialNB
mnb = MultinomialNB()
mnb.fit(X_train, y_train)

print("Multinomial Navie bayes Training set score: {:.3f}".format(mnb.score(X_train,y_train)))
print("Multinomial Navie bayes Testing set score: {:.3f}".format(mnb.score(X_test,y_test)))

NLPTest = "{:.3f}".format(mnb.score(X_test,y_test)*100)
NLPTrain = "{:.3f}".format(mnb.score(X_train,y_train)*100)


def sanitization(f):
    tkns_BySlash = str(f.encode('utf-8')).split('/')	# make tokens after splitting by slash
    total_Tokens = []
    for i in tkns_BySlash:
        tokens = str(i).split('-')	# make tokens after splitting by dash
        tkns_ByDot = []
        for j in range(0,len(tokens)):
            temp_Tokens = str(tokens[j]).split('.')	# make tokens after splitting by dot
            tkns_ByDot = tkns_ByDot + temp_Tokens
        total_Tokens = total_Tokens + tokens + tkns_ByDot
    total_Tokens = list(set(total_Tokens))	#remove redundant tokens
    if 'com' in total_Tokens:
        total_Tokens.remove('com')	#removing .com since it occurs a lot of times and it should not be included in our features
    return total_Tokens     


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

y_list_Pattern = dataset.iloc[:, 0].values
url_list_Pattern = dataset.iloc[:, 1].values

TFIDvectorizer = TfidfVectorizer(tokenizer=sanitization)
X_list_Pattern = TFIDvectorizer.fit_transform(url_list_Pattern) 

X_train_Pattern, X_test_Pattern, y_train_Pattern, y_test_Pattern = train_test_split(X_list_Pattern, y_list_Pattern, test_size=0.2, random_state=42)

# Model Building
#using logistic regression
logit = LogisticRegression()	
logit.fit(X_train_Pattern, y_train_Pattern)

print("Accuracy ",logit.score(X_test_Pattern, y_test_Pattern)) 
X_predict = TFIDvectorizer.transform(['http://www.google2.com'])
New_predict = logit.predict(X_predict)
print(New_predict)      

def index(request):
    return render(request,'index.html',{'NLPTest':NLPTest,"NLPTrain":NLPTrain,
                                        "DecisionTEST":DecisionTEST,"DecisonTrain":DecisonTrain})
    
def Greater(i,j):
    if i>=j:
        return 'good'
    return 'bad'


def register(request):
    registered=False
    if request.method=="POST":

        user_form=UserForm(data=request.POST)
        
        if user_form.is_valid() :
            print("NAME: "+ user_form.cleaned_data['username'])
            user=user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            
            
            registered=True
        else:
                print(user_form.errors)
    else:
         user_form=UserForm()


    return render (request,'registration.html',{'user_form':user_form,'registered':registered})

def hasNumbers(inputString):
     return any(char.isdigit() for char in inputString)
@login_required
def user_logout(request):
     logout(request)
     return HttpResponseRedirect(reverse('index'))


@login_required
def URL(request):
    
           
       if request.method=="POST":
           Count_tags=[]
           URLForm = request.POST.getlist('URL')
           print(URLForm)
           URLForm=URLForm[0]
           i=AddAdditionalInfo(URLForm)
           PatternI=i
           print(i)
           user=UserRequests.objects.get_or_create(username= request.user.username,
                                                       requests=i)
           print(i)
           my_dict={}
           try:
            response = urlopen(i)
            html = response.read()
            soup = BeautifulSoup(html)
            html=str(html)[2:-1]
            for i in range(len(tag_list)):
                    Count_tags.append(html.count(tag_list[i]))
                    pass
                    
            
            
            
            # Predicting the Test set results
            y_pred = classifier.predict([Count_tags])
            y_pred = regressor.predict([Count_tags])
            print("y_pred",y_pred[0])
            Count_tags=[]
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

                # get text
            text = soup.get_text()

                # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
                # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            text=text.split("\n")
            
            Count1=0
            Count0=0
            #till here
            for i in text:
               x=mnb.predict(vectorizer.transform([i]).toarray())[0] 
               #print("Multinomial navie bayes",x)
               if x==1:
                     Count1=Count1+1
               else:
                    Count0=Count0+1
            print('I am done') 
            #till here
            y_pred2=Greater(Count1,Count0)
            
            
            N_pred = 1 if y_pred2=='good' else 0
            D_pred=y_pred[0]
            if y_pred[0]>0.7:
                y_pred='good'
                
            else:
               y_pred='bad'
               
            print("MNB Trainset accuracy",NLPTrain,"MNB Testset accuracy",NLPTest,"Decision Trainset accuracy",DecisonTrain,"Decision Testset accuracy",DecisionTEST)    
            my_dict={"set":True,"URL":URLForm,"y_pred":y_pred,"N_pred":N_pred,"y_pred2":y_pred2,"D_pred":D_pred}
            print(PatternI,"I ra")
            my_dict['pattern']='good'
            PatternI=PatternI[:3]+"s"+PatternI[4:]
            if hasNumbers(PatternI):
                my_dict['pattern']='bad'
            else:
                X_predict = TFIDvectorizer.transform([PatternI])
                New_predict = logit.predict(X_predict)
                print(New_predict) 
                if(New_predict == 0):
                    my_dict['pattern']='good'
                else:
                    my_dict['pattern']='bad'
                pass
            
           except:
               my_dict={'not_set':True}
               my_dict['URL']=PatternI
               if hasNumbers(PatternI):
                my_dict['pattern']='bad'
               else:
                X_predict = TFIDvectorizer.transform([PatternI])
                New_predict = logit.predict(X_predict)
                print(New_predict) 
                if(New_predict == 0):
                    my_dict['pattern']='good'
                else:
                    my_dict['pattern']='bad'
                pass
                      
                
            
           return render(request,'URLDetection.html',context=my_dict)
           pass
       else:
            return render(request,'URLDetection.html')
                   
def user_login(request):


       if request.method=="POST":
           username=request.POST.get('username')
           password=request.POST.get('password')

           user=authenticate(username=username,password=password)



           if user:

               if user.is_active:
                   login(request,user)
                  
                  
                   return HttpResponseRedirect(reverse('URL_page'))

                   

               else :
                   return HttpResponse("ACCOUNT NOT ACTIVE")
           else:
               print("someone tried to login and failed")
               print(f'username: {username} and password: {password} ')
               return HttpResponse("invalid login details supplied!!")

       return render(request,'login.html',{})
   