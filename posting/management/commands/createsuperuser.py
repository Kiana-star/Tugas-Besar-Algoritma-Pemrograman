from django.contrib.auth.management.commands import createsuperuser

class Command(createsuperuser.Command):
    help = 'Create a superuser and set role as super_admin.'

    def handle(self, *args, **options):
        options['role'] = 'super_admin'  # Set role otomatis menjadi super_admin
        super().handle(*args, **options)
