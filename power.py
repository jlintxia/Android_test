# encoding:utf-8
import csv
import os
import time
import pymysql.cursors

# 控制类 应用电量
class Controller(object):
    def __init__(self, count):
        # 定义测试的次数
        self.counter = count
        # 定义收集数据的数组
        self.all_data = [("timestamp", "power")]

    # 单次测试过程
    def test_process(self):
        cmd = "adb shell dumpsys battery"
        result = os.popen(cmd)

        for line in result:
            if "level" in line:
                power = line.split(":")[1]
        print('电量',power)
        # 获取当前时间
        #current_time = self.get_current_time()
        # 将获取到的数据存到数组中
        #self.all_data.append((current_time, power))
        
# 数据存数据库连接数据库
        connect = pymysql.Connect(
        host='172.26.1.39',
        port=3306,
        user='root',
        passwd='Aa123456',
        db='test',
        charset='utf8'
            )
           # 获取游标
        cursor = connect.cursor()
        sql = "INSERT INTO and_power (power) VALUES('"+power+"')"
        cursor.execute(sql)
        connect.commit()
           # 关闭连接
        cursor.close()
        connect.close()
    # 多次执行测试过程
    def run(self):
        cmd = "adb shell dumpsys battery set status 1"
        os.popen(cmd)
        while self.counter > 0:
            self.test_process()
            self.counter = self.counter - 1
            # 每5秒采集一次数据, 真实测试场景建议在0.5-1小时
            time.sleep(3)

    

if __name__ == '__main__':
    controller = Controller(5)
    controller.run()
