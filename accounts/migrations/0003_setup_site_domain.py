from django.db import migrations
import os

def setup_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    domain_name = os.environ.get('SITE_DOMAIN')

    if domain_name:
        Site.objects.update_or_create(
            pk=1,  # Use pk=1 to match SITE_ID = 1
            defaults={
                'domain': domain_name,
                'name': 'AIDHAMURA'
            }
        )
        print(f"Site domain set to: {domain_name}")
    else:
        print("\n⚠️ WARNING: SITE_DOMAIN environment variable not set. Skipping site setup.")


class Migration(migrations.Migration):

    dependencies = [
        # This must point to your PREVIOUS migration in the SAME app ('accounts')
        ('accounts', '0002_create_superuser'),
        # This dependency on the 'sites' app is also required
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(setup_site),
    ]