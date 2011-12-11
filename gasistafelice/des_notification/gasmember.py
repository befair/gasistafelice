from django.contrib.auth.models import User
from notification.models import Notice
import notification

import logging

log = logging.getLogger(__name__)

#-------------------------------------------------------------------------------

def bulk_gasmembers_notification(unseen_since):
    """Retrieve all unseen user notices and send them via mail."""

    if not settings.DEBUG:
        recipients = User.objects.filter(person__gasmember_set__isnull=True).distinct()
    else:
        recipients = User.objects.filter(is_superuser=True)
    
    for user in recipients:

        notices = Notice.objects.notices_for(user, 
            on_site=True, unseen=True, added__gte=unseen_since
        )

        try:
            notification.send([user], "gasmember_notification", {
                'notices' : notices,
            }, on_site=False)

        except Exception as e:
            log.error("Send msg gasmember_notification: %s (%s)" % (e.message, type(e)))
            print 'EEEEEEEEEEEEEE  notification gasmember_notification %s (%s)' % (e.message, type(e))
            pass

        for n in notices:
            n.unseen = False
            n.save()


