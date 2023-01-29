# encoding:utf-8
import csv
import os
import time
import pymysql.cursors

device_id="com.sightidea.locale"#测试应用包名称
app_bundle_id = "com.sightidea.locale/com.sightidea.locale.LocaleActivity" #测试应用Activity名称
device_id='BH907HED9G'#测试设备ID
adb="/System/Volumes/Data/mytest/rj/sdk/platform-tools/adb" #本地adb路径

# APP类
class App(object):
    def __init__(self):
        self.content = ""
        self.startTime = 0

    # 启动APP
    def launch_app(self):
        cmd = '/System/Volumes/Data/mytest/rj/sdk/platform-tools/adb shell am start -W -n com.sightidea.locale/com.sightidea.locale.LocaleActivity'  # type: str
        self.content = os.popen(cmd)

    # 停止app，热启动
    @staticmethod
    def stop_app():
        # 冷启动停止的命令：完全杀进程，再启动
        # cmd = 'adb shell am force-stop org.chromium.webview_shell'
        # 热启动停止的命令,启动完至于后台
        cmd = '/System/Volumes/Data/mytest/rj/sdk/platform-tools/adb shell input keyevent 3'
        os.popen(cmd)
 # 停止app，冷启动
    @staticmethod
    def stop_app2():
        # 冷启动停止的命令：完全杀进程，再启动
        cmd = '/System/Volumes/Data/mytest/rj/sdk/platform-tools/adb shell am force-stop com.sightidea.locale'
        # 热启动停止的命令,启动完至于后台
        #cmd = '/System/Volumes/Data/mytest/rj/sdk/platform-tools/adb shell input keyevent 3'
        os.popen(cmd)

    # 获取热启动时间
    def get_launched_time(self):
        for line in self.content.readlines():
            line = line.strip() 
            if "ThisTime" in line:
                self.startTime = line.split(":")[1]
                #print (self.startTime)
            if "TotalTime" in line:
                self.startTime2 = line.split(":")[1]
                #print (self.startTime2)
            if "WaitTime" in line:
                self.startTime3 = line.split(":")[1] 
                #print (self.startTime3) 
                    
        print (self.startTime,self.startTime2,self.startTime3)  
        # 数据存数据库连接数据库
        connect = pymysql.Connect(
        host='10.0.3.140',
        port=3306,
        user='root',
        passwd='Aa654321',
        db='test',
        charset='utf8'
        )
           # 获取游标
        cursor = connect.cursor()
        sql = "INSERT INTO and_qidtime (ThisTime,TotalTime,WaitTime) VALUES('"+self.startTime+"','"+self.startTime2+"','"+self.startTime3+"')"
        cursor.execute(sql)
        connect.commit()
           # 关闭连接
        cursor.close()
        connect.close()
        
# 获取冷启动时间
    def get_launched_time2(self):
        for line in self.content.readlines():
            line = line.strip() 
            if "ThisTime" in line:
                self.startTime = line.split(":")[1]
                #print (self.startTime)
            if "TotalTime" in line:
                self.startTime2 = line.split(":")[1]
                #print (self.startTime2)
            if "WaitTime" in line:
                self.startTime3 = line.split(":")[1] 
                #print (self.startTime3) 
                    
        print (self.startTime,self.startTime2,self.startTime3)  
        # 数据存数据库连接数据库
        connect = pymysql.Connect(
        host='10.0.3.140',
        port=3306,
        user='root',
        passwd='Aa654321',
        db='test',
        charset='utf8'
        )
           # 获取游标
        cursor = connect.cursor()
        sql = "INSERT INTO and_qidtime (leng_ThisTime,leng_TotalTime,leng_WaitTime) VALUES('"+self.startTime+"','"+self.startTime2+"','"+self.startTime3+"')"
        cursor.execute(sql)
        connect.commit()
           # 关闭连接
        cursor.close()
        connect.close()        

# 控制类
class Controller(object):
    def __init__(self, count):
        self.app = App()
        self.counter = count
        self.all_data = [("timestamp", "elapsedTime")]
    # 单次测试过程
    def test_process(self):
        #热启动
        self.app.launch_app()
        time.sleep(2)
        self.app.get_launched_time()
        self.app.stop_app()
        time.sleep(2) #间隔要延迟，不然运行太快，数据为0不准确
    # 多次执行测试过程
    def run(self):
        while self.counter > 0:
            self.test_process()
            self.counter = self.counter - 1

    # 获取当前的时间戳
    @staticmethod
    def get_current_time():
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return current_time
# 控制类
class Controller2(object):
    def __init__(self, count):
        self.app = App()
        self.counter = count
        self.all_data = [("timestamp", "elapsedTime")]
    # 单次测试过程
    def test_process(self):
        #冷启动
        self.app.launch_app()
        time.sleep(2)
        self.app.get_launched_time2()
        self.app.stop_app2()
        time.sleep(2)#间隔要延迟，不然运行太快，数据为0不准确
    # 多次执行测试过程
    def run2(self):
        while self.counter > 0:
            self.test_process()
            self.counter = self.counter - 1

    # 获取当前的时间戳
    @staticmethod
    def get_current_time():
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return current_time



if __name__ == '__main__':
    controller = Controller(10)
    controller.run()
    
    controller = Controller2(10)
    controller.run2()
    
