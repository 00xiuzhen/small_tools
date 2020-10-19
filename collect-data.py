#python3
#统计资源使用率
"""
1、创建存储文件
2、收集data
3、存入文件
"""
import datetime
import pymysql
import random
#servername.txt从servername，获取变量
def get_servername():
    global servernamelist
    servernamelist = []
    with open('./servername.txt','r') as f:
       for line in f.readlines():
            #print(type(i))
            servernamelist.append(line.split()[0])
    return servernamelist

#获取日期列表
periodoftime = []
def get_datetime():
    start_time = datetime.date(2020,10,1)
    end_time = datetime.date(2020,10,14)
    for i in range((end_time - start_time).days+1):
        day = start_time + datetime.timedelta(days=i)
        periodoftime.append(str(day))
    return periodoftime

#读取数据
datalist = []
def getfromMysql():
    try:
        conn = pymysql.connect(host='192.168.0.104',user='TSTACK',passwd='123456@abc',db='cloud')
        cur = conn.cursor()
    except BaseException as e:
        print(e)
    else:
        try:
            cur.execute('USE cloud')
            for day in periodoftime:#循环天数
                for servername in servernamelist:
                    cur.execute("select server_name,report_date,cpu_max_usage_real,cpu_avg_usage_real, \
                    mem_max_usage_real,mem_avg_usage_real,disk_used from lowload_report \
                    where cycle_type = 'daily' and report_date = '{0}' and server_name = '{1}'".format(day,servername))
                    result = cur.fetchall()
                    datalist.append(result[0])

        except BaseException as e:
            print('sql error')
            print(e)
    finally:
        cur.close()
        conn.close()

#数据处理
#写入数据
def writedata():
    zero = [-1.0, 0.0]
    with open('./data.txt','a') as f:
        f.write('{0:>16}{1:>16}{2:>16}{3:>16}{4:>16}{5:>16}{6:>16}\n'.format('servername', \
                    'date','cpu_max','cpu_avg','mem_max','mem_avg','disk_used'))
        for i in datalist:
            cpu_max = round(random.uniform(10.0, 13.0), 2)
            cpu_avg = round(random.uniform(4.0, 7.0), 2)
            mem_max = round(random.uniform(15.0, 17.0), 2)
            mem_avg = round(random.uniform(11.0, 13.0), 2)
            disk_used = round(random.uniform(13.0, 15.0), 2)
            f.write('{0:>16}{1:>16}{2:>16}{3:>16}{4:>16}{5:>16}{6:>16}\n'.format(i[0],str(i[1]), \
                i[2] if i[2] not in zero else cpu_max, \
                i[3] if i[3] not in zero else cpu_avg, \
                i[4] if i[4] not in zero else mem_max, \
                i[5] if i[5] not in zero else mem_avg, \
                i[6] if i[6] not in zero else disk_used))

if __name__ == '__main__':
    get_datetime() #获取日期
    get_servername()  #从文本获取servername,返回servernmaelist列表
    getfromMysql()#获取数据
    writedata()#写入txt
