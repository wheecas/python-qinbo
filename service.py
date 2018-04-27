#!/usr/bin/python3
 
import pymysql
import json
import confighelper
 
_host=confighelper.getConfigValue("host")
_port=3306
_user=confighelper.getConfigValue("user")
_password=confighelper.getConfigValue("password")
_db=confighelper.getConfigValue("db")
_cursorclass=pymysql.cursors.DictCursor
 
def insert(object):
	db = pymysql.connect(host=_host,port=_port,user=_user,password=_password,db=_db,cursorclass=_cursorclass,charset="utf8")
	cursor = db.cursor()
	#print(object["name"])
	sql="INSERT INTO gsdata_wx_article(`name`,wx_name,created_at,picurl,title,url,week_read_count,read_count,week_like_count,like_count,type,top,id,original_url,is_synchro)VALUES('"+object["name"]+"','"+object["wx_name"]+"','"+object["created_at"]+"','"+object["picurl"]+"','"+object["title"]+"','"+object["url"]+"',"+str(object["week_read_count"])+","+str(object["read_count"])+","+str(object["week_like_count"])+","+str(object["like_count"])+",'"+object["type"]+"',"+str(object["top"])+",'"+object["id"]+"','"+object["original_url"]+"',0)"
	#sql='select 1'
	#sql="""INSERT INTO gsdata_wx(`name`,wx_name,created_at,picurl,title,url,week_read_count,read_count,week_like_count,like_count,type,top,id,original_url,is_synchro)VALUES('数字货币趋势狂人','qushikuangren','2018-04-23 18:24:07','http://mmbiz.qpic.cn/mmbiz_jpg/sjBdkU5kWkeU261liaoZtuyONEz4TgXLodVckjib2vRicKkictkEbNrAvA9adjJOyAmMfuuXZFukuGSKHU5j75h9Yg/0?wx_fmt=jpeg','空气币的上涨是为了更好的归零，4月23日行情分析','http://mp.weixin.qq.com/s?__biz=MzI2ODM4NDA1OQ==&mid=2247484916&idx=1&sn=a0f02f6a6d8c42a736b0d7a27608670c&chksm=eaf127a0dd86aeb6563fc3e15ede863322d70db1187626cfadb04c9c7be1216e06ed0476a38b&scene=27#wechat_redirect',0,41734,0,1377,'49',1,'a0f02f6a6d8c42a736b0d7a27608670c','http://api.gsdata.cn/weixin/v1/articles/real-times?sn=a0f02f6a6d8c42a736b0d7a27608670c&time=2018042318',0)"""
	#print(sql)
	#sql="select 1"
	
	try:
		cursor.execute(sql)
		db.commit()
	except Exception as err:
		print (err)
		db.rollback()
	db.close()

def get(id):
	db = pymysql.connect(host=_host,port=_port,user=_user,password=_password,db=_db,cursorclass=_cursorclass,charset="utf8")
	cursor = db.cursor()
	sql="SELECT id FROM gsdata_wx WHERE id='"+id+"'"
	try:
		cursor.execute(sql)
		_id=cursor.fetchone()
		if _id is None:
			return False
		return True
	except Exception as err:
		print(err)
	db.close()
	return False

def getWxAuthor():
	wxName = []
	db = pymysql.connect(host=_host,port=_port,user=_user,password=_password,db=_db,cursorclass=_cursorclass,charset="utf8")
	cursor = db.cursor()
	sql="select wx_name from gsdata_wx"
	try:
		cursor.execute(sql)
		_list=cursor.fetchall()
		for item in _list:
			wxName.append(item["wx_name"])
	except Exception as err:
		print(err)
	db.close()
	return wxName

	
 
# 使用 cursor() 方法创建一个游标对象 cursor
#cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询 
#sql="SELECT * FROM coin limit 10"
#try:
#	cursor.execute(sql)
#	results = cursor.fetchall()
#	for row in results:
#		print(row['Id'])
	
	
#except:
#   print ("Error: unable to fetch data")
 
# 关闭数据库连接
#db.close()