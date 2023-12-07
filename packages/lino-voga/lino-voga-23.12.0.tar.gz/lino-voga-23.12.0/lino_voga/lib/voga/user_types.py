# Copyright 2015-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Defines the standard user roles for Lino Voga.

See also :ref:`voga.specs.profiles`.

See also :attr:`lino.core.site.Site.user_types_module`.

"""

from lino.core.roles import UserRole, SiteUser, SiteAdmin, SiteStaff, Explorer
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.search.roles import SiteSearcher
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino_xl.lib.ledger.roles import LedgerUser, VoucherSupervisor, LedgerStaff, LedgerPartner
from lino_xl.lib.notes.roles import NotesUser, NotesStaff
from lino_xl.lib.sepa.roles import SepaStaff
from lino_xl.lib.products.roles import ProductsStaff
from lino_xl.lib.courses.roles import CoursesTeacher, CoursesUser
from lino_xl.lib.cal.roles import GuestOperator, CalendarGuest, CalendarReader
from lino.modlib.checkdata.roles import CheckdataUser


class Receptor(SiteUser, CoursesUser, ContactsUser, OfficeUser,
               NotesUser,
               LedgerUser, CheckdataUser, ExcerptsUser, SiteSearcher, CalendarReader):
    pass


class Secretary(Receptor, SiteStaff, ContactsStaff, ExcerptsUser,
                VoucherSupervisor, ProductsStaff, Explorer, GuestOperator):
    pass


class Teacher(CoursesTeacher, CalendarReader):
    """Can register presences of participants, i.e. mark them as absent or present.

    """
    pass


class Pupil(CalendarGuest, LedgerPartner, CalendarReader):
    """Can confirm invitations to calendar events.

    """
    pass


class SiteAdmin(SiteAdmin, CoursesUser, ContactsStaff, OfficeStaff,
                NotesStaff, LedgerStaff, SepaStaff, CheckdataUser,
                GuestOperator, ExcerptsStaff, ProductsStaff,
                Explorer, SiteSearcher, CalendarReader):
    pass


class Anonymous(CalendarReader):
    pass


from django.utils.translation import gettext_lazy as _
from lino.modlib.users.choicelists import UserTypes
UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"), Anonymous, name='anonymous', readonly=True)
add('100', _("User"), Receptor, name='user')
add('200', _("Secretary"), Secretary, name='secretary')
add('300', _("Teacher"), Teacher, name='teacher')
add('400', _("Pupil"), Pupil, name='pupil')
add('900', _("Administrator"), SiteAdmin, name='admin')


from lino_xl.lib.storage.choicelists import StorageStates
StorageStates.clear()
add = StorageStates.add_item
add('10', _("Purchased"), 'purchased')
