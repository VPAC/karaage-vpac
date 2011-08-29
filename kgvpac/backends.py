from django.contrib.auth.backends import RemoteUserBackend as DjangoRemoteUserBackend


class RemoteUserBackend(DjangoRemoteUserBackend):

    create_unknown_user = False

