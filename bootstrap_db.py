import os
import django
from django.core.management import call_command

def bootstrap():
    from base.models import User, Topic, DEPARTMENT_CHOICES
    print("Checking database status...")
    if User.objects.count() == 0:
        print("Database has no users. Attempting to load initial_data.json...")
        try:
            call_command('loaddata', 'initial_data.json')
            print("Successfully loaded initial_data.json.")
        except Exception as e:
            print(f"Notice: loaddata encountered an issue or partial load: {e}")

    # Guarantee Topics exist
    if Topic.objects.count() == 0:
        print("Populating initial Avrasya department topics...")
        for group_name, subchoices in DEPARTMENT_CHOICES:
            for val, label in subchoices:
                Topic.objects.get_or_create(name=label)
        print("Topics created.")

    # Guarantee Superuser ramin exists with guaranteed password 'ramin1234'
    ramin = User.objects.filter(username='ramin').first()
    if not ramin:
        ramin = User.objects.filter(email='raminentezarprogrammer@gmail.com').first()
        
    if not ramin:
        print("Creating superuser 'ramin'...")
        ramin = User.objects.create_superuser(
            username='ramin',
            email='raminentezarprogrammer@gmail.com',
            password='ramin1234',
            name='Ramin Entezar',
            role='faculty',
            department='İngiliz Dili ve Edebiyatı',
            is_staff=True,
            is_active=True
        )
        print("Superuser 'ramin' created successfully with password 'ramin1234'.")
    else:
        ramin.is_superuser = True
        ramin.is_staff = True
        ramin.is_active = True
        if not ramin.check_password('ramin1234'):
            ramin.set_password('ramin1234')
            ramin.save()
            print("Superuser 'ramin' updated with guaranteed password 'ramin1234'.")

    # Also guarantee an 'admin' fallback superuser
    admin = User.objects.filter(username='admin').first()
    if not admin:
        print("Creating fallback superuser 'admin'...")
        User.objects.create_superuser(
            username='admin',
            email='admin@avrasya.edu.tr',
            password='admin1234',
            name='Sistem Yöneticisi',
            role='faculty',
            department='Bilgisayar Mühendisliği',
            is_staff=True,
            is_active=True
        )
        print("Fallback superuser 'admin' created successfully with password 'admin1234'.")

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')
    django.setup()
    bootstrap()
