#encoding=utf-8
from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect  
from django.views.decorators.csrf import csrf_protect
import MySQLdb
import os
import time
def main(request):
    account=request.session.get('account')
    name=request.session.get('name')
    grade=request.session.get('grade')
    data={}
    connection = MySQLdb.connect(host='localhost', user='root', passwd='545269649', port=3306, use_unicode=1, charset='utf8')
    cursor = connection.cursor()
    connection.select_db('database')
    sql="select * from homeworks"
    objs=[]
    try:
        cursor.execute(sql)
        result=cursor.fetchall()
        for row in result:
            temp={}
            temp["num"]=row[0]
            temp["epic"]=row[1]
            temp["name"]=row[2]
            temp["descript"]=row[3]
            temp["score"]=row[4]
            temp["endtime"]=row[5]
            temp["filename"]=row[6]
            try:
                tempsql="select * from subrecord where num=%s and account=%s"%(row[0],account)
                cursor.execute(tempsql)
                tempresult=cursor.fetchall()
                for item in tempresult:
                    temp["subtime"]=item[3]
                    temp["rate"]=item[4]
                    temp["count"]=item[5]
            except:
                pass
            objs.append(temp)
    except:
        pass
    data["objs"]=objs
    data["account"]=account
    data["name"]=name
    data["grade"]=grade
    data["logintime"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    connection.close()
    return render(request,"smain.html",{"data":data})
def login(request):
 if request.method == 'POST':
    account=request.POST.get("username")
    password=request.POST.get("password")
    connection = MySQLdb.connect(host='localhost', user='root', passwd='545269649', port=3306, use_unicode=1, charset='utf8')
    cursor = connection.cursor()
    connection.select_db('database')
    sql="select * from user where account=%s"%account
    try:
        cursor.execute(sql)
        result=cursor.fetchall()
        if result[0][1]==password:
            request.session['account']=result[0][0]
            request.session['name']=result[0][2]
            request.session['grade']=result[0][3]
            connection.close()
            return HttpResponseRedirect('/main')
        else:
            connection.close()
            return HttpResponseRedirect('/index')
    except:
            return HttpResponseRedirect('/index')
def index(request):
    if request.method == 'GET':
        return render(request,"login.html")
def register(request):
    if request.method == 'GET':
        return render(request,"register.html")
    if request.method == 'POST':
        account=request.POST.get("username")
        password=request.POST.get("password")
        name=request.POST.get("name")
        grade=request.POST.get("grade")
        connection = MySQLdb.connect(host='localhost', user='root', passwd='545269649', port=3306, use_unicode=1, charset='utf8')
        cursor = connection.cursor()
        connection.select_db('database')
        sql="insert into user values(%s,%s,%s,%s)"
        sqldata=(account,password,name,grade)
        try:
            cursor.execute(sql,sqldata)
            connection.commit()
            connection.close()
            os.mkdir("D:\\upload\\"+account) 
            return HttpResponseRedirect('/index')
        except:
             return HttpResponseRedirect('/register')
def uploadfile(request):
    if request.method == "POST":
        account=request.session.get('account')
        connection = MySQLdb.connect(host='localhost', user='root', passwd='545269649', port=3306, use_unicode=1, charset='utf8')
        cursor = connection.cursor()
        connection.select_db('database')
        sql="select * from homeworks"
        cursor.execute(sql)
        result=cursor.fetchall()
        for row in result:
            file =request.FILES.get(row[2], None)
            if not file:  
                continue 
            if not os.path.exists("D:\\upload\\"+str(account)+"\\"+str(row[0])):
                os.mkdir("D:\\upload\\"+str(account)+"\\"+str(row[0]))
            store = open(os.path.join("D:\\upload\\"+str(account)+"\\"+str(row[0]),file.name.split('\\')[0]),'wb+')
            for chunk in file.chunks(): 
                store.write(chunk)  
            store.close()
            tempsql="select count,rate from subrecord where num=%s and account=%s"%(row[0],account)
            cursor.execute(tempsql)
            tempresult=cursor.fetchall()
            count=0
            rate="100%"
            for item in tempresult:
                count=item[0]
                rate=item[1]
            count=count+1
            tempsql="insert into subrecord(num,account,subtime,rate,count) values(%s,%s,%s,%s,%s)"
            subtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sqldata=(row[0],account,subtime,rate,count)
            cursor.execute(tempsql,sqldata)
        connection.commit()
        connection.close()
        return HttpResponse("upload success!")  

