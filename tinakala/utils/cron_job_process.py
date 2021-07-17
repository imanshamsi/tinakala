from django.core.management import call_command


def django_process_background_tasks():
    call_command('process_tasks')
