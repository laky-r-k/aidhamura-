from django.db import migrations
import os

# This function will be run by the migration
def setup_site(apps, schema_editor):
    # We get the Site model from the 'sites' app
    Site = apps.get_model('sites', 'Site')
    
    # We get your live domain name from an environment variable
    domain_name = os.environ.get('SITE_DOMAIN')
    
    # This is the key part: update_or_create
    # It tries to find a Site with pk=1.
    # - If it exists, it UPDATES its domain and name.
    # - If it does not exist, it CREATES it.
    # This makes the migration safe to run multiple times.
    Site.objects.update_or_create(
        pk=1,
        defaults={
            'domain': domain_name,
            'name': 'AIDHAMURA'
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        # This should be the name of your previous migration in the 'accounts' app
        ('accounts', '0002_create_superuser'),
        # We also depend on the sites app's own migrations
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(setup_site),
    ]