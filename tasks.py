from celery import Celery, current_task
import time

celery = Celery(
    'tasks',
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

celery.set_default()

@celery.task(name="createSomeAsyncTask")
def createSomeAsyncTask(id):
    for x in range(int(id)):
        current_task.update_state(state='PROGRESS',meta={'id': id, 'x':x})
        time.sleep(1)
    current_task.update_state(state='SUCCESS',meta={'id': id, 'x':'done'})
    return id