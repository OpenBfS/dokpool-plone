# -*- coding: utf-8 -*-
__author__ = 'Condat AG'
__docformat__ = 'plaintext'

from docpool.dbaccess.content.structured import StructuredEntity
from docpool.dbaccess.dbinit import __metadata__
from docpool.dbaccess.dbinit import __session__
from elan.irix.db.security import IELANProtectedEntityClass
from elixir import Boolean
from elixir import DateTime
from elixir import Entity
from elixir import EntityBase
from elixir import Field
from elixir import Float
from elixir import Integer
from elixir import ManyToOne
from elixir import OneToMany
from elixir import setup_all
from elixir import Unicode
from elixir import UnicodeText
from formalchemy.validators import regex
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relationship
from zope.interface import provider

import logging


metadata = __metadata__
session = __session__


DEBUG = 0
__metadata__.bind.echo = False
if DEBUG:
    __metadata__.bind.echo = True
logger = logging.getLogger("elan.irix")


@provider(IELANProtectedEntityClass)
class IRIXEntity(StructuredEntity):
    pass


#########################################################################
# This is the representation of the IRIX schema as an Elixir data model
#########################################################################


class Report(Entity, IRIXEntity):
    """
    """

    _c_min_ = 1
    _c_max_ = 1

    title = Field(Unicode(255), required=True)

    # subobjects via OneToMany
    Identification = OneToMany('Identification', cascade='all')
    EventInformation = OneToMany('EventInformation', cascade='all')
    #  further sections of the report:
    #                <xsd:element ref="release:Release" minOccurs="0"/>
    #                <xsd:element ref="meteo:Meteorology" minOccurs="0"/>
    #                <xsd:element ref="con:Consequences" minOccurs="0"/>
    #                <xsd:element ref="pa:ResponseActions" minOccurs="0"/>
    #                <!--xsd:element ref="meas:Measurements" minOccurs="0"/-->
    #                <xsd:element ref="med:MedicalInformation" minOccurs="0"/>
    #                <xsd:element ref="media:MediaInformation" minOccurs="0"/>
    #                <xsd:element ref="req:Requests" minOccurs="0"/>

    def __repr__(self):
        return self.title


class Identification(Entity, IRIXEntity):
    """
    """

    _c_min_ = 1
    _c_max_ = 1

    OrganisationReporting = Field(Unicode(100), required=True)
    DatetimeOfSubmittal = Field(DateTime, required=True)
    ReportContext = Field(Unicode(100), required=True)
    UUID = Field(Unicode(100), required=True)
    Confidentiality = Field(Unicode(100), required=True)
    ReportsTo = OneToMany('ReportTo', cascade='all')
    ReportBases = OneToMany('ReportBasis', cascade='all')
    ContactPerson = Field(Unicode(100))  # email
    AdditionalInformationURI = Field(Unicode(100))  # URI
    EventIdentifications = OneToMany('EventIdentification', cascade='all')
    Identifications = OneToMany('Identifications', cascade='all')  # required

    # superobjects via ManyToOne (foreign key constraint)
    Report = ManyToOne('Report', ondelete='CASCADE', required=True)

    def __repr__(self):
        """
        If you want to see helpful names for objects in the navigation,
        you need to override __repr__ with something meaningful for the
        particular class.
        """
        return self.OrganisationReporting

    @classmethod
    def myfieldsetconfig(cls, fs):
        """
        If you need to explicitly define the form for creating and editing this object,
        override this method choosing the relevant fields, labels, renderers and validators.
        Only include the normal fields, not references to subobjects or superobjects.
        """
        return [
            fs.OrganisationReporting.label(
                "Reporting organisation").required(),
            fs.DatetimeOfSubmittal.label(
                "Date & time of submittal").required(),
            fs.ReportContext.label("Report Context")
            .dropdown(
                options=[
                    ('Emergency', 'emergency'),
                    ('Routine', 'routine'),
                    ('Exercise', 'exercise'),
                    ('Test', 'test'),
                ]
            )
            .required(),
            fs.UUID,
            fs.Confidentiality.dropdown(
                options=[
                    ('For recipients use only', 'recipients'),
                    ('For authority use only', 'authority'),
                    ('Free for public use', 'public'),
                ]
            ).required(),
            fs.ContactPerson.label("Contact person"),
            fs.AdditionalInformationURI.label("Additional information").validate(
                regex(
                    r"""http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"""
                )
            ),
        ]

    @classmethod
    def mygridconfig(cls, g):
        """
        If you need to define the columns for the list representation of this object,
        override this method choosing the relevant fields, labels and renderers.
        """
        return [
            g.OrganisationReporting.label("Reporting organisation"),
            g.DatetimeOfSubmittal.label("Date & time of submittal"),
            g.ReportContext.label("Report Context"),
        ]


class ReportTo(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 100
    OrganisationID = Field(Unicode(100), required=True)
    Through = Field(Unicode(100))
    Identification = ManyToOne(
        "Identification",
        ondelete='CASCADE',
        required=True)

    def __repr__(self):
        """
        If you want to see helpful names for objects in the navigation,
        you need to override __repr__ with something meaningful for the
        particular class.
        """
        return self.OrganisationID


class ReportBasis(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 100
    name = Field(Unicode(100), required=True)
    scheme = Field(Unicode(100))
    Identification = ManyToOne(
        "Identification",
        ondelete='CASCADE',
        required=True)

    def __repr__(self):
        """
        If you want to see helpful names for objects in the navigation,
        you need to override __repr__ with something meaningful for the
        particular class.
        """
        return self.name


class EventIdentification(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 100
    name = Field(Unicode(100), required=True)
    Organisation = Field(Unicode(100), required=True)
    Identification = ManyToOne(
        "Identification",
        ondelete='CASCADE',
        required=True)

    def __repr__(self):
        """
        If you want to see helpful names for objects in the navigation,
        you need to override __repr__ with something meaningful for the
        particular class.
        """
        return self.name


class Identifications(Entity, IRIXEntity):
    """
    """

    _c_min_ = 1
    _c_max_ = 1
    PersonalContactAddresses = OneToMany(
        'PersonalContactAddress', cascade='all')
    OrganisationContactAddresses = OneToMany(
        'OrganisationContactAddress', cascade='all'
    )  # required
    Identification = ManyToOne(
        "Identification",
        ondelete='CASCADE',
        required=True)


class PersonalContactAddress(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 100
    Name = Field(Unicode(100), required=True)
    UserID = Field(Unicode(100))
    Position = Field(Unicode(100))
    OrganisationID = Field(Unicode(100))
    PhoneNumber = Field(Unicode(100))
    FaxNumber = Field(Unicode(100))
    EmailAddress = Field(Unicode(100))
    Description = Field(UnicodeText)
    Identifications = ManyToOne(
        "Identifications",
        ondelete='CASCADE',
        required=True)

    def __repr__(self):
        """
        If you want to see helpful names for objects in the navigation,
        you need to override __repr__ with something meaningful for the
        particular class.
        """
        return self.Name


class OrganisationContactAddress(Entity, IRIXEntity):
    """
    """

    _c_min_ = 1
    _c_max_ = 100
    Name = Field(Unicode(100), required=True)
    OrganisationID = Field(Unicode(100), required=True)
    Country = Field(Unicode(100), required=True)
    WebAddress = Field(Unicode(100))
    Addresses = OneToMany("Address", cascade='all')
    PhoneNumber = Field(Unicode(100))
    FaxNumber = Field(Unicode(100))
    EmailAddress = Field(Unicode(100))
    Description = Field(UnicodeText)
    Identifications = ManyToOne(
        "Identifications",
        ondelete='CASCADE',
        required=True)

    def __repr__(self):
        """
        If you want to see helpful names for objects in the navigation,
        you need to override __repr__ with something meaningful for the
        particular class.
        """
        return self.Name


class Address(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 2
    Postbox = Field(Unicode(100))
    Street = Field(Unicode(100))
    PostalCode = Field(Unicode(50), required=True)
    Municipality = Field(Unicode(100), required=True)
    Country = Field(Unicode(100), required=True)
    Postalbox = Field(Unicode(100), required=True)
    Type = Field(Unicode(100), required=True)
    OrganisationContactAddress = ManyToOne(
        'OrganisationContactAddress', ondelete='CASCADE', required=True
    )


class EventInformation(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 1

    TypeOfEvent = Field(Unicode(100), required=True)
    TypeOfEventDescription = Field(Unicode(100))
    DateAndTimeOfEvent = Field(DateTime, required=True)
    LocationOfEvent = OneToMany('Location', cascade='all')
    ObjectInvolved = OneToMany('ObjectInvolved', cascade='all')
    EmergencyClassification = OneToMany(
        'EmergencyClassification', cascade='all')
    PlantStatus = OneToMany('PlantStatus', cascade='all')
    INESClassification = OneToMany('INESClassification', cascade='all')
    EventDescription = Field(UnicodeText)
    Report = ManyToOne('Report', ondelete='CASCADE', required=True)


class PlantStatus(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 1
    CoreState = OneToMany('CoreState', cascade='all')
    SpentFuelState = Field(UnicodeText)
    TrendInConditions = Field(Unicode(100))
    Description = Field(UnicodeText)
    EventInformation = ManyToOne(
        'EventInformation',
        ondelete='CASCADE',
        required=True)


class CoreState(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 1
    Criticality = OneToMany('Criticality', cascade='all')
    SevereDamageToFuel = OneToMany('SevereDamageToFuel', cascade='all')
    Description = Field(UnicodeText)
    PlantStatus = ManyToOne('PlantStatus', ondelete='CASCADE', required=True)


class SevereDamageToFuel(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 1
    Occurrence = Field(Unicode(100), required=True)
    TimeOfOccurrence = Field(DateTime)
    CoreState = ManyToOne('CoreState', ondelete='CASCADE', required=True)


class Criticality(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 1
    Status = Field(Unicode(100), required=True)
    StoppedAt = Field(DateTime)
    CoreState = ManyToOne('CoreState', ondelete='CASCADE', required=True)


class ObjectInvolved(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 1
    TypeOfObjectOrActivity = Field(Unicode(100), required=True)
    TypeOfObjectOrActivityDescription = Field(Unicode(100))
    Name = Field(Unicode(100), required=True)
    Location = OneToMany('ObjectLocation', cascade='all')
    SourceCharacteristics = OneToMany('Source', cascade='all')
    ReactorCharacteristics = OneToMany('ReactorCharacteristics', cascade='all')
    Description = Field(UnicodeText)
    EventInformation = ManyToOne(
        'EventInformation',
        ondelete='CASCADE',
        required=True)


class Source(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 100
    Sealed = Field(Boolean)
    Shielded = Field(Boolean)
    Nuclides = OneToMany('Nuclide', cascade='all')
    Description = Field(UnicodeText)
    ObjectInvolved = ManyToOne(
        'ObjectInvolved',
        ondelete='CASCADE',
        required=True)


class Nuclide(Entity, IRIXEntity):
    """
    """

    _c_min_ = 1
    _c_max_ = 100
    NuclideInfo = Field(Unicode(100))
    Activity = Field(Float)
    ActivityAt = Field(DateTime)
    Source = ManyToOne('Source', ondelete='CASCADE', required=True)


class ReactorCharacteristics(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 1
    TypeOfReactor = Field(Unicode(100))
    TypeOfReactorDescription = Field(Unicode(255))
    ThermalPower = Field(Integer)
    ElectricalPower = Field(Integer)
    Description = Field(UnicodeText)
    ObjectInvolved = ManyToOne(
        'ObjectInvolved',
        ondelete='CASCADE',
        required=True)


class INESClassification(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 1
    INESLevel = Field(Unicode(100), required=True)
    StatusOfClassification = Field(Unicode(100), required=True)
    DateTimeOfDeclaration = Field(DateTime)
    BasisForClassification = Field(UnicodeText)
    EventInformation = ManyToOne(
        'EventInformation',
        ondelete='CASCADE',
        required=True)


class EmergencyClassification(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 1
    EmergencyClass = Field(Unicode(100), required=True)
    EmergencyClassDescription = Field(Unicode(255))
    DateTimeOfDeclaration = Field(DateTime)
    BasisForClassification = Field(UnicodeText)
    EventInformation = ManyToOne(
        'EventInformation',
        ondelete='CASCADE',
        required=True)


class Location(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 1
    Name = Field(Unicode(100))
    GeographicLocation = Field(Unicode(100))
    Municipality = Field(Unicode(100))
    AdministrativeUnit = Field(Unicode(100))
    RegionCode = Field(Unicode(100))
    Country = Field(Unicode(100))
    AccuracyType = Field(Unicode(100))
    Description = Field(UnicodeText)
    EventInformation = ManyToOne('EventInformation', ondelete='CASCADE')


class ObjectLocation(Entity, IRIXEntity):
    """
    """

    _c_min_ = 0
    _c_max_ = 1
    Name = Field(Unicode(100))
    GeographicLocation = Field(Unicode(100))
    Municipality = Field(Unicode(100))
    AdministrativeUnit = Field(Unicode(100))
    RegionCode = Field(Unicode(100))
    Country = Field(Unicode(100))
    AccuracyType = Field(Unicode(100))
    Description = Field(UnicodeText)
    ObjectInvolved = ManyToOne('ObjectInvolved', ondelete='CASCADE')


@provider(IELANProtectedEntityClass)
class IRIXReport(EntityBase, IRIXEntity):

    @classmethod
    def fkName(cls):
        """
        Name of the foreign key used to reference instances from subentities
        """
        return "Report_id"

    def __repr__(self):
        """
        If you want to see helpful names for objects in the navigation,
        you need to override __repr__ with something meaningful for the
        particular class.
        """
        return self.title


setup_all(create_tables=True)

Identification.register()
ReportTo.register()
ReportBasis.register()
EventIdentification.register()
Identifications.register()
PersonalContactAddress.register()
OrganisationContactAddress.register()
Address.register()
EventInformation.register()
PlantStatus.register()
CoreState.register()
SevereDamageToFuel.register()
Criticality.register()
ObjectInvolved.register()
Source.register()
Nuclide.register()
ReactorCharacteristics.register()
INESClassification.register()
EmergencyClassification.register()
Location.register()
ObjectLocation.register()

j = (
    Report.table.join(
        Identification.table, Report.table.c.id == Identification.table.c.Report_id
    )
    .join(
        Identifications.table,
        Identification.table.c.id == Identifications.table.c.Identification_id,
    )
    .join(
        OrganisationContactAddress.table,
        Identifications.table.c.id
        == OrganisationContactAddress.table.c.Identifications_id,
    )
)
IRIXReport.mapper = mapper(
    IRIXReport,
    j,
    properties={
        'id': [Report.table.c.id, Identification.table.c.Report_id],
        'identification_id': [
            Identification.table.c.id,
            Identifications.table.c.Identification_id,
        ],
        'identifications_id': [
            Identifications.table.c.id,
            OrganisationContactAddress.table.c.Identifications_id,
        ],
        'oca_id': [OrganisationContactAddress.table.c.id],
        'Identification': relationship(
            Identification,
            primaryjoin=Report.table.c.id == Identification.table.c.Report_id,
            foreign_keys=[Identification.table.c.Report_id],
        ),  # primaryjoin=Person.table.c.nutzername == VPProperty.table.c.nutzer, foreign_keys=[VPProperty.table.c.nutzer] , , backref='portalnutzer'
        'EventInformation': relationship(
            EventInformation,
            primaryjoin=Report.table.c.id == EventInformation.table.c.Report_id,
            foreign_keys=[EventInformation.table.c.Report_id],
        ),  # primaryjoin=Person.table.c.nutzername == VPProperty.table.c.nutzer, foreign_keys=[VPProperty.table.c.nutzer] , , backref='portalnutzer'
    },
    primary_key=[Report.table.c.id],
)
