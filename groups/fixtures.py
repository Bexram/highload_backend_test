import random

from groups.models import Group


def generate_groups(count):
    for i in range(count):
        Group.objects.create(title='Group', users_count=random.randint(1, 999))
