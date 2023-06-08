from django.shortcuts import render,redirect
from .forms import loginForm,signupForm
from django.contrib.auth import authenticate,login,logout

import pickle
import pandas as pd
import numpy as np

from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder


# Create your views here.
def model(request):
    # fm=billingForm()
    
    values=[]
    top_30_items = pickle.load(open('top-30-items.pkl', 'rb'))
    
    print(type(top_30_items))
    
       
    with open('fpgrowth-model.pkl', 'rb') as f:
        fp_model = pickle.load(f)
        
    te = TransactionEncoder()
    te.fit(top_30_items)
    if request.method=="POST":
        
        input1=request.POST.get('p1')
        input2=request.POST.get('p2')
        input3=request.POST.get('p3')
        input4=request.POST.get('p4')
       
        values.append(input1)
        values.append(input2)
        values.append(input3)
        values.append(input4)
        
        print(values)
        transaction = values 
        print(top_30_items)
        transaction = np.array(transaction)
        print(transaction)
        # TransactionEncoder
        te = TransactionEncoder()
        te_ary = te.fit(top_30_items).transform(transaction)
        
       
        df = pd.DataFrame(te_ary, columns=te.columns_)
        te_ary = te.transform(transaction)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        
        recommendations = fpgrowth(df, min_support=0.05, use_colnames=True)
        recommendations = association_rules(recommendations, metric='lift', min_threshold=1)
        recommendations = recommendations.sort_values('confidence', ascending=False)
        
        print("result:----")
        print(recommendations)
        
def home(request):
    return render(request,'home.html')


def auth_login(request):
    form=loginForm(request.POST or None)
    msg=None
    if request.method=='POST':
        if form.is_valid():
            
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            
            if user is not None:
                
                login(request,user)
                return redirect('home')
            else:
                msg="invalid credentials"
        else:
            msg="ERROR  validating form"

        
    return render(request,'login.html',{"form":form,"msg":msg})

def signup(request):
    
    msg=None
    if request.method =='POST':
        form=signupForm(request.POST)
        
        if form.is_valid():
            
            user=form.save()
            msg="user created"
            return redirect('login')
        else:
            msg="form is not valid"
    else:
        form=signupForm()
    
    return render(request,'signup.html',{"form":form,"msg":msg})

def logout_request(request):
    logout(request)
    return redirect('home')
    