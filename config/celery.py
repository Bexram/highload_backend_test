from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('test')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(300.0, update_db.s(), name='update_db')


@app.task
def update_db():
    from groups.models import Group
    from services.vk import get_data_from_vk

    for group in Group.objects.all():
        get_data_from_vk(group.id, 'update')
