class BaseConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/zhaobiao?charset=utf8"
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 5
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 定时任务配置
    JOBS = [
        {
            'id': 'province',
            'func': 'apschedulerjob:spider_province',
            'args': '',
            'trigger': 'interval',
            'seconds': 30
        },
        {
            'id': 'city',
            'func': 'apschedulerjob:spider_city',
            'args': '',
            'trigger': 'interval',
            'seconds': 30
        }
    ]
    # 添加APS的API开关
    SCHEDULER_API_ENABLED = True