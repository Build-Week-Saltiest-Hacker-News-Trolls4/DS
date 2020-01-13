from apscheduler.schedulers.blocking import BlockingScheduler

from main import main_process

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=2)
def api_access():
    main_process()
    print('This job is run every day.')

@sched.scheduled_job('interval', minutes=1)
def api_access_test():
    main_process()
    print('This job is run every day.')