from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import numpy as np
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
from csv import writer
import pandas as pd
from flask_material import Material
from keras.models import load_model


import pickle




app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'

# Enter your database connection details below


# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = 1#cursor.fetchone()
        print (account)
                # If account exists in accounts table in out database
        if username=="admin" and password=="admin":
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] =1 #account['id']
            session['username'] = "admin" #account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
@app.route('/pythonlogin/upload_image', methods=['POST'])
def upload_image():
    if 'loggedin' in session:
        cylinders=int(request.form["cylinders"])
        displacement=int(request.form["displacement"])
        horsepower=int(request.form["horsepower"])
        weight=int(request.form["weight"])
        acceleration=int(request.form["acceleration"])
        model_year=int(request.form["model_year"])
        origin=int(request.form["origin"])

        values=[[cylinders,displacement,horsepower,weight,acceleration,model_year,origin]]

        scaler_path=os.path.join(os.path.dirname('E:/Fuel/models/'),'scaler.pkl')

        sc=None
        with open(scaler_path,'rb') as f:
            sc=pickle.load(f)
            
        values=sc.transform(values)

        model=load_model(r"E:\Fuel\models\model.h5")

        prediction=model.predict(values)
        prediction=float(prediction)
        
        return render_template('home.html', prediction=prediction)
        
    return redirect(url_for('login'))
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
       
        
        
                
            
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        
        account = cursor.fetchone()
        cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor1.execute('SELECT * FROM predictiondetails WHERE username = %s', (session['username'],))
        prediction_details = cursor1.fetchall()
        # Show the profile page with account info
        return render_template('profile.html', account=account,prediction_details = prediction_details)
    # User is not loggedin redirect to login page
    return redirect(url_for('login')) 
    



    





if __name__ =='__main__':
	app.run()
