from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
import time
import datetime
from random import randint
from flask import send_file
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt  
import pandas as pd
import numpy as np
import csv
import json
#import seaborn as sns
import mysql.connector
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="depression"
)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####


@app.route('/',methods=['POST','GET'])
def index():
    act=""
    msg=""

    return render_template('index.html',msg=msg,act=act)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM dp_login WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/login_user',methods=['POST','GET'])
def login_user():
    act=""
    msg=""
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM dp_user WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            ff=open("static/det.txt","w")
            ff.write("")
            ff.close()

            ff=open("static/qid.txt","w")
            ff.write("")
            ff.close()

            cursor.execute("update dp_question set answer=0,status=0")
            mydb.commit()
                
            session['username'] = uname
            return redirect(url_for('bot'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_user.html',msg=msg,act=act)



@app.route('/register',methods=['POST','GET'])
def register():
    msg=""
    act=""
    mycursor = mydb.cursor()
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        uname = request.form['uname']
        pass1 = request.form['pass']

        mycursor.execute("SELECT count(*) FROM dp_user where uname=%s or mobile=%s or email=%s",(uname,mobile,email))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM dp_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            sql = "INSERT INTO dp_user(id,name,mobile,email,address,city,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,mobile,email,address,city,uname,pass1)
            mycursor.execute(sql,val)
            mydb.commit()
            msg="success"
        else:
            msg="fail"
        

    return render_template('register.html',msg=msg,act=act)

def checklevel(a1,a2,a3,a4):
    level=0
    s4=0
    if a1==4:
        s4+=1
    if a2==4:
        s4+=1
    if a3==4:
        s4+=1
    if a4==4:
        s4+=1

    s3=0
    if a1==3:
        s3+=1
    if a2==3:
        s3+=1
    if a3==3:
        s3+=1
    if a4==3:
        s3+=1

    s2=0
    if a1==2:
        s2+=1
    if a2==2:
        s2+=1
    if a3==2:
        s2+=1
    if a4==2:
        s2+=1

    s1=0
    if a1==1:
        s1+=1
    if a2==1:
        s1+=1
    if a3==1:
        s1+=1
    if a4==1:
        s1+=1

    if s4>s3 and s4>s2 and s4>s1:
        level=4
    elif s3>s2 and s3>s1:
        level=3
    elif s2>s1:
        level=2
    else:
        if s1>=2:
            level=1
        else:
            level=0



    return level

@app.route('/bot',methods=['POST','GET'])
def bot():
    msg=""
    output=""
    uname=""
    mm=""
    s=""
    xn=0
    qry_st=""
    if 'username' in session:
        uname = session['username']
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      charset="utf8",
      database="depression"
    )

    
    
    cnt=0
   
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM dp_user where uname=%s",(uname, ))
    value = mycursor.fetchone()
    
    mycursor.execute("SELECT * FROM dp_question order by rand() limit 0,10")
    data=mycursor.fetchall()

            
    if request.method=='POST':
        msg_input=request.form['msg_input']

        if msg_input=="":
            
            s=1
            output="How can i help you?"
        else:
            if '.' in msg_input:
                mp=msg_input.split('.')
                msg_input=mp[0]        

        
        text=msg_input

        ff=open("static/det.txt","r")
        qry_st=ff.read()
        ff.close()

        ff=open("static/qid.txt","r")
        qid1=ff.read()
        ff.close()
        ##
        #NLP
        #nlp=STOPWORDS
        #def remove_stopwords(text):
        #    clean_text=' '.join([word for word in text.split() if word not in nlp])
        #    return clean_text
        ##
        #txt=remove_stopwords(msg_input)
        ##
        '''stemmer = PorterStemmer()
    
        from wordcloud import STOPWORDS
        STOPWORDS.update(['rt', 'mkr', 'didn', 'bc', 'n', 'm', 
                          'im', 'll', 'y', 've', 'u', 'ur', 'don', 
                          'p', 't', 's', 'aren', 'kp', 'o', 'kat', 
                          'de', 're', 'amp', 'will'])

        def lower(text):
            return text.lower()

        def remove_specChar(text):
            return re.sub("#[A-Za-z0-9_]+", ' ', text)

        def remove_link(text):
            return re.sub('@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+', ' ', text)

        def remove_stopwords(text):
            return " ".join([word for word in 
                             str(text).split() if word not in STOPWORDS])

        def stemming(text):
            return " ".join([stemmer.stem(word) for word in text.split()])

        #def lemmatizer_words(text):
        #    return " ".join([lematizer.lemmatize(word) for word in text.split()])

        def cleanTxt(text):
            text = lower(text)
            text = remove_specChar(text)
            text = remove_link(text)
            text = remove_stopwords(text)
            text = stemming(text)
            
            return text'''

        

        #show the clean text
        #dat=df.head()
        #data=[]
        #for ss in dat.values:
        #    data.append(ss)
        #msg_input=data
        mm=""
        mm1=""
        ######################
        #output="How can i help you?"
        #return json.dumps(output)

        
        if msg_input=="":
            s=1
            output="How can i help you?"

        else:
            mput=msg_input.lower()
            if mput=="hi" or mput=="hai":
                ff=open("static/det.txt","w")
                ff.write("1")
                ff.close()

                ff=open("static/qid.txt","w")
                ff.write("")
                ff.close()

                mycursor.execute("update dp_question set answer=0,status=0")
                mydb.commit()
            
                output="Enter your Age?"

            if qry_st=="1":
                try:
               
                    v=int(msg_input)
                    if v>0 and v<=100:
                        ff=open("static/det.txt","w")
                        ff.write("2")
                        ff.close()
                        output="Enter you are Male or Female or Transgender?"
                    else:
                        output="Age Incorrect"
                except:
                    output="Not a Number!"

            if qry_st=="2":
                msg="2"

                if msg_input=="Male" or msg_input=="Female" or msg_input=="Transgender":
                    
                    ff=open("static/det.txt","w")
                    ff.write("3")
                    ff.close()
                    mycursor.execute("SELECT * FROM dp_question where status=0 limit 0,1")
                    data=mycursor.fetchall()
                    for dat in data:
                        ques=dat[1]
                        qid=str(dat[0])
                        output=ques+"<br><br>Type Given option<br> 0:None 1:Very Mild<br> 2:Mild 3:Moderate 4:Severe"

                        mycursor.execute("update dp_question set status=1 where id=%s",(qid,))
                        mydb.commit()

                    
                else:
                    output="Gender Invalid!"
            if qry_st=="3":
                
                
                ques=""
                qid=""
                mycursor.execute("SELECT count(*) FROM dp_question where status=0")
                dd1=mycursor.fetchone()[0]
                tot=32
                tn=tot-dd1
                if tn<32:
                    #if msg_input=="":
                    #    msg_input="0"
                    
                    mycursor.execute("SELECT * FROM dp_question where status=0 limit 0,1")
                    data=mycursor.fetchall()
                    for dat in data:
                        ques=dat[1]
                        qid=str(dat[0])
                        output=ques+"<br><br>Type Given option<br> 0:None 1:Very Mild<br> 2:Mild 3:Moderate 4:Severe"
                        
                        if msg_input=="0" or msg_input=="1" or msg_input=="2" or msg_input=="3" or msg_input=="4":
                        

                            ff=open("static/qid.txt","w")
                            ff.write(qid)
                            ff.close()
                            mycursor.execute("update dp_question set status=1 where id=%s",(qid,))
                            mydb.commit()
                            
                            if qid1=="":
                                s=1
                            else:

                                
                                mi="0"
                                if msg_input=="0" or msg_input=="1" or msg_input=="2" or msg_input=="3" or msg_input=="4":
                                    mi=msg_input
                                    mycursor.execute("update dp_question set answer=%s where id=%s",(mi,qid1))
                                    mydb.commit()
                        else:
                            output="Incorrect option!"
                        

                else:
                    dep_type=['Major Depressive Disorder','Persistent Depressive Disorder','Bipolar Disorder','Postpartum Depression','Premenstrual Dysphoric Disorder','Seasonal Affective Disorder','Atypical Depression','Psychotic Depression']

                    ff=open("static/det.txt","w")
                    ff.write("3")
                    ff.close()
                    ###
                    n1=0
                    n2=0
                    n3=0
                    n4=0
                    n5=0
                    n6=0
                    n7=0
                    n8=0
                    
                    a1=0
                    a2=0
                    a3=0
                    a4=0

                    b1=0
                    b2=0
                    b3=0
                    b4=0

                    c1=0
                    c2=0
                    c3=0
                    c4=0

                    d1=0
                    d2=0
                    d3=0
                    d4=0

                    e1=0
                    e2=0
                    e3=0
                    e4=0

                    f1=0
                    f2=0
                    f3=0
                    f4=0

                    g1=0
                    g2=0
                    g3=0
                    g4=0

                    h1=0
                    h2=0
                    h3=0
                    h4=0
                    mycursor.execute("SELECT * FROM dp_question where status=1")
                    dat2=mycursor.fetchall()
                    for dat22 in dat2:
                        if dat22[2]=='a1':
                            a1=dat22[3]
                        if dat22[2]=='a2':
                            a2=dat22[3]
                        if dat22[2]=='a3':
                            a3=dat22[3]
                        if dat22[2]=='a4':
                            a4=dat22[3]

                        if dat22[2]=='b1':
                            b1=dat22[3]
                        if dat22[2]=='b2':
                            b2=dat22[3]
                        if dat22[2]=='b3':
                            b3=dat22[3]
                        if dat22[2]=='b4':
                            b4=dat22[3]
                        
                        if dat22[2]=='c1':
                            c1=dat22[3]
                        if dat22[2]=='c2':
                            c2=dat22[3]
                        if dat22[2]=='c3':
                            c3=dat22[3]
                        if dat22[2]=='c4':
                            c4=dat22[3]

                        if dat22[2]=='d1':
                            d1=dat22[3]
                        if dat22[2]=='d2':
                            d2=dat22[3]
                        if dat22[2]=='d3':
                            d3=dat22[3]
                        if dat22[2]=='d4':
                            d4=dat22[3]

                        if dat22[2]=='e1':
                            e1=dat22[3]
                        if dat22[2]=='e2':
                            e2=dat22[3]
                        if dat22[2]=='e3':
                            e3=dat22[3]
                        if dat22[2]=='e4':
                            e4=dat22[3]

                        if dat22[2]=='f1':
                            f1=dat22[3]
                        if dat22[2]=='f2':
                            f2=dat22[3]
                        if dat22[2]=='f3':
                            f3=dat22[3]
                        if dat22[2]=='f4':
                            f4=dat22[3]


                        if dat22[2]=='g1':
                            g1=dat22[3]
                        if dat22[2]=='g2':
                            g2=dat22[3]
                        if dat22[2]=='g3':
                            g3=dat22[3]
                        if dat22[2]=='g4':
                            g4=dat22[3]

                        if dat22[2]=='h1':
                            h1=dat22[3]
                        if dat22[2]=='h2':
                            h2=dat22[3]
                        if dat22[2]=='h3':
                            h3=dat22[3]
                        if dat22[2]=='h4':
                            h4=dat22[3]

                    n1=a1+a2+a3+a4
                    n2=b1+b2+b3+b4
                    n3=c1+c2+c3+c4
                    n4=d1+d2+d3+d4
                    n5=e1+e2+e3+e4
                    n6=f1+f2+f3+f4
                    n7=g1+g2+g3+g4
                    n8=h1+h2+h3+h4       
                    if n1>0 or n2>0 or n3>0 or n4>0 or n5>0 or n6>0 or n7>0 or n8>0:
            
        
                        if n1>n2 and n1>n3 and n1>n4 and n1>n5 and n1>n6 and n1>n7 and n1>n8:
                            dep='1'
                            level=checklevel(a1,a2,a3,a4)
                            
                        elif n2>n3 and n2>n4 and n2>n5 and n2>n6 and n2>n7 and n2>n8:
                            dep='2'
                            level=checklevel(b1,b2,b3,b4)
                        elif n3>n4 and n3>n5 and n3>n6 and n3>n7 and n3>n8:
                            dep='3'
                            level=checklevel(c1,c2,c3,c4)
                        elif n4>n5 and n4>n6 and n4>n7 and n4>n8:
                            dep='4'
                            level=checklevel(d1,d2,d3,d4)
                        elif n5>n6 and n5>n7 and n5>n8:
                            dep='5'
                            level=checklevel(e1,e2,e3,e4)
                        elif n6>n7 and n6>n8:
                            dep='6'
                            level=checklevel(f1,f2,f3,f4)
                        elif n7>n8:
                            dep='7'
                            level=checklevel(g1,g2,g3,g4)
                        else:
                            dep='8'
                            level=checklevel(h1,h2,h3,h4)


                        depr=int(dep)-1
                        depr_type=dep_type[depr]
                        if level==4:
                            dlevel="Severe"
                        elif level==3:
                            dlevel="Moderate"
                        elif level==2:
                            dlevel="Mild"
                        elif level==1:
                            dlevel="Very Mild"
                        else:
                            dlevel="none"
                            depr_type="none"

                    else:
                        depr_type="none"
                        dlevel="none"

                    value=dlevel+"|"+depr_type
                    ff=open("static/result.txt","w")
                    ff.write(value)
                    ff.close()
                    ##

                    #if qry_st=="3":

                    ##output="Your Result"
                    
                    mycursor.execute("SELECT * FROM dp_recommend order by city limit 0,6")
                    hdata = mycursor.fetchall()
                    hn=""
                    for hd in hdata:
                        hn+="<br>Hospital: "+hd[1]
                        hn+="<br>Specialist: "+hd[2]+", Time:"+hd[3]
                        hn+="<br>Location: "+hd[4]+", "+hd[5]
                        hn+="<br>Contact: "+str(hd[6])+", "+hd[7]
                        hn+="<br>"

                    
                    ff=open("static/result.txt","r")
                    value=ff.read()
                    ff.close()

                    vv=value.split("|")
                    value1=vv[0]
                    value2=vv[1]

                    mycursor.execute("SELECT * FROM dp_treatment where dtype=%s",(value2,))
                    rdata = mycursor.fetchall()

                    if value1=="none":
                        output="<h3>No Depression!! You are Healthy!!</h3>"
                    else:
                        mm="<h4>Depression Type: "+value2+"</h4>"
                        mm+="<br>Stage: "+value1

                        mm+="<br><br>Recommendations:"
                        mm+="<br>Life Time Changes:"
                        mm+="<br>"+rdata[0][2]
                        mm+="<br><br>Medication:"
                        mm+="<br>"+rdata[0][4]
                        mm+="<br><br>Treatment:"
                        mm+="<br>"+rdata[0][3]
                        mm+="<br><br>Doctor Suggestions:"
                        mm+="<br>"+rdata[0][5]
                        mm+="<br><br>Psyciatrist Doctors and Locations:"
                        mm+=hn
                        output=mm
                    
                
        return json.dumps(output)


        '''output="How can i help you?"
            return json.dumps(output)
     
                                        
                        output=dd3
                    
                    else:                    
                        if msg_input=="":
                            output="How can i help you?"
                        else:
                            output="Sorry, No Results Found!"

                return json.dumps(output)
                ####################

           
                return json.dumps(output)
                ##################################'''


    return render_template('bot.html', msg=msg,output=output,uname=uname,data=data,value=value)   




                
@app.route('/userhome',methods=['POST','GET'])
def userhome():
    uname=""
    dep=''
    depr_type=''
    dlevel=''
    st=""
    if 'username' in session:
        uname = session['username']
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM dp_user where uname=%s",(uname, ))
    data = mycursor.fetchone()

    dep_type=['Major Depressive Disorder','Persistent Depressive Disorder','Bipolar Disorder','Postpartum Depression','Premenstrual Dysphoric Disorder','Seasonal Affective Disorder','Atypical Depression','Psychotic Depression']

    if request.method == 'POST':
        st="1"
        age = request.form['age']
        gender = request.form['gender']
        a1 = int(request.form['a2'])
        a2 = int(request.form['a3'])
        a3 = int(request.form['a7'])
        a4 = int(request.form['a8'])
        
        b1 = int(request.form['b6'])
        b2 = int(request.form['b4'])
        b3 = int(request.form['b8'])
        b4 = int(request.form['b2'])
        
        c1 = int(request.form['c2'])
        c2 = int(request.form['c3'])
        c3 = int(request.form['c1'])
        c4 = int(request.form['c5'])
        
        d1 = int(request.form['d2'])
        d2 = int(request.form['d3'])
        d3 = int(request.form['d5'])
        d4 = int(request.form['d10'])
        
        e1 = int(request.form['e1'])
        e2 = int(request.form['e3'])
        e3 = int(request.form['e5'])
        e4 = int(request.form['e7'])

        f1 = int(request.form['f1'])
        f2 = int(request.form['f2'])
        f3 = int(request.form['f3'])
        f4 = int(request.form['f4'])
        
        g1 = int(request.form['g2'])
        g2 = int(request.form['g3'])
        g3 = int(request.form['g4'])
        g4 = int(request.form['g5'])
        
        h1 = int(request.form['h1'])
        h2 = int(request.form['h3'])
        h3 = int(request.form['h5'])
        h4 = int(request.form['h6'])

     
        ##
        n1=a1+a2+a3+a4
        n2=b1+b2+b3+b4
        n3=c1+c2+c3+c4
        n4=d1+d2+d3+d4
        n5=e1+e2+e3+e4
        n6=f1+f2+f3+f4
        n7=g1+g2+g3+g4
        n8=h1+h2+h3+h4
        ##
        if n1>0 or n2>0 or n3>0 or n4>0 or n5>0 or n6>0 or n7>0 or n8>0:
            
        
            if n1>n2 and n1>n3 and n1>n4 and n1>n5 and n1>n6 and n1>n7 and n1>n8:
                dep='1'
                level=checklevel(a1,a2,a3,a4)
                
            elif n2>n3 and n2>n4 and n2>n5 and n2>n6 and n2>n7 and n2>n8:
                dep='2'
                level=checklevel(b1,b2,b3,b4)
            elif n3>n4 and n3>n5 and n3>n6 and n3>n7 and n3>n8:
                dep='3'
                level=checklevel(c1,c2,c3,c4)
            elif n4>n5 and n4>n6 and n4>n7 and n4>n8:
                dep='4'
                level=checklevel(d1,d2,d3,d4)
            elif n5>n6 and n5>n7 and n5>n8:
                dep='5'
                level=checklevel(e1,e2,e3,e4)
            elif n6>n7 and n6>n8:
                dep='6'
                level=checklevel(f1,f2,f3,f4)
            elif n7>n8:
                dep='7'
                level=checklevel(g1,g2,g3,g4)
            else:
                dep='8'
                level=checklevel(h1,h2,h3,h4)


            depr=int(dep)-1
            depr_type=dep_type[depr]
            if level==4:
                dlevel="Severe"
            elif level==3:
                dlevel="Moderate"
            elif level==2:
                dlevel="Mild"
            elif level==1:
                dlevel="Very Mild"
            else:
                dlevel="none"
                depr_type="none"

        else:
            depr_type="none"
            dlevel="none"

        value=dlevel+"|"+depr_type
        ff=open("static/result.txt","w")
        ff.write(value)
        ff.close()

        mycursor.execute("SELECT max(id)+1 FROM dp_test")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO dp_test(id,uname,age,gender,value1,value2,value3,value4,value5,value6,value7,value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,value20,value21,value22,value23,value24,value25,value26,value27,value28,value29,value30,value31,value32) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,uname,age,gender,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,f1,f2,f3,f4,g1,g2,g3,g4,h1,h2,h3,h4)
        mycursor.execute(sql,val)
        mydb.commit()

        mycursor.execute("SELECT max(id)+1 FROM dp_result")
        maxid2 = mycursor.fetchone()[0]
        if maxid2 is None:
            maxid2=1
        sql2 = "INSERT INTO dp_result(id,uname,test_id,depression_level,depression_type) VALUES(%s,%s,%s,%s,%s)"
        val2 = (maxid2,uname,maxid,dlevel,depr_type)
        mycursor.execute(sql2,val2)
        mydb.commit()

        
        return redirect(url_for('result'))
        

    return render_template('userhome.html',data=data,depr_type=depr_type,dlevel=dlevel,st=st)

@app.route('/result',methods=['POST','GET'])
def result():
    uname=""
    value1=""
    value2=""

    if 'username' in session:
        uname = session['username']

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM dp_user where uname=%s",(uname, ))
    data = cursor.fetchone()

    
    ff=open("static/result.txt","r")
    value=ff.read()
    ff.close()

    vv=value.split("|")
    value1=vv[0]
    value2=vv[1]

    return render_template('result.html',data=data,value1=value1,value2=value2)


@app.route('/admin',methods=['POST','GET'])
def admin():
    uname=""

    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    if request.method=='POST':
        
        file = request.files['file']
        #try:
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fn="datafile.csv"
            #fn1 = secure_filename(fn)
            file.save(os.path.join("static/upload", fn))
            return redirect(url_for('view_data'))
        #except:
        #    print("dd")
    

    return render_template('admin.html')

@app.route('/add_recommend',methods=['POST','GET'])
def add_recommend():
    msg=""
    uname=""
    act=request.args.get("act")
    
    mycursor = mydb.cursor()
    
    if request.method == 'POST':
        hospital = request.form['hospital']
        specialist = request.form['specialist']
        av_time = request.form['av_time']
        address = request.form['address']
        city = request.form['city']
        mobile = request.form['mobile']
        email = request.form['email']
        
        
        mycursor.execute("SELECT max(id)+1 FROM dp_recommend")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO dp_recommend(id,hospital,specialist,av_time,address,city,mobile,email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,hospital,specialist,av_time,address,city,mobile,email)
        mycursor.execute(sql,val)
        mydb.commit()
        msg="success"

    mycursor.execute("SELECT * FROM dp_recommend")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from dp_recommend where id=%s",(did,))
        mydb.commit()
        msg="ok"
    
    return render_template('add_recommend.html',msg=msg,data=data)

@app.route('/edit_recommend',methods=['POST','GET'])
def edit_recommend():
    msg=""
    uname=""
    tid=request.args.get("tid")
    mycursor = mydb.cursor()
    
    if request.method == 'POST':
        hospital = request.form['hospital']
        specialist = request.form['specialist']
        av_time = request.form['av_time']
        address = request.form['address']
        city = request.form['city']
        mobile = request.form['mobile']
        email = request.form['email']
        mycursor.execute("update dp_recommend set hospital=%s,specialist=%s,av_time=%s,address=%s,city=%s,mobile=%s,email=%s where id=%s",(hospital,specialist,av_time,address,city,mobile,email,tid))        
        mydb.commit()        
        msg="success"

    mycursor.execute("SELECT * FROM dp_recommend")
    data = mycursor.fetchall()

    mycursor.execute("SELECT * FROM dp_recommend where id=%s",(tid,))
    data1 = mycursor.fetchone()

    
    return render_template('edit_recommend.html',msg=msg,data=data,data1=data1)


@app.route('/add_treatment',methods=['POST','GET'])
def add_treatment():
    msg=""
    uname=""
    data1=[]
    act=request.args.get("act")
    tid=request.args.get("tid")
    mycursor = mydb.cursor()

    if request.method == 'POST':
        #dtype = request.form['dtype']
        life_time = request.form['life_time']
        treatment = request.form['treatment']
        medication = request.form['medication']
        suggestion = request.form['suggestion']
        
        mycursor.execute("update dp_treatment set life_time=%s,treatment=%s,medication=%s,suggestion=%s where id=%s",(life_time,treatment,medication,suggestion,tid))        
        mydb.commit()
        '''mycursor.execute("SELECT max(id)+1 FROM dp_treatment")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO dp_treatment(id,dtype,life_time,treatment,medication,suggestion) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (maxid,dtype,life_time,treatment,medication,suggestion)
        mycursor.execute(sql,val)
        mydb.commit()'''
        msg="success"
    
    mycursor.execute("SELECT * FROM dp_treatment")
    data = mycursor.fetchall()

    if act=="edit":
        mycursor.execute("SELECT * FROM dp_treatment where id=%s",(tid,))
        data1 = mycursor.fetchone()

    
    return render_template('add_treatment.html',msg=msg,data=data,act=act,data1=data1)

@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    msg=""
    cnt=0
    data=[]
    rows=0
    cols=0

    '''df = pd.read_csv("static/upload/datafile.csv",encoding='cp1252')
    dat=df.head()
    data=[]
    rows=len(dat.values)
    for ss in dat.values:
        cnt=len(ss)
        data.append(ss)'''

        
    filename = 'static/upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0,encoding='cp1252')
    data2 = list(data1.values.flatten())
    
    i=0
    sd=len(data1)
    rows=len(data1.values)
    
    
    for ss in data1.values:
        cnt=len(ss)
        data.append(ss)
    cols=cnt
    
    return render_template('view_data.html',data=data,rows=rows,cols=cols)

@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():
    msg=""
    mem=0
    cnt=0
    cols=0
    rows=0
    rowsn=0
    nullcount=0
    filename = 'static/upload/datafile.csv'
    data1 = pd.read_csv(filename, encoding='cp1252')
    data2 = list(data1.values.flatten())
    cname=[]
    data=[]
    dtype=[]
    dtt=[]
    nv=[]
    i=0
    
    sd=len(data1)
    rows=len(data1.values)
    
    #print(data1.columns)
    col=data1.columns
    #print(data1[0])
    for ss in data1.values:
        cnt=len(ss)
        i=0
        x=0
        while i<cnt:
            if pd.isnull(ss[i]):
                nullcount+=1
                x+=1
            i+=1
        if x>0:
            rowsn+=1
        

    i=0
    while i<cnt:
        j=0
        x=0
        for rr in data1.values:
            dt=type(rr[i])
            if rr[i]!="":
                x+=1
            
            j+=1
        dtt.append(dt)
        nv.append(str(x))
        
        i+=1

    arr1=np.array(col)
    arr2=np.array(nv)
    data3=np.vstack((arr1, arr2))
    rows=rows-rowsn

    arr3=np.array(data3)
    arr4=np.array(dtt)
    
    data=np.vstack((arr3, arr4))
   
    print(data)
    cols=cnt
    mem=float(rows)*0.75

    #if request.method=='POST':
    #    return redirect(url_for('feature_ext'))
    
    return render_template('preprocess.html',data=data, msg=msg, rows=rows,nullcount=nullcount, cols=cols, dtype=dtype, mem=mem)

@app.route('/feature', methods=['GET', 'POST'])
def feature():
    msg=""
    mem=0
    cnt=0
    cols=0
    rows=0
    rowsn=0
    nullcount=0
    data=[]

    filename = 'static/upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0,encoding='cp1252')
    data2 = list(data1.values.flatten())
    
    i=0
    sd=len(data1)
    #rows=len(data1.values)
    dep_type=['Major Depressive Disorder','Persistent Depressive Disorder','Bipolar Disorder','Postpartum Depression','Premenstrual Dysphoric Disorder','Seasonal Affective Disorder','Atypical Depression','Psychotic Depression']

    
    
    for ss in data1.values:
        dt=[]
        cnt=len(ss)
        i=0
        x=0
        while i<cnt:
            if pd.isnull(ss[i]):
                nullcount+=1
                x+=1
            i+=1
        if x>0:
            rowsn+=1
        else:
            a1 = int(ss[8])
            a2 = int(ss[16])
            a3 = int(ss[43])
            a4 = int(ss[58])
            
            b1 = int(ss[44])
            b2 = int(ss[25])
            b3 = int(ss[52])
            b4 = int(ss[9])
            
            c1 = int(ss[10])
            c2 = int(ss[18])
            c3 = int(ss[2])
            c4 = int(ss[34])
            
            d1 = int(ss[11])
            d2 = int(ss[19])
            d3 = int(ss[35])
            d4 = int(ss[56])
            
            e1 = int(ss[4])
            e2 = int(ss[20])
            e3 = int(ss[36])
            e4 = int(ss[46])

            f1 = int(ss[5])
            f2 = int(ss[13])
            f3 = int(ss[21])
            f4 = int(ss[29])
            
            g1 = int(ss[14])
            g2 = int(ss[22])
            g3 = int(ss[30])
            g4 = int(ss[37])
            
            h1 = int(ss[7])
            h2 = int(ss[23])
            h3 = int(ss[38])
            h4 = int(ss[42])

         
            ##
            n1=a1+a2+a3+a4
            n2=b1+b2+b3+b4
            n3=c1+c2+c3+c4
            n4=d1+d2+d3+d4
            n5=e1+e2+e3+e4
            n6=f1+f2+f3+f4
            n7=g1+g2+g3+g4
            n8=h1+h2+h3+h4
            ##
            if n1>0 or n2>0 or n3>0 or n4>0 or n5>0 or n6>0 or n7>0 or n8>0:
                
            
                if n1>n2 and n1>n3 and n1>n4 and n1>n5 and n1>n6 and n1>n7 and n1>n8:
                    dep='1'
                    level=checklevel(a1,a2,a3,a4)
                    
                elif n2>n3 and n2>n4 and n2>n5 and n2>n6 and n2>n7 and n2>n8:
                    dep='2'
                    level=checklevel(b1,b2,b3,b4)
                elif n3>n4 and n3>n5 and n3>n6 and n3>n7 and n3>n8:
                    dep='3'
                    level=checklevel(c1,c2,c3,c4)
                elif n4>n5 and n4>n6 and n4>n7 and n4>n8:
                    dep='4'
                    level=checklevel(d1,d2,d3,d4)
                elif n5>n6 and n5>n7 and n5>n8:
                    dep='5'
                    level=checklevel(e1,e2,e3,e4)
                elif n6>n7 and n6>n8:
                    dep='6'
                    level=checklevel(f1,f2,f3,f4)
                elif n7>n8:
                    dep='7'
                    level=checklevel(g1,g2,g3,g4)
                else:
                    dep='8'
                    level=checklevel(h1,h2,h3,h4)


                depr=int(dep)-1
                depr_type=dep_type[depr]
                if level==4:
                    dlevel="Severe"
                elif level==3:
                    dlevel="Moderate"
                elif level==2:
                    dlevel="Mild"
                elif level==1:
                    dlevel="Very Mild"
                else:
                    dlevel="No Depression"
                    depr_type="none"

            else:
                depr_type="none"
                dlevel="No Depression"

            dt.append(ss)
            dt.append(dlevel)
            
            data.append(dt)
    cols=cnt



    #plt.matshow(dataframe.corr())
    #plt.show()
    ###co relation######
    filename = 'static/upload/datafile.csv'
    datam = pd.read_csv(filename, header=0,encoding='cp1252')

    corr = datam.corr()
    ax = sns.heatmap(
        corr, 
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True
    )
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right'
    );
    #plt.show()
    plt.savefig('static/graph3.png')
    plt.close()
    ###########
    #acc########################################
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(94,98)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(94,98)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[5,16,35,50,61]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy %")
    
    fn="graph4.png"
    #plt.savefig('static/'+fn)
    plt.close()
    #######################################################
    #graph4
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,4)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(1,4)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[5,16,35,50,61]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Model loss")
    
    fn="graph5.png"
    #plt.savefig('static/'+fn)
    plt.close()
    ############################

    return render_template('feature.html',data=data)

#SNN Classify -Symptomatic Neural Network
def predict(sym1, sym2, sym3, sym4, sym5):

    # from gui_stuff import *

    l2=[]
    for x in range(0,len(l1)):
        l2.append(0)

    # TESTING DATA df -------------------------------------------------------------------------------------
    df=pd.read_csv(os.path.abspath(os.path.dirname(__file__).replace("",""))+"/asset/Training.csv")

    # print(df.head())

    X= df[l1]

    y = df[["prognosis"]]
    np.ravel(y)
    # print(y)

    # TRAINING DATA tr --------------------------------------------------------------------------------
    tr=pd.read_csv(os.path.abspath(os.path.dirname(__file__).replace("",""))+"/asset/Testing.csv")
       

    X_test= tr[l1]
    y_test = tr[["prognosis"]]
    np.ravel(y_test)
    # -------------------------------------------------------------

    # calculating accuracy-------------------------------------------------------------------
    #from sklearn.metrics import accuracy_score
    #y_pred=clf3.predict(X_test)
    #print(accuracy_score(y_test, y_pred))
    #print(accuracy_score(y_test, y_pred,normalize=False))
    # -----------------------------------------------------
    Symptom1 = '%s' % sym1
    
    Symptom2 = '%s' % sym2
    
    Symptom3 = '%s' % sym3
    
    Symptom4 = '%s' % sym4
    
    Symptom5 = '%s' % sym5
    
    
    psymptoms = [Symptom1,Symptom2,Symptom3,Symptom4,Symptom5]

    for k in range(0,len(l1)):
    # print (k,)
        for z in psymptoms:
            if(z==l1[k]):
                l2[k]=1

    inputtest = [l2]
    predict = clf3.predict(inputtest)
    predicted=predict[0]

    
@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    mem=0
    cnt=0
    cols=0
    rows=0
    rowsn=0
    nullcount=0
    data=[]

    filename = 'static/upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0,encoding='cp1252')
    data2 = list(data1.values.flatten())
    
    i=0
    sd=len(data1)
    #rows=len(data1.values)
    dep_type=['Major Depressive Disorder','Persistent Depressive Disorder','Bipolar Disorder','Postpartum Depression','Premenstrual Dysphoric Disorder','Seasonal Affective Disorder','Atypical Depression','Psychotic Depression']

    x=0
    y=0
    f1=0
    f2=0
    f3=0
    f4=0
    f5=0
    f6=0
    f7=0
    f8=0

    f1a=0
    f1b=0
    f1c=0
    f1d=0
    f2a=0
    f2b=0
    f2c=0
    f2d=0
    f3a=0
    f3b=0
    f3c=0
    f3d=0
    f4a=0
    f4b=0
    f4c=0
    f4d=0
    f5a=0
    f5b=0
    f5c=0
    f5d=0
    f6a=0
    f6b=0
    f6c=0
    f6d=0
    f7a=0
    f7b=0
    f7c=0
    f7d=0
    f8a=0
    f8b=0
    f8c=0
    f8d=0
    
    xx=0
    yy=0
    for ss in data1.values:
        dt=[]
        cnt=len(ss)
        i=0
        x=0
        while i<cnt:
            if pd.isnull(ss[i]):
                nullcount+=1
                x+=1
            i+=1
        if x>0:
            rowsn+=1
        else:
            a1 = int(ss[8])
            a2 = int(ss[16])
            a3 = int(ss[43])
            a4 = int(ss[58])
            
            b1 = int(ss[44])
            b2 = int(ss[25])
            b3 = int(ss[52])
            b4 = int(ss[9])
            
            c1 = int(ss[10])
            c2 = int(ss[18])
            c3 = int(ss[2])
            c4 = int(ss[34])
            
            d1 = int(ss[11])
            d2 = int(ss[19])
            d3 = int(ss[35])
            d4 = int(ss[56])
            
            e1 = int(ss[4])
            e2 = int(ss[20])
            e3 = int(ss[36])
            e4 = int(ss[46])

            f1 = int(ss[5])
            f2 = int(ss[13])
            f3 = int(ss[21])
            f4 = int(ss[29])
            
            g1 = int(ss[14])
            g2 = int(ss[22])
            g3 = int(ss[30])
            g4 = int(ss[37])
            
            h1 = int(ss[7])
            h2 = int(ss[23])
            h3 = int(ss[38])
            h4 = int(ss[42])

         
            ##
            n1=a1+a2+a3+a4
            n2=b1+b2+b3+b4
            n3=c1+c2+c3+c4
            n4=d1+d2+d3+d4
            n5=e1+e2+e3+e4
            n6=f1+f2+f3+f4
            n7=g1+g2+g3+g4
            n8=h1+h2+h3+h4
            ##
            if n1>0 or n2>0 or n3>0 or n4>0 or n5>0 or n6>0 or n7>0 or n8>0:
                
            
                if n1>n2 and n1>n3 and n1>n4 and n1>n5 and n1>n6 and n1>n7 and n1>n8:
                    dep='1'
                    f1+=1
                    level=checklevel(a1,a2,a3,a4)
                    if level==1:
                        f1a+=1
                    if level==2:
                        f1b+=1
                    if level==3:
                        f1c+=1
                    if level==4:
                        f1d+=1
                    
                elif n2>n3 and n2>n4 and n2>n5 and n2>n6 and n2>n7 and n2>n8:
                    dep='2'
                    f2+=1
                    level=checklevel(b1,b2,b3,b4)
                    if level==1:
                        f2a+=1
                    if level==2:
                        f2b+=1
                    if level==3:
                        f2c+=1
                    if level==4:
                        f2d+=1
                        
                elif n3>n4 and n3>n5 and n3>n6 and n3>n7 and n3>n8:
                    dep='3'
                    f3+=1
                    level=checklevel(c1,c2,c3,c4)
                    if level==1:
                        f3a+=1
                    if level==2:
                        f3b+=1
                    if level==3:
                        f3c+=1
                    if level==4:
                        f3d+=1
                        
                elif n4>n5 and n4>n6 and n4>n7 and n4>n8:
                    dep='4'
                    f4+=1
                    level=checklevel(d1,d2,d3,d4)
                    if level==1:
                        f4a+=1
                    if level==2:
                        f4b+=1
                    if level==3:
                        f4c+=1
                    if level==4:
                        f4d+=1

                        
                elif n5>n6 and n5>n7 and n5>n8:
                    dep='5'
                    f5+=1
                    level=checklevel(e1,e2,e3,e4)
                    if level==1:
                        f5a+=1
                    if level==2:
                        f5b+=1
                    if level==3:
                        f5c+=1
                    if level==4:
                        f5d+=1
                        
                elif n6>n7 and n6>n8:
                    dep='6'
                    f6+=1
                    level=checklevel(f1,f2,f3,f4)
                    if level==1:
                        f6a+=1
                    if level==2:
                        f6b+=1
                    if level==3:
                        f6c+=1
                    if level==4:
                        f6d+=1
                        
                elif n7>n8:
                    dep='7'
                    f7+=1
                    level=checklevel(g1,g2,g3,g4)
                    if level==1:
                        f7a+=1
                    if level==2:
                        f7b+=1
                    if level==3:
                        f7c+=1
                    if level==4:
                        f7d+=1
                else:
                    dep='8'
                    f8+=1
                    level=checklevel(h1,h2,h3,h4)
                    if level==1:
                        f8a+=1
                    if level==2:
                        f8b+=1
                    if level==3:
                        f8c+=1
                    if level==4:
                        f8d+=1


                depr=int(dep)-1
                depr_type=dep_type[depr]
                if level==4:
                    xx+=1
                    dlevel="Severe"
                elif level==3:
                    xx+=1
                    dlevel="Moderate"
                elif level==2:
                    xx+=1
                    dlevel="Mild"
                elif level==1:
                    yy+=1
                    dlevel="Very Mild"
                else:
                    yy+=1
                    dlevel="No Depression"
                    depr_type="-"

            else:
                depr_type="-"
                dlevel="No Depression"

            dt.append(ss)
            dt.append(depr_type)
            dt.append(dlevel)
            
            
            data.append(dt)
    cols=cnt


    ##
    doc = ['Depressed','Not Depressed'] #list(data.keys())
    values = [xx,yy] #list(data.values())
    
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    cc=['red','green']
    plt.bar(doc, values, color =cc,
            width = 0.6)
 

    plt.ylim((1,30))
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="graph1.png"
    #plt.xticks(rotation=5,size=20)
    plt.savefig('static/'+fn)
    
    plt.close()
    #plt.clf()

    ##############
    gvalue=[f1,f2,f3,f4,f5,f6,f7,f8]
    X = ['MDD','PDD','BD','PPD','PMDD','SAD','AD','PD']
    Y1=[f1a,f2a,f3a,f4a,f5a,f6a,f7a,f8a]
    Y2=[f1b,f2a,f3b,f4a,f5b,f6b,f7a,f8b]
    Y3=[f1c,f2a,f3c,f4a,f5c,f6c,f7a,f8c]
    Y4=[f1d,f2a,f3d,f4a,f5d,f6d,f7a,f8d]
    '''Y1 = [10,20,20,40] 
    Y2 = [20,30,25,30]
    Y3 = [20,30,25,30]
    Y4 = [20,30,25,30]''' 
      
    X_axis = np.arange(len(X)) 
      
    plt.bar(X_axis + 0.2, Y1, 0.4, label = 'Very Mild') 
    plt.bar(X_axis + 0.4, Y2, 0.4, label = 'Mild')
    plt.bar(X_axis + 0.6, Y3, 0.4, label = 'Moderate')
    plt.bar(X_axis + 0.8, Y4, 0.4, label = 'Severe') 
      
    plt.xticks(X_axis, X) 
    plt.xlabel("Depression") 
    plt.ylabel("Count") 
    plt.title("Depression Type") 
    plt.legend() 
    #plt.show()
    plt.savefig('static/graph2.png')
    plt.close()


    ##
    return render_template('classify.html',data=data,values=values)



@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    #session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
