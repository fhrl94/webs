
from apscheduler.schedulers.background import BackgroundScheduler

from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from research.views import auto_calculate, to_mail

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "cron", hour=4, minute=0, id="auto_calculate", replace_existing=True)
def test_job():
    auto_calculate(None)
    to_mail()


register_events(scheduler)

scheduler.start()
print("Scheduler started!")