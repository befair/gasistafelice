from django.contrib.auth.models import User
from notification.models import Notice
import notification


#-------------------------------------------------------------------------------

def bulk_gasmembers_notification(unseen_since):
    """Retrieve all unseen user notices and send them via mail."""

    for user in User.objects.filter(person__gasmember_set__isnull=True).distinct():

        notices = Notice.objects.notices_for(user, 
            on_site=True, unseen=True, added__gte=unseen_since
        )

        notification.send([user], "gasmember_notification", {
            'notices' : notices,
        }, on_site=False)
        
        for n in notices:
            n.unseen = False
            n.save()

