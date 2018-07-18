#coding:utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

class Config:
    SECRET_KEY =  '1AR4bnTnLHZyHaKt' #os.environ.get('SECRET_KEY') or
    # SQLALCHEMY_POOL_SIZE = 100
    # SQLALCHEMY_MAX_OVERFLOW = 0
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_NUM_PER_PAGE = 5
    FLASK_NUM_PER_PAGE_LIST = 6
#SESSION_TYPE= 'redis'
    SESSION_PERMANENT = True
    # SESSION_KEY_PREFIX='sessionp'
    # ALARM_LEVEL=0
    MAX_CHAR_PER_COMMENT = 20

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hard_guess@localhost:3306/testdb1?charset=utf8'

class Development2Config(Config):
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # string= os.path.join(basedir,'projects\inventory2\database\data.sqlite')
    # print("path:"+string)
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\projects\\inventory2\\database\\data.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///'+string

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Aosien2016@120.76.207.142:3306/inventory?charset=utf8'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Aosien2016@120.76.207.142:3306/inventory?charset=utf8'


config = {
    'development': DevelopmentConfig,
    'development2': Development2Config,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
from enum import Enum
class Oprenum(Enum):
    INITADD = 1
    INBOUND = 2
    OUTBOUND = 3
    RESTORE = 4
    REWORK = 5
    BUYING = 6
    CANCELBUY=7
    SCRAP=8

oprenumCH ={
    Oprenum.INITADD.name: '新添加',
    Oprenum.INBOUND.name: '入库',
    Oprenum.OUTBOUND.name: '出库',
    Oprenum.RESTORE.name: '修好',
    Oprenum.REWORK.name: '返修中',
    Oprenum.BUYING.name:"购买中",
    Oprenum.CANCELBUY.name:'取消购买',
    Oprenum.SCRAP.name:'报废'
}
oprenumNum = {
    '入库':Oprenum.INBOUND,
    '出库':Oprenum.OUTBOUND,
    '修好':Oprenum.RESTORE,
    '返修':Oprenum.REWORK,
    '购买':Oprenum.BUYING,
    '不买':Oprenum.CANCELBUY,
    '报废':Oprenum.SCRAP
}
class Sensorname(Enum):
    P25 = 1
    P10 = 2
    TSP = 3
    NOISE = 4
    WINDSPEED = 5
    WINDDIRECTION = 6
    TEMP = 7
    PRESSURE = 8
    HUMIDITY = 9
    NEGOXYGEN = 10
    RAINFALL = 11
    ILLUM = 12
    CH2O = 13
    SO2 = 14
    NO2 = 15
    O3 = 16
    CO = 17
    CO2 = 18
    H2S = 19
    VOC = 20
    O2 = 21
    RADIATION = 22
    NH3 = 23
    SOILTEMP = 24
    SOILHUMIDITY = 25
    PHOTOSYNTHESIS = 26
    ULTRAVIOLETRAYS = 27


class Param(Enum):
    PARAM_8 = 8
    PARAM_7 = 7
    PARAM_5 = 5
    PARAM_3 = 3
    PARAM_0 = 0

params = {
    Param.PARAM_8.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name, Sensorname.NOISE.name, Sensorname.WINDSPEED.name,
                             Sensorname.WINDDIRECTION.name, Sensorname.TEMP.name, Sensorname.PRESSURE.name],
    Param.PARAM_7.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name, Sensorname.NOISE.name, Sensorname.WINDSPEED.name,
                             Sensorname.WINDDIRECTION.name, Sensorname.TEMP.name],
    Param.PARAM_5.name:  [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name, Sensorname.NOISE.name, Sensorname.WINDSPEED.name],
    Param.PARAM_3.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name]
}
paramnums = {
    Param.PARAM_8.name: [1, 1, 1, 1, 1, 1, 1, 1],
    Param.PARAM_7.name: [1, 1, 1, 1, 1, 1, 1],
    Param.PARAM_5.name:  [1, 1, 1, 1, 1],
    Param.PARAM_3.name: [1, 1, 1]
}

paramdict={
    Param.PARAM_8.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name, Sensorname.NOISE.name, Sensorname.WINDSPEED.name,
                             Sensorname.WINDDIRECTION.name, Sensorname.TEMP.name, Sensorname.PRESSURE.name],
    Param.PARAM_7.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name, Sensorname.NOISE.name, Sensorname.WINDSPEED.name,
                             Sensorname.WINDDIRECTION.name, Sensorname.TEMP.name],
    Param.PARAM_5.name:  [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name, Sensorname.NOISE.name, Sensorname.WINDSPEED.name],
    Param.PARAM_3.name: [Sensorname.P25.name, Sensorname.P10.name, Sensorname.TSP.name]
}



# oprenum = {
#     Oprenum.INITADD:'INITADD',
#     Oprenum.INBOUND:'INBOUND',
#     Oprenum.OUTBOUND:'OUTBOUND',
#     Oprenum.REWORK:'REWORK',
#     Oprenum.RESTORE:'RESTORE'
# }