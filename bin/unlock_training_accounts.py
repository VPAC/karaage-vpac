#!/usr/bin/env python

from django.core.management import setup_environ
from kgadmin.conf import settings
setup_environ(settings)
import re

from karaage.people.models import Person

username_re = re.compile('([a-zA-Z]*)([0-9]*)')

if __name__ == "__main__":

    accounts = Person.active.filter(user__username__startswith='train')
	
    for account in accounts:
        m = username_re.match(account.username)
        prefix, number = m.groups()
        number = int(number) + 80
        account.unlock()
        account.set_password("Vtrain%s" % number)
        for a in account.useraccount_set.all():
            a.change_shell('/bin/bash')

 