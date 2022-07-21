import random

from groups.models import Group


def generate_groups(count):
    for i in range(count):
        Group.objects.create(title=f'Group {i}', users_count=random.randint(1, 999))
