from django.db import migrations
import os
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    # We get the User model
    User = get_user_model()

    # We get the superuser credentials from the environment variables
    # This is secure and flexible
    username = os.environ.get('ADMIN_USER')
    email = os.environ.get('ADMIN_EMAIL')
    password = os.environ.get('ADMIN_PASS')

    # We create the superuser only if it does not already exist
    if not User.objects.filter(username=username).exists():
        print(f'Creating superuser: {username}')
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print(f'Superuser {username} already exists.')


class Migration(migrations.Migration):

    dependencies = [
        # This should be the name of your previous migration file in the 'accounts' app
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]