# coding=utf8
import pymysql.cursors
import os
import configparser as cparser

# ======== 读取 db_config.ini 文件设置 ========
# os.path.dirname(__file__) 返回脚本的路径，脚本为py文件
base_dir = str(os.path.dirname(os.path.dirname(__file__)))

# replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)
base_dir = base_dir.replace('\\', '/')

file_path = base_dir + '/db_config.ini'

cf = cparser.ConfigParser()
cf.read(file_path)
'''
ConfigParser方法 
1、config=ConfigParser.ConfigParser()  
创建ConfigParser实例  
  
2、config.sections()  
返回配置文件中节序列  
  
3、config.options(section)  
返回某个项目中的所有键的序列  
  
4、config.get(section,option)  
返回section节中，option的键值  
  
5、config.add_section(str)  
添加一个配置文件节点(str)  
  
6、config.set(section,option,val)  
设置section节点中，键名为option的值(val)  
  
7、config.read(filename)  
读取配置文件  
  
8、config.write(obj_file)  
写入配置文件
'''


host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
db   = cf.get("mysqlconf", "db_name")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")

# ======== 封装 MySQL 基本操作 ========
class DB:
    def __init__(self):
        try:
            # 连接数据库
            self.connection = pymysql.connect(host=host,
                                              port=int(port),
                                              user=user,
                                              password=password,
                                              db=db,
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # 清除表数据
    def clear(self, table_name):
        real_sql = "delete from " + table_name +";"
        with self.connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.connection.commit()

    # 插入表数据
    def insert(self,table_name, table_data):
        for key in table_data:
            table_data[key] = "'"+str(table_data[key])+"'"
        key   = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        #print(real_sql)

        with self.connection.cursor() as cursor:
            cursor.execute(real_sql)

        self.connection.commit()

    # 关闭数据库
    def close(self):
        self.connection.close()

    # init data
    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()


if __name__ == '__main__':
    db = DB()
    table_name = "sign_event"
    data = {'id':1, 'name':'红米', '`limit`':2000, 'status':1,'address':'北京会展中心', 'start_time': '2016-08-20 00:25:42'}
    table_name2 = "sign_guest"
    data2 = {'realname':'alen','phone':12312341234,'email':'alen@mail.com','sign':0,'event_id':1}
    db.clear(table_name)
    db.insert(table_name, data)
    db.close()