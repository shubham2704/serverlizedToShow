from celery.decorators import task
import time

@task(name="install Server")
def installServer():
    print("0")
    time.sleep(5)
    print("1")
    return "Completed"

    