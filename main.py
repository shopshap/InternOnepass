from flask import Flask, render_template, request, redirect, url_for, session ,g
import pymysql ,pymssql
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'any random string'
app.permanent_session_lifetime = timedelta(seconds=5)
SESSION_TYPE = 'redis'

def getConnection ():
    return pymysql.connect(
        host = 'localhost',
        db = 'qrcode',
        user = 'root',
        password = '',
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor
		)

def mssqlconnect ():
    return pymssql.connect(
     server='10.3.1.20',
     user='tran01', 
     password='tog@1234', 
     database='BarcodeSystem',
     charset = 'tis620'
    )

iplist = []

def sumVisitor():
    connection = mssqlconnect()
    cursor = connection.cursor()
    re = f"""select TOP(10) * from
            (
            select (CAST(WorkTimeIn AS DATE)) AS DateIn, value from ExternalVisitorDetail
            unpivot
            (
                value
                for col in (VisitPurpose)
            ) unp
            ) src
            pivot
            (
            count(value)
            for value in (O1, O2, O3, O4, O5, O6, O7, P1, P2, P3, P4, P5, P6, P7, P8, P9)
            ) piv
            GROUP BY DateIn, piv.O1, piv.O2, piv.O3, piv.O4, piv.O5, piv.O6, piv.O7, piv.P1, piv.P2, piv.P3, piv.P4, piv.P5, piv.P6, piv.P7, piv.P8, piv.P9
            Order by DateIn DESC"""
    cursor = connection.cursor()
    cursor.execute(re)
    res = cursor.fetchall()
    return res

def Total():
    connection = mssqlconnect()
    cursor = connection.cursor()
    to ="select COUNT(ExternalVisitorDetail.WorkID) from ExternalVisitorDetail,ExternalVisitorTran where ExternalVisitorDetail.WorkID = ExternalVisitorTran.WorkID"
    cursor = connection.cursor()
    cursor.execute(to)
    total = cursor.fetchall()
    return total


@app.route('/')
def home():
    return render_template("test.html")

@app.route('/login', methods=['GET', 'POST'])
def login():

    ip = request.args.get('ip')
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    date_times = date_time.strftime("%Y-%m-%d,%H:%M:%S")
    date,time = date_times.split(',')
    
    session['user_ip'] = ip
    
    if 'phonenumber' in session:
        #if ip in session:
        print("onetime with session")
        print(session)
        #count = 0
        connection = getConnection()
        sql = "SELECT * FROM visitor WHERE ip = '%s' AND employeeid ='' AND date = '%s'" %(ip,date)
        cursor = connection.cursor()
        cursor.execute(sql)
        vi = cursor.fetchall()
        
        #for i in vi:
        #    count += 1
        #print(count)
                
        #if count == 0:
        #print("Onetime เหลือกดออก")
        #connection = getConnection() #119.76.14.172 
        #sql = "SELECT * FROM visitor WHERE ip = '%s' AND date = '%s' AND status ='เหลือกดออก'" %(ip,date)
        #cursor = connection.cursor()
        #cursor.execute(sql)
        #hi = cursor.fetchone()
        #print(hi)
        #return render_template("successin.html" ,hi=hi)
        #elif count > 0 :
        print("Onetime เหลือกรอกรหัสพนักงาน")
        return render_template("profilein.html" ,vi=vi)   
            
    print(session)    
    return render_template("index.html" ,ip=ip ,date=date ,time=time )
   
    
    

    # if ip == "" or ip is None:
    #     print("index")
    #     return redirect(url_for('home'))
              
    # else:
        
                
                
            
    #     print("Ontime no session")    
    #     return render_template("index.html" ,ip=ip ,date=date ,time=time )


    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    ip = request.args.get('ip')
    name = request.args.get('name')
    date = request.args.get('date')
    #iplist.remove(ip)
    
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
    # if request.method == 'POST':
    ip = request.args.get('ip')
    iplist.append(ip)
    name = request.args.get('name')
    date = request.args.get('date')
    timein = request.args.get('time')
    department = request.args.get("department")
    detail = request.args.get('detail')
    phonenumber = request.args.get('phonenumber')
    session["phonenumber"] = phonenumber
    print(phonenumber)
    print(session)
    
    connection = getConnection()
    sql = "INSERT INTO visitor(ip, name, detail ,date ,timein ,department ,phonenumber,status) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (ip, name, detail ,date ,timein ,department ,phonenumber,"เหลือกรอกชื่อพนักงาน")
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    
    return render_template("profile.html" ,name=name ,date=date ,timein=timein ,department=department ,detail=detail ,phonenumber=phonenumber,ip=ip)
    #return redirect(url_for('home'))


@app.route('/saveemployee', methods=['GET', 'POST'])
def saveemployee():
    #if 'ip' in session:
        employeeid = request.args.get('employeeid')
        ip = request.args.get('ip')
        name = request.args.get('name')
        date = request.args.get('date')
        timein = request.args.get('timein')
        department = request.args.get("department")
        detail = request.args.get('detail')
        phonenumber = request.args.get('phonenumber')
        
        connection = getConnection()
        sql = f"UPDATE visitor SET employeeid = '{employeeid}' , status ='เหลือกดออก' WHERE ip = '{ip}' AND name = '{name}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return render_template("success.html",name=name,date=date,timein=timein,department=department,detail=detail,phonenumber=phonenumber,employeeid=employeeid,ip=ip)
    #return redirect(url_for('home'))


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







@app.route('/dashboard')
def dashboard():
    user = showUser()
    total = Total()
    connection = mssqlconnect()
    cursor = connection.cursor()
    re ="""select top(10)* from
            (
            select (CAST(WorkTimeIn AS DATE)) AS DateIn, value from ExternalVisitorDetail
            unpivot
            (
                value
                for col in (VisitPurpose)
            ) unp
            ) src
            pivot
            (
            count(value)
            for value in (O1, O2, O3, O4, O5, O6, O7, P1, P2, P3, P4, P5, P6, P7, P8, P9)
            ) piv
            GROUP BY DateIn, piv.O1, piv.O2, piv.O3, piv.O4, piv.O5, piv.O6, piv.O7, piv.P1, piv.P2, piv.P3, piv.P4, piv.P5, piv.P6, piv.P7, piv.P8, piv.P9
            Order by DateIn DESC"""
    cursor = connection.cursor()
    cursor.execute(re)
    res = cursor.fetchall()
    t= total[0][0]
    currency = "{:,}".format(t)
    return render_template('dashboard.html',user=user,res=res,total = currency)

def showUser():  
    connection = mssqlconnect()
    sql = """SELECT TOP(100) * FROM ExternalVisitorDetail s
            RIGHT JOIN
            (SELECT CAST(WorkTimeIn AS TIME(0)) AS TimeIn, CAST(WorkTimeOut AS TIME(0)) AS TimeOut 
            , CAST(WorkTimeIn AS DATE) AS DateIn , WorkID AS WorkID
            FROM ExternalVisitorDetail) TI
            ON (s.WorkID = TI.WorkID)
            RIGHT JOIN
            (SELECT * FROM ExternalVisitPurpose) pr
            ON (s.VisitPurpose = pr.VisitID and s.FlagStation = pr.FlagVisit)
            WHERE GuestCompany IS NOT NULL and 
            s.WorkID IS NOT NULL and GuestName IS NOT NULL and 
            VisitPurpose IS NOT NULL and WorkLocation IS NOT NULL 
            and WorkTimeIn IS NOT NULL 
            and CustID IS NOT NULL and BarcodeExpireDate IS NOT NULL
	        ORDER BY WorkTimeIn DESC"""
    cursor = connection.cursor()
    cursor.execute(sql)
    user = cursor.fetchall()
    return user

@app.route('/table')
def table():
    user = showUser()
    print(user)


    
    return render_template("table.html",user=user)

@app.route('/tablesearch', methods=['GET', 'POST'])
def tablesearch():
    startday = request.args.get('startdaterange')
    stopday = request.args.get('stopdaterange')
    connection = mssqlconnect()
    u = f"""
           SELECT TOP(100) * FROM ExternalVisitorDetail s
            RIGHT JOIN
            (SELECT CAST(WorkTimeIn AS TIME(0)) AS TimeIn, CAST(WorkTimeOut AS TIME(0)) AS TimeOut 
            , CAST(WorkTimeIn AS DATE) AS DateIn , WorkID AS WorkID
            FROM ExternalVisitorDetail) TI
            ON (s.WorkID = TI.WorkID)
            RIGHT JOIN
            (SELECT * FROM ExternalVisitPurpose) pr
            ON (s.VisitPurpose = pr.VisitID and s.FlagStation = pr.FlagVisit)
            WHERE GuestCompany IS NOT NULL and 
            s.WorkID IS NOT NULL and GuestName IS NOT NULL and 
            VisitPurpose IS NOT NULL and WorkLocation IS NOT NULL 
            and WorkTimeIn IS NOT NULL 
            and CustID IS NOT NULL and BarcodeExpireDate IS NOT NULL
	        and WorkTimeIn BETWEEN CONVERT(varchar, '{startday} 00:00:00', 108) 
		   and CONVERT(varchar, '{stopday} 23:59:59', 108)
		   ORDER BY WorkTimeIn DESC"""
    cursor = connection.cursor()
    cursor.execute(u)
    user = cursor.fetchall()
    return render_template('table.html',user=user)

@app.route('/table_DWMY', methods=['GET', 'POST']) ###f
def table_DWMY():
    times = request.args.get('type')
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    date_times = date_time.strftime("%Y-%m-%d,%H:%M:%S")
    day,time = date_times.split(',')
    y,m,d = day.split('-')
    connection = mssqlconnect()
    cursor = connection.cursor()
    u = ''
    #my_week = datetime.date.today() 
    #yy,wk,dd = my_week.isocalendar()
    
    if times =='All':
        u = """SELECT TOP(100) * FROM ExternalVisitorDetail s
                RIGHT JOIN
                (SELECT CAST(WorkTimeIn AS TIME(0)) AS TimeIn, CAST(WorkTimeOut AS TIME(0)) AS TimeOut 
                , CAST(WorkTimeIn AS DATE) AS DateIn , WorkID AS WorkID
                FROM ExternalVisitorDetail) TI
                ON (s.WorkID = TI.WorkID)
                RIGHT JOIN
                (SELECT * FROM ExternalVisitPurpose) pr
                ON (s.VisitPurpose = pr.VisitID and s.FlagStation = pr.FlagVisit)
                WHERE GuestCompany IS NOT NULL and 
                    s.WorkID IS NOT NULL and GuestName IS NOT NULL and 
                    VisitPurpose IS NOT NULL and WorkLocation IS NOT NULL 
                    and WorkTimeIn IS NOT NULL 
                    and CustID IS NOT NULL and BarcodeExpireDate IS NOT NULL
                    ORDER BY WorkTimeIn DESC"""
    elif times =='Daily':
        u = f"""SELECT TOP(100) * FROM ExternalVisitorDetail s
                RIGHT JOIN
                (SELECT CAST(WorkTimeIn AS TIME(0)) AS TimeIn, CAST(WorkTimeOut AS TIME(0)) AS TimeOut 
                , CAST(WorkTimeIn AS DATE) AS DateIn , WorkID AS WorkID
                FROM ExternalVisitorDetail) TI
                ON (s.WorkID = TI.WorkID)
                RIGHT JOIN
                (SELECT * FROM ExternalVisitPurpose) pr
                ON (s.VisitPurpose = pr.VisitID and s.FlagStation = pr.FlagVisit)
                WHERE GuestCompany IS NOT NULL and 
                    s.WorkID IS NOT NULL and GuestName IS NOT NULL and 
                    VisitPurpose IS NOT NULL and WorkLocation IS NOT NULL 
                    and WorkTimeIn IS NOT NULL 
                    and CustID IS NOT NULL and BarcodeExpireDate IS NOT NULL and
                    DATEPART(yy, WorkTimeIn) = DATEPART(yy, GETDATE()) AND DATEPART(mm, WorkTimeIn) = DATEPART(mm, GETDATE())
                    AND DATEPART(dd, WorkTimeIn) = DATEPART(dd, GETDATE())
                    ORDER BY WorkTimeIn DESC"""
    elif times == 'Monthly':
        u = f"""SELECT TOP(100) * FROM ExternalVisitorDetail s
                RIGHT JOIN
                (SELECT CAST(WorkTimeIn AS TIME(0)) AS TimeIn, CAST(WorkTimeOut AS TIME(0)) AS TimeOut 
                , CAST(WorkTimeIn AS DATE) AS DateIn , WorkID AS WorkID
                FROM ExternalVisitorDetail) TI
                ON (s.WorkID = TI.WorkID)
                RIGHT JOIN
                (SELECT * FROM ExternalVisitPurpose) pr
                ON (s.VisitPurpose = pr.VisitID and s.FlagStation = pr.FlagVisit)
                WHERE GuestCompany IS NOT NULL and 
                    s.WorkID IS NOT NULL and GuestName IS NOT NULL and 
                    VisitPurpose IS NOT NULL and WorkLocation IS NOT NULL 
                    and WorkTimeIn IS NOT NULL 
                    and CustID IS NOT NULL and BarcodeExpireDate IS NOT NULL and
                    DATEPART(yy, WorkTimeIn) = DATEPART(yy, GETDATE()) AND DATEPART(mm, WorkTimeIn) = '{m}'
                    ORDER BY WorkTimeIn DESC"""

    elif times == 'Yearly':
        u = f"""SELECT TOP(100) * FROM ExternalVisitorDetail s
                RIGHT JOIN
                (SELECT CAST(WorkTimeIn AS TIME(0)) AS TimeIn, CAST(WorkTimeOut AS TIME(0)) AS TimeOut 
                , CAST(WorkTimeIn AS DATE) AS DateIn , WorkID AS WorkID
                FROM ExternalVisitorDetail) TI
                ON (s.WorkID = TI.WorkID)
                RIGHT JOIN
                (SELECT * FROM ExternalVisitPurpose) pr
                ON (s.VisitPurpose = pr.VisitID and s.FlagStation = pr.FlagVisit)
                WHERE GuestCompany IS NOT NULL and 
                    s.WorkID IS NOT NULL and GuestName IS NOT NULL and 
                    VisitPurpose IS NOT NULL and WorkLocation IS NOT NULL 
                    and WorkTimeIn IS NOT NULL 
                    and CustID IS NOT NULL and BarcodeExpireDate IS NOT NULL and
                    (DATEPART(yy, WorkTimeIn) = DATEPART(yy, GETDATE()))
                    ORDER BY WorkTimeIn DESC""" 
    elif times == 'Weekly':
        u =  f"""SELECT * FROM ExternalVisitorDetail s
            RIGHT JOIN
            (SELECT CAST(WorkTimeIn AS TIME(0)) AS TimeIn, CAST(WorkTimeOut AS TIME(0)) AS TimeOut 
            , CAST(WorkTimeIn AS DATE) AS DateIn , WorkID AS WorkID
            FROM ExternalVisitorDetail) TI
            ON (s.WorkID = TI.WorkID)
            RIGHT JOIN
            (SELECT * FROM ExternalVisitPurpose) pr
            ON (s.VisitPurpose = pr.VisitID and s.FlagStation = pr.FlagVisit)
            WHERE GuestCompany IS NOT NULL and 
                s.WorkID IS NOT NULL and GuestName IS NOT NULL and 
            VisitPurpose IS NOT NULL and WorkLocation IS NOT NULL 
            and WorkTimeIn IS NOT NULL 
            and CustID IS NOT NULL and BarcodeExpireDate IS NOT NULL and
            (DATEPART(ww, WorkTimeIn) = DATEPART(ww, GETDATE()) and DATEPART(yy, WorkTimeIn) = '{y}')
	        ORDER BY WorkTimeIn DESC"""
        
    cursor = connection.cursor()
    cursor.execute(u)
    user = cursor.fetchall()
    return render_template('table.html',user=user)



def sumAll():  ###f
    connection = mssqlconnect()
    cursor = connection.cursor()
    re = f"""select * from
            (SELECT total = 'Total Visiter',
                VisitPurpose as title,
                COUNT(VisitPurpose) as num
                FROM ExternalVisitorDetail, ExternalVisitPurpose
                where ExternalVisitorDetail.VisitPurpose = ExternalVisitPurpose.VisitID
                GROUP BY VisitPurpose) as P
                pivot
            (
            SUM(num)
            for title in ( O1, O2, O3, O4, O5, O6, O7, P1, P2, P3, P4, P5, P6, P7, P8, P9)
            ) piv"""
    cursor = connection.cursor()
    cursor.execute(re)
    res = cursor.fetchall()
    return res

@app.route('/chart')  
def chart():
    res = sumAll()
    print(res)
    return render_template('chart.html',res = res)

@app.route('/chartsearch', methods=['GET', 'POST'])  
def chartsearch():
    startday = request.args.get('startdaterange')
    stopday = request.args.get('stopdaterange')
    connection = mssqlconnect()
    cursor = connection.cursor()
    re = f"""select * from
            (
            select (CAST(WorkTimeIn AS DATE)) AS DateIn, value
            from ExternalVisitorDetail
            unpivot
            (
                value
                for col in (VisitPurpose)
            ) unp
            ) src
            pivot
            (
            count(value)
            for value in (O1, O2, O3, O4, O5, O6, O7, P1, P2, P3, P4, P5, P6, P7, P8, P9)
            ) piv
            where DateIn BETWEEN CONVERT(varchar, '{startday} 00:00:00', 108) 
                    and CONVERT(varchar, '{stopday} 23:59:59', 108)
            Order by DateIn DESC"""
    cursor = connection.cursor()
    cursor.execute(re)
    res = cursor.fetchall()
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
    connection = mssqlconnect()
    cursor = connection.cursor()
    c = ''
    print(y)
    if times =='All': #pass
        c = """select * from
            (SELECT total = 'Total Visiter',
                VisitPurpose as title,
                COUNT(VisitPurpose) as num
                FROM ExternalVisitorDetail, ExternalVisitPurpose
                where ExternalVisitorDetail.VisitPurpose = ExternalVisitPurpose.VisitID
                GROUP BY VisitPurpose) as P
                pivot
            (
            SUM(num)
            for title in ( O1, O2, O3, O4, O5, O6, O7, P1, P2, P3, P4, P5, P6, P7, P8, P9)
            ) piv"""
    if times =='Daily': 
        c = f"""select * from
            (
            select (CAST(WorkTimeIn AS DATE)) AS DateIn, value from ExternalVisitorDetail
            unpivot
            (
                value
                for col in (VisitPurpose)
            ) unp
            ) src
            pivot
            (
            count(value)
            for value in (O1, O2, O3, O4, O5, O6, O7, P1, P2, P3, P4, P5, P6, P7, P8, P9)
            ) piv
			where
                    (DATEPART(yy, DateIn) = DATEPART(yy, GETDATE()) AND DATEPART(mm, DateIn) = DATEPART(mm, GETDATE())
                    AND DATEPART(dd, DateIn) = DATEPART(dd, GETDATE()))
            GROUP BY DateIn, piv.O1, piv.O2, piv.O3, piv.O4, piv.O5, piv.O6, piv.O7, piv.P1, piv.P2, piv.P3, piv.P4, piv.P5, piv.P6, piv.P7, piv.P8, piv.P9
            Order by DateIn DESC"""
        print(c)
    if times == 'Monthly': #pass 
        c = f"""select * from
            (
            select (CAST(WorkTimeIn AS DATE)) AS DateIn, value from ExternalVisitorDetail
            unpivot
            (
                value
                for col in (VisitPurpose)
            ) unp
            ) src
            pivot
            (
            count(value)
            for value in (O1, O2, O3, O4, O5, O6, O7, P1, P2, P3, P4, P5, P6, P7, P8, P9)
            ) piv
			where (DATEPART(yy, DateIn) = DATEPART(yy, GETDATE()) AND DATEPART(mm, DateIn) = DATEPART(mm, GETDATE()))
            GROUP BY DateIn, piv.O1, piv.O2, piv.O3, piv.O4, piv.O5, piv.O6, piv.O7, piv.P1, piv.P2, piv.P3, piv.P4, piv.P5, piv.P6, piv.P7, piv.P8, piv.P9
            Order by DateIn DESC"""
        print(c)
    if times == 'Yearly': #pass
        c = f"""select * from
            (
            select (CAST(WorkTimeIn AS DATE)) AS DateIn, value from ExternalVisitorDetail
            unpivot
            (
                value
                for col in (VisitPurpose)
            ) unp
            ) src
            pivot
            (
            count(value)
            for value in (O1, O2, O3, O4, O5, O6, O7, P1, P2, P3, P4, P5, P6, P7, P8, P9)
            ) piv
			where (DATEPART(yy, DateIn) = (DATEPART(yy, GETDATE())))
            GROUP BY DateIn, piv.O1, piv.O2, piv.O3, piv.O4, piv.O5, piv.O6, piv.O7, piv.P1, piv.P2, piv.P3, piv.P4, piv.P5, piv.P6, piv.P7, piv.P8, piv.P9
            Order by DateIn DESC"""
    if times == 'Weekly': #pass
        c = f"""select * from
            (
            select (CAST(WorkTimeIn AS DATE)) AS DateIn, value from ExternalVisitorDetail
            unpivot
            (
                value
                for col in (VisitPurpose)
            ) unp
            ) src
            pivot
            (
            count(value)
            for value in (O1, O2, O3, O4, O5, O6, O7, P1, P2, P3, P4, P5, P6, P7, P8, P9)
            ) piv
			where (DATEPART(ww, DateIn) = DATEPART(ww, GETDATE()) and DATEPART(yy, DateIn) = DATEPART(yy, GETDATE()))
            GROUP BY DateIn, piv.O1, piv.O2, piv.O3, piv.O4, piv.O5, piv.O6, piv.O7, piv.P1, piv.P2, piv.P3, piv.P4, piv.P5, piv.P6, piv.P7, piv.P8, piv.P9
            Order by DateIn DESC"""
        
    cursor = connection.cursor()
    cursor.execute(c)    
    res = cursor.fetchall()
    return render_template('chart.html',res=res) 


if __name__ == '__main__':
    app.run(debug=True)