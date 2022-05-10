from flask import Flask, render_template, request, redirect, url_for, session ,g
import pymysql
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'any random string'
app.permanent_session_lifetime = timedelta(seconds=5)

def getConnection ():
    return pymysql.connect(
        host = 'localhost',
        db = 'qrcode',
        user = 'root',
        password = '',
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor
		)


iplist = []


@app.route('/')
def home():
    return render_template("test.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    ip = request.args.get('ip')
    print(iplist)
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    date_times = date_time.strftime("%Y-%m-%d,%H:%M:%S")
    date,time = date_times.split(',')
    
    
    
    
    if ip == "" or ip is None:
        print("index")
        return redirect(url_for('home'))
    
             
    else:
        if ip in iplist:
            print("onetime with session")
            count = 0
            connection = getConnection()
            sql = "SELECT * FROM visitor WHERE ip = '%s' AND employeeid ='' AND date = '%s'" %(ip,date)
            cursor = connection.cursor()
            cursor.execute(sql)
            vi = cursor.fetchall()
            for i in vi:
                count += 1//1
            print(count)
                
            if count == 0:
                print("Onetime เหลือกดออก")
                connection = getConnection() #119.76.14.172 
                sql = "SELECT * FROM visitor WHERE ip = '%s' AND date = '%s' AND status ='เหลือกดออก'" %(ip,date)
                cursor = connection.cursor()
                cursor.execute(sql)
                hi = cursor.fetchone()
                print(hi)
                return render_template("successin.html" ,hi=hi)
            elif count > 0 :
                print("Onetime เหลือกรอกรหัสพนักงาน") 
                return render_template("profilein.html" ,vi=vi)   
                
                
            
        print("Ontime no session")    
        return render_template("index.html" ,ip=ip ,date=date ,time=time )


    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    ip = request.args.get('ip')
    name = request.args.get('name')
    date = request.args.get('date')
    iplist.remove(ip)
    
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    date_times = date_time.strftime("%Y-%m-%d,%H:%M:%S")
    day,time = date_times.split(',')
    
    connection = getConnection()
    sql = "UPDATE visitor SET timeout = '%s' ,status = 'ออกไปแล้ว' WHERE ip = '%s' AND name = '%s' AND timeout ='' AND date = '%s'" %(time,ip,name,date)
    print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    session.clear()
    return render_template("test.html")


@app.route('/saveVisitor', methods=['GET', 'POST'])
def saveVisitor():
    ip = request.args.get('ip')
    
    name = request.args.get('name')
    if name=="" or ip is None:
        return redirect(url_for('home'))
    else :
        iplist.append(ip)
        date = request.args.get('date')
        timein = request.args.get('time')
        department = request.args.get("department")
        detail = request.args.get('detail')
        phonenumber = request.args.get('phonenumber')
        connection = getConnection()
        sql = "INSERT INTO visitor(ip, name, detail ,date ,timein ,department ,phonenumber,status) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (ip, name, detail ,date ,timein ,department ,phonenumber,"เหลือกรอกชื่อพนักงาน")
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return render_template("profile.html" ,name=name ,date=date ,timein=timein ,department=department ,detail=detail ,phonenumber=phonenumber,ip=ip)

@app.route('/saveemployee', methods=['GET', 'POST'])
def saveemployee():
    employeeid = request.args.get('employeeid')
    ip = request.args.get('ip')
    name = request.args.get('name')
    date = request.args.get('date')
    timein = request.args.get('timein')
    department = request.args.get("department")
    detail = request.args.get('detail')
    phonenumber = request.args.get('phonenumber')
    if ip is None:
        return redirect(url_for('home'))
    else:
        connection = getConnection()
        sql = f"UPDATE visitor SET employeeid = '{employeeid}' , status ='เหลือกดออก' WHERE ip = '{ip}' AND name = '{name}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return render_template("success.html",name=name,date=date,timein=timein,department=department,detail=detail,phonenumber=phonenumber,employeeid=employeeid,ip=ip)
    

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/table')
def table():
    return render_template("table.html")

@app.route('/chart')
def chart():
    return render_template("chart.html")

@app.route('/success')
def success():
    employeeid = request.args.get('employeeid')
    ip = request.args.get('ip')
    if not ip:
        return redirect(url_for('home'))
    else :
        name = request.args.get('name')
        connection = getConnection()
        sql = f"UPDATE visitor SET employeeid = '{employeeid}' WHERE ip = '{ip}' AND name = '{name}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return render_template("success.html")



if __name__ == '__main__':
    app.run(debug=True)