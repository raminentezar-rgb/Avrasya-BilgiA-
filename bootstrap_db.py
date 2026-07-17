import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')
django.setup()

from base.models import User

def bootstrap():
    if User.objects.count() == 0:
        print("Database is empty! Automatically loading initial_data.json (including superuser ramin and all topics)...")
        try:
            call_command('loaddata', 'initial_data.json')
            print("Successfully bootstrapped initial users, superusers, and topics into the database.")
        except Exception as e:
            print(f"Error during bootstrap: {e}")
    else:
        print("Database already contains users/data. Skipping initial data loading to preserve live data.")

if __name__ == '__main__':
    bootstrap()
