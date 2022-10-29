from django.db import models


class VenueQuerySet(models.QuerySet):
    def filter_for_date(self, date):
        """
        Return records as seen on `date` from a material historical perspective.
        The records that have their `start_at` date and `end_at` date between
        the given `date`. If there is no `end_at` date, it means the record is
        still actual.
        If there are multiple records returned, the last added record (ie. with
        the highest `index`) is the most actual record from a formal historical
        perspective.
        """
        return (
            self.filter(start_at__lte=date)
            .filter(models.Q(end_at__gte=date) | models.Q(end_at__isnull=True))
            .order_by("-index")
        )

    def filter_for_registration_date(self, date):
        """
        Return records as seen on `date` and later, from a formal historical
        perspective.
        Typically, the first record in the result set represents the record as
        it is most actual from a material historical perspective.
        """
        return self.filter(registration_at__lte=date).order_by(
            "-registration_at", "-index"
        )