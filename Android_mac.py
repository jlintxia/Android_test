import os
import subprocess
import time
import pymysql.cursors
import threading
import re
from time import sleep
 
#测试设备ID
devices='BH907HED9G'
#测试应用包名称
packages ="com.appsinnova.android.keepclean"
 #测试应用Activity名称
app_bundle_id = 'com.appsinnova.android.keepclean/com.appsinnova.android.keepclean.ui.SplashActivity'
#热启动和冷启动测试次数，推荐10次
a=10






#获取CPU和内存测试时长,单位秒，预留开关，暂时忽略
b=30
#本地adb路径,默认不改
adb=os.getcwd()+'/adb'

class Utils(object):
    # 根据包名获取Pid
    @staticmethod
    def get_pid_by_package_name(pkg):
        pid = os.popen(adb +' -s ' +  devices +' shell pidof '+pkg).read()
        #print(pid)
        return pid
        

# APP类
class App(object):
    def __init__(self):
        self.content = ""
        self.startTime = 0
    
    
    # 启动APP
    def launch_app1(self):
        cmd = adb+' shell am start -W -n '+app_bundle_id  # type: str
        self.content = os.popen(cmd)
    # 停止app，热启动
    @staticmethod
    def stop_app():
        # 冷启动停止的命令：完全杀进程，再启动
        # cmd = 'adb shell am force-stop org.chromium.webview_shell'
        # 热启动停止的命令,启动完至于后台
        cmd = adb+' shell input keyevent 3'
        os.popen(cmd)
 # 停止app，冷启动
    @staticmethod
    def stop_app2():
        # 冷启动停止的命令：完全杀进程，再启动
        cmd = adb+' shell am force-stop '+packages
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
    
    # 内存
    def launch_app(self):
        # cmd = '/System/Volumes/Data/mytest/rj/sdk/platform-tools/adb -s ' +  devices +' shell "dumpsys meminfo com.appsinnova.android.keepclean"'
        # self.content = os.popen(cmd)
        
        cmd = adb+' -s ' +  devices +' shell dumpsys meminfo '+packages
        # result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # output, error = result.communicate(timeout=1000)
        # kkp=str(output.decode())
        #print(kk)
        
        nc = os.popen(cmd).read()
        print(nc)
        
#单位KB 占用总内存
       # current_time = self.get_current_time()
        pp= nc.split("TOTAL")[1].split("App Summary")[0][0:12]
        te=str(int(pp)/1024).split(".")[0]
        print('占用总内存'+te) #单位MB
        #time.sleep(1)
        #剩余内存
        pp2= nc.split("TOTAL")[1].split("App Summary")[0][-12:]
        te2=str(int(pp2)/1024).split(".")[0]
        print('剩余内存'+te2)#单位MB
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
        sql = "INSERT INTO and_meminfo (total,heap_free) VALUES('"+te+"','"+te2+"')"
        cursor.execute(sql)
        connect.commit()
       # 关闭连接
        cursor.close()
        connect.close()
        
        
        
    TIME = "time"
    NATIVE_HEAP = "Native Heap(MB)"
    DALVIK_HEAP = "Dalvik Heap(MB)"    
         # 内存
    def launch_app11(self):
         t = threading.Thread(target=self.get_mem_info)
         t.start()
         
    def get_mem_info(self):
        mem_field_names = [self.TIME, self.NATIVE_HEAP, self.DALVIK_HEAP]
        while 5 != 0:
            # 测试应用占用总内存
            native_info = os.popen(adb+' shell dumpsys meminfo '+packages+' | grep "TOTAL"').read()
            native_pss = format(int(re.findall(r"\d+", native_info)[0]) / 1000.0, ".1f")
            # 当前手机剩余内存
            dalvik_info = os.popen(adb+' shell dumpsys meminfo  | grep "Free"').read()
            fm=int(dalvik_info.split("Free RAM:")[1].split("(")[0].split("K")[0].replace(',',' ').replace(' ', '') )/1024
            fm3=str(fm).split(".")[0]
            print(fm3)
            print('测试应用内存',native_pss)
            print('剩余内存',fm3)
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
            sql = "INSERT INTO and_meminfo (total,heap_free) VALUES('"+native_pss+"','"+fm3+"')"
            cursor.execute(sql)
            connect.commit()
           # 关闭连接
            cursor.close()
            connect.close()
            
         
        # CPU
    def launch_app2(self):
        
        t = threading.Thread(target=self.get_cpu_info)
        t.start()
        
        
       
    # 总的CPU信息
    def get_cpu_usage(self):
        cpu_usage = 0.0
        cpu_path = "/proc/stat"
        info = os.popen(adb+' shell cat '+cpu_path).read()
        result = re.split("\s+", info.split("\n")[0])
        for i in range(2, len(result)):
            cpu_usage += float(result[i])
        return cpu_usage

    # 通过ID获取cpu信息（例如此时的今日头条进程id为10808）
    def get_process_cpu_usage(self):
        pid = Utils.get_pid_by_package_name(packages)
        kj=pid.replace("\n","")#去掉返回值里面的换行符
        #print('1测试',kj)
        kk=str(kj)
        cpu_path = "/proc/" + kk + "/stat"
        #print('2测试',cpu_path)
        info = os.popen(adb+' shell cat '+cpu_path).read()
        result = re.split("\s+", info)
        # 进程总的cpu占用
        cpu_usage = float(result[13]) + float(result[14])
        return cpu_usage    
         #
    TIME = "time"
    CPU_RATE = "进程CPU占比(%)"     
    def get_cpu_info(self):
        cpu_field_names = [self.TIME, self.CPU_RATE]
        while 5 != 0:
            start_all_cpu = self.get_cpu_usage()
            start_p_cpu = self.get_process_cpu_usage()
            sleep(1)
            end_all_cpu = self.get_cpu_usage()
            end_p_cpu = self.get_process_cpu_usage()
            cpu_rate = 0.0
            if (end_all_cpu - start_all_cpu) != 0:
                cpu_rate = (end_p_cpu - start_p_cpu) * 100.00 / (
                        end_all_cpu - start_all_cpu)
                if cpu_rate < 0:
                    cpu_rate = 0.00
                elif cpu_rate > 100:
                    cpu_rate = 100.00
            #print(f"CPU:【{format(cpu_rate, '.2f')}%】")
            cpu1=format(cpu_rate, '.2f')
            print(cpu1)
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
            sql = "INSERT INTO and_cpu (cpu) VALUES('"+cpu1+"')"
            cursor.execute(sql)
            connect.commit()
            # 关闭连接
            cursor.close()
            connect.close()
            sleep(0.5)


    
    DOWN_SPEED = "下载速度(KB/s)"
    UP_SPEED = "上传速度(KB/s)"
    AVERAGE_DOWN_SPEED = "平均下载速度(KB/s)"
    AVERAGE_UP_SPEED = "平均上传速度(KB/s)"
    TOTAL_DOWN_SPEED = "下载总流量(KB)"
    TOTAL_UP_SPEED = "上传总流量(KB)"    
    def launch_app3(self):    
        pid = Utils.get_pid_by_package_name(packages)
        kj=pid.replace("\n","")#去掉返回值里面的换行符
        #print('1测试',kj)
        kk2=str(kj)
        net_command = adb+' shell cat /proc/'+kk2+'/net/dev | grep "wlan"'
        while 5 != 0:
            if self.is_first:
                self.start_time = time.time_ns()
                self.last_time = self.start_time
                net_info = os.popen(net_command).read()
                net_array = re.split("\s+", net_info)
                self.start_net_down = int(net_array[2])
                self.last_net_down = self.start_net_down
                self.start_net_up = int(net_array[10])
                self.last_net_up = self.start_net_up
                self.is_first = False
            current_time = time.time_ns()
            current_info = os.popen(net_command).read()
            current_array = re.split("\s+", current_info)
            current_net_down = int(current_array[2])
            current_net_up = int(current_array[10])
            time_delta = (current_time - self.last_time) / 1000000000.0
            time_total = (current_time - self.start_time) / 1000000000.0
            net_delta_up = (current_net_up - self.last_net_up) / 1024.0
            net_delta_down = (current_net_down - self.last_net_down) / 1024.0
            net_total_up = (current_net_up - self.start_net_up) / 1024.0
            net_total_down = (current_net_down - self.start_net_down) / 1024.0
            net_speed_up = net_delta_up / time_delta
            net_speed_down = net_delta_down / time_delta
            net_average_speed_up = net_total_up / time_total
            net_average_speed_down = net_total_down / time_total
            print("下载速度：{:.2f} KB/s".format(net_speed_down))
            print("上传速度：{:.2f} KB/s".format(net_speed_up))
            # print("平均下载速度：{:.2f} KB/s".format(net_average_speed_down))
            # print("平均上传速度：{:.2f} KB/s".format(net_average_speed_up))
            print("下载总流量：{:.0f} KB/s".format(net_total_down))
            print("上传总流量：{:.0f} KB/s".format(net_total_up))
            self.last_time = current_time
            self.last_net_up = current_net_up
            self.last_net_down = current_net_down
            #下载/上传速度
            xz1=format(net_speed_down,".2f")
            xz2=format(net_speed_up,".2f")
            #总流量
            xz3=format(net_total_down,".0f")
            xz4=format(net_total_up,".0f")
            
              #数据存数据库连接数据库
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
            sql = "INSERT INTO and_wlan (down_net,up_net,total_down,total_up) VALUES('"+xz1+"','"+xz2+"','"+xz3+"','"+xz4+"')"
            cursor.execute(sql)
            connect.commit()
            # 关闭连接
            cursor.close()
            connect.close()
            sleep(0.5)
            
            
            
        
    def __init__(self):
        self.is_first = True
        self.last_time = 0
        self.last_net_up = 0
        self.last_net_down = 0
        self.start_time = 0
        self.start_net_up = 0
        self.start_net_down = 0 
    
       
        
# 控制类
class Controller1(object):
    def __init__(self, count):
        self.app = App()
        self.counter = count
        self.all_data = [("timestamp", "elapsedTime")]
    # 单次测试过程
    def test_process(self):
        #热启动
        self.app.launch_app1()
        time.sleep(2)
        self.app.get_launched_time()
        self.app.stop_app()
        time.sleep(2) #间隔要延迟，不然运行太快，数据为0不准确
    # 多次执行测试过程
    def run(self):
        while self.counter > 0:
            self.test_process()
            self.counter = self.counter - 1

     
    
# 控制类
class Controller2(object):
    def __init__(self, count):
        self.app = App()
        self.counter = count
        self.all_data = [("timestamp", "elapsedTime")]
    # 单次测试过程
    def test_process(self):
        #冷启动
        self.app.launch_app1()
        time.sleep(2)
        self.app.get_launched_time2()
        self.app.stop_app2()
        time.sleep(2)#间隔要延迟，不然运行太快，数据为0不准确
    # 多次执行测试过程
    def run2(self):
        while self.counter > 0:
            self.test_process()
            self.counter = self.counter - 1

   
    
 
     
# 控制类
class Controller(object):
    def __init__(self, count):
        self.app = App()
        self.counter = count
        self.all_data = [("timestamp", "elapsedTime")]
        
    # 单次测试过程
    def test_process(self):
        
        #self.app.launch_app()#这个单独运行可行，于其他性能同时获取会出现只能获取一次，脚本性能待优化
        
        self.app.launch_app11()
        self.app.launch_app2()
        self.app.launch_app3()
    # 多次执行测试过程
    def run(self):
        while self.counter > 0:
            self.test_process()
            self.counter = self.counter - 1
           # 每3秒采集一次数据
            time.sleep(2)
 

if __name__ == '__main__':
    #热启动
    controller = Controller1(a)
    controller.run()
    #冷启动
    controller = Controller2(a)
    controller.run2()
    pid = os.popen( adb+' shell am start -W -n '+app_bundle_id).read()#启动应用，防止没手动启动应用，无法获取性能数据
    
    #CPU和内存
    controller = Controller(b)
    controller.run()
    
    