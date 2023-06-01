import os
from celery import Celery
from root.tasks import notify_telegram_group
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
app = Celery("root")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, notify_telegram_group.s(), name='add every 10')