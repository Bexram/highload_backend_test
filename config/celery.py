from __future__ import absolute_import, unicode_literals

import asyncio
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
async def update_db():
    from services.vk import get_data_from_vk
    from groups.views import _get_groups_ids
    groups = await _get_groups_ids()
    queue = asyncio.Queue()
    task_list = []
    for group in groups:
        task = asyncio.create_task(get_data_from_vk(group, 'update'))
        task_list.append(task)
    await queue.join()
    await asyncio.gather(*task_list, return_exceptions=True)
    await asyncio.gather(*task_list, return_exceptions=True)
