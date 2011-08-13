from django.db.models.query import QuerySet

from datetime import date

class OrderQuerySet(QuerySet):

    def open(self):
        return self.filter(date_end__gte=date.today()) | self.filter(date_end__isnull=True)

    def closed(self):
        return self.filter(date_end__lt=date.today())

class AppointmentQuerySet(QuerySet):

    def future(self):
        """
        Return a QuerySet containing all appointments scheduled for today or for a future date.
        """
        return self.filter(date__gte=date.today())

    def past(self):
        """
        Return a QuerySet containing all past appointments.
        """
        return self.filter(date__lt=date.today())

