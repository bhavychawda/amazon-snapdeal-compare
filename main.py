
import pyrebase
from flask import Flask, flash, session,redirect, render_template, request, session, abort, url_for

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from send_mail import *

from flask import Flask,render_template,request,redirect
from flask import Flask
from bot import *
from singleproduct import *

app = Flask(__name__)       #Initialze flask constructor
app.secret_key = "abc" 

cred = credentials.Certificate("cdeal-f772f-firebase-adminsdk-1h6c0-f0e0b99461.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


#Add your own details
config = {
 'apiKey': "AIzaSyD3I1oY3Ykv2ZJXeHHz_xclmjJGfYjT0Pk",
  'authDomain': "cdeal-f772f.firebaseapp.com",
  'projectId': "cdeal-f772f",
  'storageBucket': "cdeal-f772f.appspot.com",
  'messagingSenderId': "754250424363",
  'appId': "1:754250424363:web:0103a3a2368a5bd2f2ca6e",
"databaseURL": "https://cdeal-f772f-default-rtdb.firebaseio.com/"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


#Initialze session as dictionary
# session = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

#Login
@app.route("/")
def home():
    try:
        if session["is_logged_in"] == True:
              print("i am logined")
        else:
           session["is_logged_in"]=False
    except:  
        print("i not logined")        
        session["is_logged_in"]=False
    return render_template("home.html")

#<------------------------------------------------------------------------------> 
 #<---------------- login system------------------------------------------------> 
 #<---------------------------------------------------------------------------->      
#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")
@app.route("/login")
def login():
    return render_template("login.html")

#profile page
@app.route("/profile")
def profile():
    if session["is_logged_in"] == True:

       #getting profile
        doc_ref = db.collection(u'users').document(session["email"])
        doc = doc_ref.get()
        #getting watchlist
        wlist=doc.to_dict()['watchlist']
        watchlist=[]
        for i in wlist:
            print(i)
            doc_ref = db.collection(u'products').document(i)
            idoc = doc_ref.get()
            if idoc.exists:
                watchlist.append(idoc.to_dict())
            else:
                print(u'No such document!')
        print("----------")
        print(watchlist)


        

        return render_template("profile.html",profile =doc.to_dict(),item=watchlist)
    else:
        return redirect(url_for('login'))
@app.route("/logout")
def logout():
    session["is_logged_in"] =False
    return render_template("home.html")
@app.route("/history")
def history():
    if session["is_logged_in"] == True:

       #getting profile
        doc_ref = db.collection(u'users').document(session["email"])
        doc = doc_ref.get()
        #getting watchlist
        wlist=doc.to_dict()['watchlist']
        watchlist=[]
        for i in wlist:
            print(i)
            doc_ref = db.collection(u'products').document(i)
            idoc = doc_ref.get()
            if idoc.exists:
                watchlist.append(idoc.to_dict())
            else:
                print(u'No such document!')
        print("----------")
        print(watchlist)


        

        return render_template("history.html", my_list=watchlist)
    else:
        return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global session
        
            session["is_logged_in"] = True
            session["email"] = user["email"]
            session["uid"] = user["localId"]
            #Get the name of the user
           
            #Redirect to profile page
            return redirect(url_for('profile'))
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if session["is_logged_in"] == True:
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global session
            global session
            session["is_logged_in"] = True
            session["email"] = user["email"]
            session["uid"] = user["localId"]
            session["name"] = name
            #Append data to the firestore database
            
            doc_ref = db.collection(u'users').document(session["email"])
            doc_ref.set({
                u'name': session["name"],
                u'uid':  session["uid"],
                  u'email':  session["email"],
                u'watchlist': []
            })
            #Go to profile page
            return redirect(url_for('profile'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if session["is_logged_in"] == True:
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('register'))
 #<---------------------------------------------------------------------------->  
 #<---------------- login system {end}------------------------------------------------>    
#<---------------------------------------------------------------------------->        

@app.route('/s',methods=['POST','GET'])
def s():
  if request.method=='GET':
    result= request.args.get("search")
    amazon = search(result)
    return render_template('search-results.html',result=result, my_list=amazon)

@app.route('/alert')
def alert():  
    flaskmail(session["email"],"new alert set for item.. we will imform you if price goes down")  
    
    
@app.route('/product',methods=['POST','GET'])
def product(): 
    print(session["is_logged_in"])
    url= request.args.get("id")   
    title= request.args.get("title") 
    price= request.args.get("price") 
    image= request.args.get("image")  
    image=image.replace(' ','%20') 
    amazon = singleproduct(url,title,image,price) 
 
    if session["is_logged_in"] == True:
        doc_id=image[36:len(image)-4]
        doc_ref = db.collection('products').document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            print("doc exist")
        else:
            doc_ref.set({
                 u'link': url,
                    u'title': title,
                    u'price':  price,
                    u'image': image,
                    u'alert':[], 
                })
         #----update real mail       
        doc_ref = db.collection('users').document(session["email"])
        
        doc_ref.update({
                   
                    u'watchlist':firestore.ArrayUnion([doc_id])
              })
     
   
    return render_template('product.html',item=amazon,login=session["is_logged_in"])
@app.route('/test',methods=['POST','GET'])
def test(): 
      return render_template('product.html')   
if __name__ == "__main__":
    app.run(debug=True)
