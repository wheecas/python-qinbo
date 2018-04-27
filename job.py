import time  
import os  
import sched  
import json
import service
import qinbo
import confighelper
from threading import Thread

  
# 初始化sched模块的scheduler类  
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。  
schedule = sched.scheduler(time.time, time.sleep)
lock = 0
  
# 被周期性调度触发的函数  
def execute_command(cmd, inc):
    hour=time.strftime('%H',time.localtime())  
    start_hour=confighelper.getConfigValue("start_hour")
    if start_hour==hour:
        Thread(target=crawlArticleJob).start()
    else:
        print("循环检查")
    schedule.enter(inc, 0, execute_command, (cmd, inc))
  
def main(cmd, inc=60):  
    # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，  
    # 给该触发函数的参数（tuple形式）
        schedule.enter(0, 0, execute_command, (cmd, inc))  
        schedule.run()

def crawlArticleJob():
    global lock
    if lock==0:
        lock=1
        print("执行任务")
        wx_names=service.getWxAuthor()
        for name in wx_names:
            crawlArticle(name)
        inc=int(confighelper.getConfigValue("service_inc"))
        time.sleep(inc)
        lock=0
    else:
        print("任务执行中") 

def crawlArticle(wx_name):
    
    #_data='{"data":[{"name":"数字货币趋势狂人","wx_name":"qushikuangren","created_at":"2018-04-23 18:24:08","picurl":"http://mmbiz.qpic.cn/mmbiz_jpg/sjBdkU5kWkeU261liaoZtuyONEz4TgXLobp3jAdpxDubt28WYcYS1zBrm0x6gFJ7gAsMBRmuBYDibkVP47ag2K7w/0?wx_fmt=jpeg","title":"主网正式上线后暴涨100%！10WTPS 吞吐量的文娱行业首条底层公链主网上线！","url":"http://mp.weixin.qq.com/s?__biz=MzI2ODM4NDA1OQ==&mid=2247484916&idx=2&sn=42b032cbb8fb2867e354d22dead2d171&chksm=eaf127a0dd86aeb6eb6a3c68dbade213d53a1baef078c7ff7c427d90c3ba4de5fd586aafa69c&scene=27#wechat_redirect","digest":"TPS性能优越，这将会是文娱行业的3.0公链代表？类似EOS一样的另外一匹黑马？","week_read_count":0,"read_count":11295,"week_like_count":0,"like_count":96,"type":"49","top":2,"id":"42b032cbb8fb2867e354d22dead2d171","is_video":null,"is_audio":null,"copyright":null,"author":"","original_url":"http://api.gsdata.cn/weixin/v1/articles/real-times?sn=42b032cbb8fb2867e354d22dead2d171&time=2018042318"},{"name":"数字货币趋势狂人","wx_name":"qushikuangren","created_at":"2018-04-23 18:24:07","picurl":"http://mmbiz.qpic.cn/mmbiz_jpg/sjBdkU5kWkeU261liaoZtuyONEz4TgXLodVckjib2vRicKkictkEbNrAvA9adjJOyAmMfuuXZFukuGSKHU5j75h9Yg/0?wx_fmt=jpeg","title":"空气币的上涨是为了更好的归零，4月23日行情分析","url":"http://mp.weixin.qq.com/s?__biz=MzI2ODM4NDA1OQ==&mid=2247484916&idx=1&sn=a0f02f6a6d8c42a736b0d7a27608670c&chksm=eaf127a0dd86aeb6563fc3e15ede863322d70db1187626cfadb04c9c7be1216e06ed0476a38b&scene=27#wechat_redirect","digest":"狂人本着负责，专注，诚恳的态度用心写每一篇分析文章，特点鲜明，不做作，不浮夸！","week_read_count":0,"read_count":41734,"week_like_count":0,"like_count":1377,"type":"49","top":1,"id":"a0f02f6a6d8c42a736b0d7a27608670c","is_video":null,"is_audio":null,"copyright":null,"author":"狂人","original_url":"http://api.gsdata.cn/weixin/v1/articles/real-times?sn=a0f02f6a6d8c42a736b0d7a27608670c&time=2018042318"}]}'
    _data=qinbo.getArticle(wx_name)
    
    status_code=_data.status_code
    if status_code ==200:
        _json=json.loads(_data.text)
        #print(_json)
        _list=_json["data"]
        for item in _list:
            #print(item)
            _id=item["id"]
            #print(_id)
            isexist=service.get(_id)
            print(isexist)
            if(isexist==False):
                service.insert(item)
    
  
  
# 每60秒检查是否运行服务
if __name__ == '__main__':  
    main("netstat -an", 60)