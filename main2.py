from flask import Flask, render_template, request, redirect, url_for
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
ipdate = []


@app.route('/')
def home():
    return render_template("test.html")

@app.route('/login', methods=['GET', 'POST'])
def login():

    ip = request.args.get('ip')
    print(iplist)
    print(ipdate)
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    date_times = date_time.strftime("%Y-%m-%d,%H:%M:%S")
    date,time = date_times.split(',')
    
    times = time.split(":")[0]
    t = int(times)

    
    if ip == "" or ip is None:
        print("index")
        return redirect(url_for('home'))
    
             
    else:
        if ip in iplist :
            d = iplist.index(ip)
            if date == ipdate[d]:
                if 6 <= t < 17:
                    print("อยู่ในเวลารายการ")
                    count = 0
                    connection = getConnection()
                    sql = "SELECT * FROM visitor WHERE ip = '%s' AND employeeid ='' AND date = '%s'" %(ip,date) ##
                    cursor = connection.cursor()
                    cursor.execute(sql)
                    vi = cursor.fetchall()
                    for i in vi:
                        count += 1
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
                else:
                    connection = getConnection()
                    sql = "UPDATE visitor SET timeout = '17:00:00' ,status = 'ระบบตัด session ตอน 17.00 น.' WHERE ip = '%s' AND timeout ='' AND date = '%s'" %(ip,date)
                    print(sql)
                    cursor = connection.cursor()
                    cursor.execute(sql)
                    connection.commit()
                    return redirect(url_for('home'))
            else:
                    connection = getConnection()
                    sql = "UPDATE visitor SET timeout = '17:00:00' ,status = 'ล็อคอินวันอื่นระบบยังไม่ตัดตามเวลา' WHERE ip = '%s' AND timeout ='' AND date = '%s'" %(ip,date)
                    print(sql)
                    cursor = connection.cursor()
                    cursor.execute(sql)
                    connection.commit()
                    return redirect(url_for('home'))    
                
                    
            
        print("Ontime no session")    
        return render_template("index.html" ,ip=ip ,date=date ,time=time )


    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    ip = request.args.get('ip')
    name = request.args.get('name')
    date = request.args.get('date')
    if ip in iplist: 
        d = iplist.index(ip)
        iplist.remove(ip)
        ipdate.remove(ipdate[d])
    
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
    return render_template("test.html")


@app.route('/saveVisitor', methods=['GET', 'POST'])
def saveVisitor():
    ip = request.args.get('ip')
    date = request.args.get('date')
    
    name = request.args.get('name')
    if name=="" or ip is None:
        return redirect(url_for('home'))
    else :
        iplist.append(ip)
        ipdate.append(date)
        date = request.args.get('date')
        timein = request.args.get('time')
        department = request.args.get("department")
        detail = request.args.get('detail')
        phonenumber = request.args.get('phonenumber')
        marketing,sales,hr,customerservice,accounting = 0,0,0,0,0
        if department == "ฝ่ายการตลาด":
            marketing = 1
        elif department == "ฝ่ายขาย":
            sales = 1
        elif department == "ฝ่ายบุคคล":
            hr = 1
        elif department == "ฝ่ายลูกค้าสัมพันธ์":
            customerservice = 1
        elif department == "ฝ่ายบัญชี/การเงิน":
            accounting = 1    
        
        connection = getConnection()
        sql = "INSERT INTO visitor(ip, name, detail ,date ,timein ,department ,phonenumber,status) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (ip, name, detail ,date ,timein ,department ,phonenumber,"เหลือกรอกชื่อพนักงาน")
        ins = "INSERT  INTO resultvisitor(date,marketing,sales,hr,customerservice,accounting) VALUES('%s', '%s', '%s', '%s','%s', '%s')" % (date,marketing,sales,hr,customerservice,accounting)
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.execute(ins)
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
    





#  Dashboard -----------------------------------------------------------------------------------------------------------
def showUser():  ###f
    connection = getConnection()
    sql = "SELECT * FROM visitor ORDER BY date,visitor.timein DESC"
    cursor = connection.cursor()
    cursor.execute(sql)
    user = cursor.fetchall()
    return user

def sumVisitor():  ###f
    connection = getConnection()
    cursor = connection.cursor()
    re = f"SELECT date,SUM(marketing) marketing,SUM(sales) sales,SUM(hr) hr,SUM(customerservice) customerservice,SUM(accounting) accounting FROM resultvisitor  GROUP BY date"
    cursor = connection.cursor()
    cursor.execute(re)
    res = cursor.fetchall()
    return res

@app.route('/dashboard')  ###f
def dashboard():
    user = showUser()
    res = sumVisitor()
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    date_times = date_time.strftime("%Y-%m-%d,%H:%M:%S")
    date,time = date_times.split(',')
    times = time.split(":")[0]
    t = int(times)

    
    
    if 6 <= t < 17:
        connection = getConnection()
        sql = "UPDATE visitor SET timeout = '17:00:00' ,status = 'ระบบตัด session ตอน 17.00 น.' WHERE date != '%s'" %(date)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return render_template("dashboard.html",user=user,res=res)

    else:
        for i in range(len(iplist)):
            if iplist[i] != date:
                iplist.remove(iplist[i])
                ipdate.remove(ipdate[i])
                print("delete Ip: "+iplist[i] + "date : "+ipdate[i])
        connection = getConnection()
        sql = "UPDATE visitor SET timeout = '17:00:00' ,status = 'ระบบตัด session ตอน 17.00 น.' WHERE date != '%s'" %(date)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return render_template("dashboard.html",user=user,res=res)

@app.route('/dashboardsearch', methods=['GET', 'POST'])  ###f
def dashboardsearch():
    res = sumVisitor()
    startday = request.args.get('startdaterange')
    stopday = request.args.get('stopdaterange')
    connection = getConnection()
    u = f"SELECT * FROM visitor WHERE date BETWEEN '{startday}' AND '{stopday}' ORDER BY date,visitor.timein DESC"
    cursor = connection.cursor()
    cursor.execute(u)
    user = cursor.fetchall()
    return render_template('dashboard.html',user=user,res=res)   


@app.route('/table')  ###f
def table():
    user = showUser()
    return render_template("table.html",user=user)



@app.route('/tablesearch', methods=['GET', 'POST'])  ###f
def tablesearch():
    startday = request.args.get('startdaterange')
    stopday = request.args.get('stopdaterange')
    connection = getConnection()
    u = f"SELECT * FROM visitor WHERE date BETWEEN '{startday}' AND '{stopday}' ORDER BY date,visitor.timein DESC"
    cursor = connection.cursor()
    cursor.execute(u)
    user = cursor.fetchall()
    return render_template('table.html',user=user)
#
@app.route('/chart')  ###f
def chart():
    res = sumVisitor()
    return render_template('chart.html',res = res)

@app.route('/chart_DWMY', methods=['GET', 'POST']) ###f
def chart_DWMY():
    times = request.args.get('type')
    print(times)
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    date_times = date_time.strftime("%Y-%m-%d,%H:%M:%S")
    day,time = date_times.split(',')
    y,m,d = day.split('-')
    connection = getConnection()
    cursor = connection.cursor()
    c = ''
    print(y)
    if times =='All': #pass
        c = "SELECT date,SUM(marketing) marketing,SUM(sales) sales,SUM(hr) hr,SUM(customerservice) customerservice,SUM(accounting) accounting FROM resultvisitor  GROUP BY date"
    if times =='Daily': 
        c = f"SELECT date_format(date, "'"%d/%m"'") date,SUM(marketing) marketing,SUM(sales) sales,SUM(hr) hr,SUM(customerservice) customerservice,SUM(accounting) accounting FROM resultvisitor  where year(date) LIKE year(CURDATE()) GROUP BY Day(date)"
        print(c)
    if times == 'Monthly': #pass 
        c = f"SELECT date_format(date, "'"%m-%y"'") date,SUM(marketing) marketing,SUM(sales) sales,SUM(hr) hr,SUM(customerservice) customerservice,SUM(accounting) accounting FROM resultvisitor where year(date) LIKE year(CURDATE()) GROUP BY month(date)"
        print(c)
    if times == 'Yearly': #pass
        c = "SELECT year(date) date,SUM(marketing) marketing,SUM(sales) sales,SUM(hr) hr,SUM(customerservice) customerservice,SUM(accounting) accounting FROM resultvisitor GROUP BY Year(date)" 
    if times == 'Weekly': #pass
        c = f"SELECT date_format(date, "'"wk%U"'") date, SUM(marketing) marketing,SUM(sales) sales,SUM(hr) hr,SUM(customerservice) customerservice,SUM(accounting) accounting FROM resultvisitor GROUP BY YEARWEEK(date, 2) ORDER BY YEARWEEK(date, 2)"
        
    cursor = connection.cursor()
    cursor.execute(c)    
    res = cursor.fetchall()
    return render_template('charts.html',res=res) 
    

@app.route('/chartsearch', methods=['GET', 'POST'])  ###f
def chartsearch():
    startday = request.args.get('startdaterange')
    stopday = request.args.get('stopdaterange')
    connection = getConnection()
    cursor = connection.cursor()
    re = f"SELECT * FROM visitor WHERE date BETWEEN '{startday}' AND '{stopday}' GROUP BY date"
    cursor = connection.cursor()
    cursor.execute(re)
    res = cursor.fetchall()
    return render_template('charts.html',res = res)
    
@app.route('/table_DWMY', methods=['GET', 'POST']) ###f
def table_DWMY():
    times = request.args.get('type')
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    date_times = date_time.strftime("%Y-%m-%d,%H:%M:%S")
    day,time = date_times.split(',')
    y,m,d = day.split('-')
    connection = getConnection()
    cursor = connection.cursor()
    u = ''
    
    if times =='All':
        u = "SELECT * FROM visitor ORDER BY date,visitor.timein DESC"
    elif times =='Daily':
        u = f"SELECT * FROM visitor WHERE date LIKE '%{y}-{m}-{d}' ORDER BY date,visitor.timein DESC"
    elif times == 'Monthly':
        u = f"SELECT * FROM visitor WHERE date LIKE '%{y}-{m}-%' ORDER BY date,visitor.timein DESC"
    elif times == 'Yearly':
        u = f"SELECT * FROM visitor WHERE date LIKE '{y}%' ORDER BY date,visitor.timein DESC"  
    elif times == 'Weekly':
        u = f"SELECT * FROM visitor WHERE week(date) = week(now()) AND year(date) = year(now()) ORDER BY date,visitor.timein DESC"
        
    cursor = connection.cursor()
    cursor.execute(u)
    user = cursor.fetchall()
    return render_template('table.html',user=user)


if __name__ == '__main__':
    app.run(debug=True)