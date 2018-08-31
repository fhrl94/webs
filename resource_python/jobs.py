
from apscheduler.schedulers.background import BackgroundScheduler

from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from research.views import to_mail

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "cron", hour=4, minute=0, id="auto_calculate", replace_existing=True, misfire_grace_time=60*1)
def test_job():
    to_mail()


register_events(scheduler)

scheduler.start()
print("Scheduler started!")

## 下面这句加在定时任务模块的末尾...判断是否运行在uwsgi模式下, 然后阻塞mule主线程(猜测).
try:
    import uwsgi
    while True:
        sig = uwsgi.signal_wait()
        print(sig)
except Exception as err:
    pass