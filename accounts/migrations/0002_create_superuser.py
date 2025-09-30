from django.db import migrations
import os
from django.contrib.auth import get_user_model
from django.utils import timezone  # <-- Import the timezone utility

def create_superuser(apps, schema_editor):
    User = get_user_model()
    username = os.environ.get('ADMIN_USER')
    email = os.environ.get('ADMIN_EMAIL')
    password = os.environ.get('ADMIN_PASS')

    if not User.objects.filter(username=username).exists():
        print(f'Creating superuser: {username}')
        # UPDATED: We now explicitly provide a value for last_login
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            last_login=timezone.now()  # <-- ADDED THIS LINE
        )
    else:
        print(f'Superuser {username} already exists.')


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]