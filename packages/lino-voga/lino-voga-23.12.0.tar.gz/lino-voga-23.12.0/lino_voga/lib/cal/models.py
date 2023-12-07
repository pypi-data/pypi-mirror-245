# -*- coding: UTF-8 -*-
# Copyright 2013-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from lino.api import _

from lino_xl.lib.cal.models import *
from lino.modlib.users.choicelists import UserTypes
from lino_xl.lib.courses.choicelists import EnrolmentStates
from lino.modlib.office.roles import OfficeUser


class Room(Room):

    class Meta(Room.Meta):
        abstract = dd.is_abstract_model(__name__, 'Room')

    fee = dd.ForeignKey('products.Product',
                        blank=True, null=True,
                        # verbose_name=_("Tariff"),
                        related_name='rooms_by_fee')

    # calendar = dd.ForeignKey(
    #     'cal.Calendar',
    #     help_text=_("Calendar where events in this room are published."),
    #     related_name='room_calendars',
    #     blank=True, null=True)

    # def __unicode__(self):
    #     s = mixins.BabelNamed.__unicode__(self)
    #     if self.company and self.company.city:
    #         s = '%s (%s)' % (self.company.city, s)
    #     return s

    def save(self, *args, **kwargs):
        super(Room, self). save(*args, **kwargs)

        if not self.calendar:
            return

        if not settings.SITE.loading_from_dump:

            user_types = set()
            for p in UserTypes.items():
                if p.has_required_roles([OfficeUser]):
                    user_types.add(p)
            User = settings.SITE.user_model
            for u in User.objects.filter(user_type__in=user_types):
                check_subscription(u, self.calendar)


class Rooms(Rooms):
    column_names = "name calendar fee company company__city *"
    detail_layout = """
    id name calendar
    fee company contact_person contact_role
    cal.EntriesByRoom
    """



class Event(Event):

    class Meta(Event.Meta):
        abstract = dd.is_abstract_model(__name__, 'Event')

    # invoiceable_date_field = 'start_date'
    invoiceable_partner_field = 'company'
    publisher_template = "cal/Event/page.pub.html"

    def get_invoiceable_product(self, max_date=None):
        # max_date = plan.max_date or plan.today
        if max_date and self.start_date > max_date:
            return
        if self.company and self.room:
            return self.room.fee

    def get_invoiceable_title(self, number=None):
        if self.company:
            return str(self.room)

    def get_invoiceable_qty(self):
        return 1

    def get_event_summary(self, ar):
        """Overrides :meth:`lino_xl.lib.cal.Event.get_event_summary`
        """
        if self.owner is None:
            yield self.summary
        else:
            yield str(self.owner)

    def __str__(self):
        if self.owner is None:
            return super().__str__()
        owner = self.owner._meta.verbose_name + " #" + str(self.owner.pk)
        return "%s %s" % (owner, self.summary)

    def suggest_guests(self):
        # print "20130722 suggest_guests"
        # for g in super(Event, self).suggest_guests():
        #     yield g
        if self.project is None:
            return
        if not settings.SITE.site_config.pupil_guestrole:
            return
        Guest = settings.SITE.models.cal.Guest
        found = set()
        for obj in self.project.enrolment_set.exclude(
                state=EnrolmentStates.cancelled):
            if obj.pupil:
                if obj.pupil.id not in found:
                    yield Guest(event=self,
                                partner=obj.pupil,
                                role=settings.SITE.site_config.pupil_guestrole)
                else:
                    found.add(obj.pupil.id)


class MyEntries(MyEntries):
    column_names = 'when_text detail_link #summary room owner workflow_buttons *'


@dd.receiver(dd.post_analyze)
def customize_cal(sender, **kw):
    site = sender

    dd.update_field(site.modules.cal.Event, 'description',
                    format="plain")

    site.modules.cal.Events.set_detail_layout('general more')
    site.modules.cal.Events.add_detail_panel('general', """
    event_type summary user
    start end
    room priority transparent #rset
    owner:30 workflow_buttons:30
    description
    """, _("General"))

    site.modules.cal.Events.add_detail_panel('more', """
    id created:20 modified:20  state
    #outbox.MailsByController cal.GuestsByEvent notes.NotesByOwner
    """, _("More"))

    site.modules.cal.Events.set_insert_layout(
        """
        start end
        room
        """,
        start="start_date start_time",
        end="end_date end_time",
        window_size=(60, 'auto'))
