from AccessControl.SecurityInfo import allow_module
from datetime import date
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class AuthorityVocabulary:
    """ """

    def __call__(self, context=None):
        items = [
            ("", "Select a value ..."),
            ("de_bw", "Baden-Württemberg"),
            ("de_by", "Bayern"),
            ("de_be", "Berlin"),
            ("de_bb", "Brandenburg"),
            ("de_hb", "Bremen"),
            ("de_el", "Endlager (Bundesaufsicht)"),
            ("de_hh", "Hamburg"),
            ("de_he", "Hessen"),
            ("de_mv", "Mecklenburg-Vorpommern"),
            ("de_ni", "Niedersachsen"),
            ("de_nw", "Nordrhein-Westfalen"),
            ("de_rp", "Rheinland-Pfalz"),
            ("de_sl", "Saarland"),
            ("de_sn", "Sachsen"),
            ("de_st", "Sachsen-Anhalt"),
            ("de_sh", "Schleswig-Holstein"),
            ("de_th", "Thüringen"),
        ]
        terms = [SimpleTerm(code, code, title) for code, title in items]
        return SimpleVocabulary(terms)


AuthorityVocabularyFactory = AuthorityVocabulary()


@implementer(IVocabularyFactory)
class ReiLegalBaseVocabulary:
    """ """

    def __call__(self, context=None):
        return safe_simplevocabulary_from_values(
            [
                "REI-E",
                "REI-I",
            ]
        )


ReiLegalBaseVocabularyFactory = ReiLegalBaseVocabulary()


@implementer(IVocabularyFactory)
class MediumVocabulary:
    """ """

    def __call__(self, context=None):
        return safe_simplevocabulary_from_values(
            [
                "Fortluft",
                "Abwasser",
                "Abwasser/Fortluft",
            ]
        )


MediumVocabularyFactory = MediumVocabulary()


@implementer(IVocabularyFactory)
class PeriodVocabulary:
    """ """

    def __call__(self, context=None):
        items = [
            ("Y", "Jahr"),
            ("H1", "1. Halbjahr"),
            ("H2", "2. Halbjahr"),
            ("Q1", "1. Quartal"),
            ("Q2", "2. Quartal"),
            ("Q3", "3. Quartal"),
            ("Q4", "4. Quartal"),
            ("M1", "Januar"),
            ("M2", "Februar"),
            ("M3", "März"),
            ("M4", "April"),
            ("M5", "Mai"),
            ("M6", "Juni"),
            ("M7", "Juli"),
            ("M8", "August"),
            ("M9", "September"),
            ("M10", "Oktober"),
            ("M11", "November"),
            ("M12", "Dezember"),
        ]
        terms = [SimpleTerm(code, code, title) for code, title in items]
        return SimpleVocabulary(terms)


PeriodVocabularyFactory = PeriodVocabulary()


@implementer(IVocabularyFactory)
class PDFVersionVocabulary:
    """ """

    def __call__(self, context=None):
        return safe_simplevocabulary_from_values(
            [
                "keine Angabe",
                "PDF/A-1b",
                "PDF/A-1a",
                "PDF/A-2a",
                "PDF/A-2b",
                "PDF/A-2u",
                "PDF/A-3a",
                "PDF/A-3b",
                "PDF/A-3u",
            ]
        )


PDFVersionVocabularyFactory = PDFVersionVocabulary()


@implementer(IVocabularyFactory)
class MStIDVocabulary:
    """ """

    def __call__(self, context=None):
        items = [
            ("00000", "ESN Sicherheit und Zertifizierung GmbH"),
            (
                "00001",
                "Ministerium für Wirtschaft, Innovation,  Digitalisierung und Energie des Landes NRW",
            ),
            (
                "01002",
                "Ministerium für Energiewende, Landwirtschaft, Umwelt, Natur und Digitalisierung des Landes Schleswig-Holstein (SH)",
            ),
            ("01010", "Helmholtz-Zentrum hereon GmbH"),
            ("01011", "Helmholtz-Zentrum hereon GmbH"),
            ("01020", "Landesmessstelle Schleswig-Holstein - LMst 1 Kiel"),
            ("01051", "Kernkraftwerk Krümmel (KKK)"),
            ("01071", "Kernkraftwerk Brunsbüttel(KKB)"),
            ("01081", "Kernkraftwerk Brokdorf (KBR)"),
            ("01181", "SH-KTA-Brokdorf_SZL"),
            ("01551", "SH-KTA-Krümmel_SZL"),
            ("03020", "Universität Göttingen"),
            ("03040", "Landesmessstelle Niedersachsen - LMst 1 Hildesheim"),
            ("03060", "Landesmessstelle Niedersachsen - LMst 2 Hildesheim"),
            ("03102", "Landeszentrale Niedersachsen (NI)"),
            (
                "03132",
                "Niedersächsisches Ministerium für Umwelt, Energie, Bauen und Klimaschutz (MU)",
            ),
            ("03141", "Kernkraftwerk Lingen GmbH"),
            ("03151", "PreussenElektra GmbH Kernkraftwerk Stade"),
            ("03161", "PreussenElektra GmbH Kernkraftwerk Unterweser "),
            ("03171", "PreussenElektra GmbH Gemeinschaftskernkraftwerk Grohnde"),
            ("03191", "Kernkraftwerke Lippe-Ems GmbH Kernkraftwerk Emsland"),
            ("03201", "BGZ Gesellschaft für Zwischenlagerung mbH Betrieb Gorleben"),
            ("03211", "Konrad Schacht II"),
            ("03221", "Advanced Nuclear Fuels GmbH"),
            ("03231", "NI-KTA-Lingen_SZL"),
            ("03561", "NI-KTA-Unterweser_SZL"),
            ("03571", "NI-KTA-Grohnde_SZL"),
            ("04020", "Landesmessstelle Bremen - LMst 1 Bremen"),
            ("04032", "Landeszentrale Bremen (BR)"),
            ("05020", "Landesmessstelle Nordrhein-Westfalen - LMst 1 Duisburg"),
            ("05030", "Landesmessstelle Nordrhein-Westfalen - LMst 2 Düsseldorf"),
            ("05040", "Ruhrverband Ruhrtalsperrverein"),
            ("05050", "TüV Rheinland - Köln"),
            ("05060", "Staatliches Veterinäruntersuchungsamt"),
            ("05080", "Landwirtschaftliche Untersuchungs- und Forschungsanstalt"),
            ("05090", "Materialprüfungsamt des Landes NRW"),
            ("05091", "Forschungszentrum Jülich (FZJ)"),
            ("05092", "Arbeitsgemeinschaft Versuchsreaktor GmbH (AVR)"),
            ("05141", "Kernkraftwerk Würgassen(KWW)"),
            ("05151", "Prototypenkraftwerk Hamm-Uentrop (THTR-300)"),
            ("05161", "SNR-Versuchskraftwerk Kalkar (SNR-300)"),
            (
                "05171",
                "BGZ Gesellschaft für Zwischenlagerung mbH Brennelement-Zwischenlager Ahaus GmbH",
            ),
            ("05181", "Urananreicherungsanlage Gronau (UAG)"),
            ("06060", "Landesmessstelle Hessen - LMst 3 Darmstadt"),
            ("06101", "Kernkraftwerk Biblis"),
            (
                "06122",
                "Hessisches Ministerium für Umwelt, Klimaschutz, Landwirtschaft und Verbraucherschutz (HMUKLV)",
            ),
            ("06501", "HE-KTA-Biblis_SZL"),
            (
                "07002",
                "Ministerium für Umwelt, Energie, Ernährung und Forsten Rheinland-Pfalz (RP) / Landeszentrale Rheinland-Pfalz (RP)",
            ),
            ("07010", "Landesmessstelle Rheinland-Pfalz - LMst 1 Mainz"),
            ("07020", "Landesmessstelle Rheinland-Pfalz - LMst 4 Mainz"),
            ("07030", "Landesmessstelle Rheinland-Pfalz - LMst 2 Speyer"),
            ("07040", "Landesmessstelle Rheinland-Pfalz - LMst 5 Speyer"),
            ("07071", "Johannes Gutenberg Universität"),
            ("07081", "Anlage Mülheim-Kärlich (KMK)"),
            (
                "08002",
                "Ministerium für Umwelt,  Klima und Energiewirtschaft Baden-Württemberg (BW)",
            ),
            ("08010", "Landesmessstelle Baden-Württemberg - LMst 1 Karlsruhe"),
            ("08031", "Universität Hohenheim"),
            (
                "08041",
                "Karlsruher Institut für Technologie - Campus Nord stellvertretend für alle Betreiber von Anlagen und Einrichtungen am Standort (Kerntechnische Entsorgung Karlsruhe GmbH, Europäische Kommission - Joint Research Centre Karlsruhe, Zyklotron AG)",
            ),
            ("08061", "Staatliche milchwirtschaftliche Lehr- und Forschungsanstalt"),
            ("08082", "Landeszentrale Baden-Württemberg (BW)"),
            ("08101", "Kernkraftwerk Obrigheim"),
            ("08111", "EnBW Kernkraft GmbH Kernkraftwerk Neckarwestheim"),
            ("08121", "EnBW Kernkraft GmbH Kernkraftwerk Philippsburg"),
            ("08131", "Deutsches Krebsforschungszentrum Heidelberg"),
            ("08201", "Fachhochschule Ravensburg-Weingarten"),
            ("08210", "Landesfeuerwehrschule Baden-Württemberg"),
            ("08221", "Kerntechnische Hilfsdienst GmbH"),
            ("08511", "BW-KTA-Neckarwestheim_SZL"),
            ("08521", "BW-KTA-Philippsburg_SZL"),
            ("09030", "Landesmessstelle Bayern - LMst 3 Augsburg"),
            ("09051", "Nicht mehr verwendet"),
            ("09052", "Mirion Technologies (AWST) GmbH"),
            ("09081", "Landesgewerbeanstalt Bayern"),
            ("09082", "Bayerisches Geologisches Landesamt"),
            ("09111", "Technische Universität München"),
            ("09121", "Kernkraftwerk Isar1+2 GmbH"),
            ("09122", "Kernkraftwerk Isar 1 GmbH"),
            ("09123", "Bayernwerk AG"),
            ("09131", "Kernkraftwerk Grafenrheinfeld (KKG)"),
            ("09141", "Kernkraftwerk Gundremmingen (KRB)"),
            ("09151", "Versuchsatomkraftwerk Kahl GmbH (VAK)"),
            ("09161", "Siemens AG"),
            ("09162", "Framatome GmbH"),
            ("09171", "Siemens AG"),
            ("09181", "Siemens AG Brennelementewerk Hanau"),
            ("09192", "Landeszentrale Bayern (BY)"),
            ("09231", "Technischer Überwachungsverein e.V."),
            ("09300", "Universitäten in Bayern"),
            ("09521", "BY-KTA-Isar_SZL"),
            ("09531", "BY-KTA-Grafenrheinfeld_SZL"),
            ("09541", "BY-KTA-Gundremmingen_SZL"),
            ("10010", "Landesmessstelle Saarland - LMst 1 Saarbrücken"),
            ("10030", "Landesmessstelle Saarland - LMst 1 Saarbrücken"),
            ("10042", "Landeszentrale Saarland (SL)"),
            ("11010", "Landesmessstelle Berlin - LMst 1 Berlin"),
            ("11020", "Freie Universität Berlin"),
            (
                "11042",
                "Senatsverwaltung für Umwelt, Verkehr und Klimaschutz (BE) / Landeszentrale Berlin (BE)",
            ),
            ("11061", "Helmholtz-Zentrum Berlin für Materialien und Energie (BERII)"),
            ("12010", "Landesmessstelle Brandenburg - LMst 1 Oranienburg"),
            ("12032", "Landeszentrale Brandenburg (BB)"),
            ("12041", "Energiewerke Nord GmbH - Kernkraftwerk Rheinsberg"),
            (
                "13002",
                "Ministerium für Inneres und Europa Mecklenburg-Vorpommern (M-V)",
            ),
            ("13010", "Landesmessstelle Mecklenburg-Vorpommern - Stralsund"),
            ("13031", "EWN Entsorgungswerk für Nuklearanlagen GmbH "),
            ("13032", "Landeszentrale Mecklenburg-Vorpommern (MV)"),
            ("13033", "Energiewerke Nord GmbH - Zwischenlager Nord"),
            (
                "14002",
                "Sächsisches Staatsministerium für Energie, Klimaschutz, Umwelt und Landwirtschaft (SMEKUL)",
            ),
            ("14010", "Landesmessstelle Sachsen - LMst 1 Radebeul"),
            ("14032", "Landeszentrale Sachsen (SN)"),
            ("14040", "IAF-Radioökologie GmbH"),
            ("14041", "Forschungszentrum Rossendorf e.V"),
            ("15010", "Landesmessstelle Sachsen-Anhalt - LMst 1 Halle/Saale"),
            ("18001", "Endlager für radioaktive Abfälle Morsleben (ERAM)"),
            (
                "18002",
                "Bundesamt für Kerntechnische Entsorgungssicherheit Atomrechtliche Aufsicht",
            ),
            ("18003", "KTA Asse"),
        ]
        terms = [SimpleTerm(code, code, f"{code} - {title}") for code, title in items]
        return SimpleVocabulary(terms)


MStIDVocabularyFactory = MStIDVocabulary()


@implementer(IVocabularyFactory)
class OriginVocabulary:
    """ """

    def __call__(self, context=None):
        items = [
            "Strahlenschutzverantwortlicher",
            "unabhängige Messstelle",
        ]
        # Already existing Reports that have the now obsolete value "Genehmigungsinhaber"
        # need to find that in the vocabulary as well.
        origins = getattr(context, "Origins", []) or []
        if "Genehmigungsinhaber" in origins:
            items.append("Genehmigungsinhaber")
        return safe_simplevocabulary_from_values(items)


OriginVocabularyFactory = OriginVocabulary()


@implementer(IVocabularyFactory)
class YearVocabulary:
    """ """

    def __call__(self, context=None):
        items = []
        today = date.today()
        year = today.year
        while year > 1986:
            items.append(SimpleVocabulary.createTerm(year, str(year), str(year)))
            year = year - 1

        return SimpleVocabulary(items)


YearVocabularyFactory = YearVocabulary()


@implementer(IVocabularyFactory)
class NuclearInstallationVocabulary:
    """ """

    def __call__(self, context=None):
        items = [
            ("UCHL", "KTA Leibstadt mit Beznau und Villigen"),
            ("UELA", "Endlager für radioaktive Abfälle Asse"),
            ("UELM", "Endlager für radioaktive Abfälle Morsleben (ERAM)"),
            ("UFRC", "KKW Cattenom"),
            ("UFRF", "KKW Fessenheim"),
            ("U01A", "Helmholtz-Zentrum hereon"),
            ("U01B", "KKW Krümmel"),
            ("U01C", "KKW Brunsbüttel"),
            ("U01D", "KKW Brokdorf"),
            ("U01I", "Interimslager Krümmel"),
            ("U01K", "Brennelemente-Zwischenlager Krümmel (BZK)"),
            ("U01L", "Standortzwischenlager Brunsbüttel"),
            ("U01M", "Brennelemente-Zwischenlager Brokdorf (BZF)"),
            ("U03A", "Brennelemente-Zwischenlager Grohnde (BZD)"),
            ("U03B", "Brennelementefertigungsanl. Lingen"),
            ("U03C", "Brennelemente-Zwischenlager Unterweser (BZU)"),
            ("U03E", "KKW Emsland"),
            ("U03G", "KKW Grohnde"),
            ("U03K", "Endlager Konrad"),
            ("U03L", "KKW Lingen"),
            ("U03P", "BGZ - Betrieb Gorleben"),
            ("U03S", "KKW Stade"),
            ("U03U", "KKW Unterweser"),
            ("U03Z", "Brennelemente-Zwischenlager Lingen (BZL)"),
            ("U05B", "BGZ - Brennelement-Zwischenl. Ahaus"),
            ("U05F", "Forschungszentrum Jülich"),
            ("U05G", "AVR-Versuchskernkraftwerk Jülich"),
            ("U05K", "KKW Würgassen"),
            ("U05T", "Thorium-Hochtemp.reakt. Hamm-Uentrop"),
            ("U05U", "Urananreicherungsanlage Gronau"),
            ("U06B", "KKW Biblis und BE-Zwischenlager"),
            ("U07M", "KKW Mülheim-Kärlich"),
            ("U07U", "Uni Mainz"),
            ("U08H", "DKFZ Heidelberg"),
            (
                "U08K",
                "Karlsruher Institut für Technologie - Campus Nord (Einrichtungen am Standort)",
            ),
            ("U08M", "Abraumhalde Menz."),
            ("U08N", "EnKK Neckarwestheim"),
            ("U08O", "EnKK Obrigheim"),
            ("U08P", "EnKK Philippsburg"),
            ("U08W", "KKW Wyhl"),
            ("U09A", "KKW Isar 1+2"),
            ("U09B", "KKW Isar1"),
            ("U09C", "KKW Isar2"),
            ("U09D", "KKW Grafenrheinfeld"),
            ("U09E", "KKW Gundremmingen Block B/C"),
            ("U09F", "Versuchs-AKW Kahl a.M."),
            ("U09G", "Forschungsreaktor München"),
            ("U09H", "Siemens Brennelementewerk Hanau, Standort Karlstein"),
            ("U09I", "Siemens AG, Karlstein"),
            ("U09J", "Framatome GmbH, Forschungszentrum Erlangen-Süd (FZE)"),
            ("U09K", "Forschungsneutronenquelle Heinz Maier-Leibnitz"),
            ("U11B", "Experimentierreakt. II Berlin"),
            ("U12R", "KKW Rheinsberg"),
            ("U13A", "KKW Lubmin/Greifswald"),
            ("U13B", "Zwischenlager Nord"),
            ("U14R", "Forschungszentrum Rossendorf"),
            (
                "U15M",
                "nicht benutzen, jetzt UELM, Endlager für radioaktive Abfälle Morsleben (ERAM)",
            ),
        ]
        terms = [SimpleTerm(code, code, f"{code} {title}") for code, title in items]
        return SimpleVocabulary(terms)


NuclearInstallationVocabularyFactory = NuclearInstallationVocabulary()


allow_module("docpool.rei.vocabularies")
