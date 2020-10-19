import multiprocessing as mp

workers = mp.cpu_count()*2+1    # 定義同時開啟的處理請求的進程數量，根據網站流量適當調整
# workers = 1
# preload = True
# worker_class = "gevent"   # 採用gevent，支持亦不處理請求，提高吞吐量
bind = "0.0.0.0:5000"    # 監聽IP放寬、以便於Docker之間、Docker和宿主機之間的通信
loglevel = 'debug'

# scheduler
# import gevent.monkey
# gevent.monkey.patch_ssl() # 修正gevent ssl無限遞迴錯誤
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# from app.database.postgresql import postgresql_uri

# import atexit
# from app.pkg.scheduler import func, listener

# jobstores = {
#     "sqlalchemy_pgsql": SQLAlchemyJobStore(url=postgresql_uri)
# }
# executors = {
#     'default': ThreadPoolExecutor(30), # 默認線程數
#     'processpool': ProcessPoolExecutor(30) # 默認進程
# }

# scheduler = BackgroundScheduler(misfire_grace_time=300, jobstores=jobstores, executors=executors)

# scheduler.add_job(func=func.set_forums_start, id="forums_start", trigger="cron", hour=11, minute=39, second=1, jobstore='sqlalchemy_pgsql', replace_existing=True)

# scheduler.start()

# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())