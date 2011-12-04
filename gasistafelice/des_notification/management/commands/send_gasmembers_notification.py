
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import notification

from gasistafelice.gas.models import GASMember


class Command(BaseCommand):
    args = ""
    help = 'Send notification to all gasmembers'

    def handle(self, *args, **options):
        
        for gm in GASMember.objects.all():

            notices = Notice.objects.notices_for(gm.user, on_site=True)

            if notices.count():

                des_notification.send_mail([gm.user], 
                    "gasmember_notification", 
                    {"from_user": from_user}, 
                    on_site=False
                )

        return 0

