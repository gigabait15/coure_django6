from MailingSetting.management.commands.scheduler import Command

def schedule_job(instance):
    Command().schedule_job(instance)