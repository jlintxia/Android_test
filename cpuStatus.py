# encoding:utf-8
import csv
import os
import time


# 控制类
class Controller(object):
    def __init__(self, count):
        self.result = ""
        self.counter = count
        self.all_data = [("timestamp", "cpuStatus")]

    # 单次测试过程
    def test_process(self):
        # window 下用findstr，Mac下用grep
        cmd = "/System/Volumes/Data/mytest/rj/sdk/platform-tools/adb shell top | /usr/bin/grep com.appsinnova.android.keepclean"
        self.result = os.popen(cmd)
       # time.sleep(2)
        
        for line in self.result.readlines():
            cpu_value =line.strip() 
        print (cpu_value)
         
    # 多次执行测试过程
    def run(self):
        while self.counter > 0:
            self.test_process()
            self.counter = self.counter - 1
            # 每3秒采集一次数据
            time.sleep(1)

    # 获取当前的时间戳
    @staticmethod
    def get_current_time():
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return current_time



if __name__ == '__main__':
    controller = Controller(10)
    controller.run()
