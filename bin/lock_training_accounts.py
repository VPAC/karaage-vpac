#!/usr/bin/env python

from django.core.management import setup_environ
from kgadmin.conf import settings
setup_environ(settings)

from django.conf import settings
from karaage.people.models import Person

if __name__ == "__main__":
    
    accounts = Person.active.filter(user__username__startswith='train')
    for account in accounts:
        account.lock()
        for a in account.useraccount_set.all():
            a.change_shell(settings.LOCKED_SHELL)
