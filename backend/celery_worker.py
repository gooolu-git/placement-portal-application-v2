from celery import Celery , Task
from celery.schedules import crontab
from app import app


#ye celery ka config hai isme pahle ham eek name diye hai celry ke liye - name_for_celery aur phir broker aur eek backend ka name aur last me bta rhe hai ki tasks name ke file me tumko sare functions milenge jisme tumko kam krna hai 
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/1',
    backend='redis://localhost:6379/2',
    include=['tasks']
)
#-- ye karne ke bad ham celery ko flask se jor rhe hai matlb ye ki abb celery flask ka sab chiz access kr saktha hai jaise flask-mail currtent_app.config's ko aur sql query kr sakta hai agar ye nhi krte hai to ye hamse runtime error dega flask bolega ki application out of context matlb ki ham nhi jante celery bhai tumko kon ho aur mere (flask) ke resources ko kaise use kr rhe ho  bin mahaul 
class FlaskTask(Task):
    def __call__(self,*args,**kwargs):
        with app.app_context():
            return self.run(*args,**kwargs)
celery_app.Task = FlaskTask

#setting the timezome

celery_app.conf.timezone='Asia/Kolkata'

celery_app.conf.beat_schedule = {
    'monthly-report': {
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(hour=8, minute=2, day_of_month=1),
    },
    'daily-reminder': {
        'task': 'tasks.send_daily_remainder',
        'schedule': crontab(hour=8, minute=5),
    },
}
