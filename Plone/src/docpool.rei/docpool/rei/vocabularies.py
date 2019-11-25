# - * - coding: utf - 8 -*-
from AccessControl.SecurityInfo import allow_module
from datetime import date
from docpool.rei import DocpoolMessageFactory as _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


class VocabItem(object):
    def __init__(self, token, value, title):
        self.token = token
        self.value = value
        self.title = title


@implementer(IVocabularyFactory)
class AuthorityVocabulary(object):
    """
    """

    def __call__(self, context):
        items = [
            VocabItem(u'Kein Wert', _(u'Kein Wert'), u'Kein Wert'),
            VocabItem(u'Baden-Württemberg', _(u'Baden-Württemberg'), u'Baden-Württemberg'),
            VocabItem(u'Bayern', _(u'Bayern'), u'Bayern'),
            VocabItem(u'Berlin', _(u'Berlin'), u'Berlin'),
            VocabItem(u'BfE', _(u'BfE'), u'BfE'),
            VocabItem(u'Brandenburg', _(u'Brandenburg'), u'Brandenburg'),
            VocabItem(u'Bremen', _(u'Bremen'), u'Bremen'),
            VocabItem(u'Hamburg', _(u'Hamburg'), u'Hamburg'),
            VocabItem(u'Hessen', _(u'Hessen'), u'Hessen'),
            VocabItem(u'Mecklenburg-Vorpommern', _(u'Mecklenburg-Vorpommern'),u'Mecklenburg-Vorpommern',),
            VocabItem(u'Niedersachsen', _(u'Niedersachsen'), u'Niedersachsen'),
            VocabItem(u'Nordrhein-Westfalen', _(u'Nordrhein-Westfahlen'),'Nordrhein-Westfalen',),
            VocabItem(u'Rheinland-Pfalz', _(u'Rheinland-Pfalz'), u'Rheinland-Pfalz'),
            VocabItem(u'Saarland', _(u'Saarland'), u'Saarland'),
            VocabItem(u'Sachsen', _(u'Sachsen'), u'Sachsen'),
            VocabItem(u'Sachsen-Anhalt', _(u'Sachsen-Anhalt'), u'Sachsen-Anhalt'),
            VocabItem(u'Schleswig-Holstein', _(u'Schleswig-Holstein'), u'Schleswig-Holstein'),
            VocabItem(u'Thüringen', _(u'Thüringen'), u'Thüringen'),
        ]

        return SimpleVocabulary(items)


AuthorityVocabularyFactory = AuthorityVocabulary()


@implementer(IVocabularyFactory)
class ReiLegalBaseVocabulary(object):
    """
    """

    def __call__(self, context):
        items = [
            VocabItem(u'REI-E', _(u'REI-E'), u'REI-E'),
            VocabItem(u'REI-I', _(u'REI-I'), u'REI-I'),
            VocabItem(u'REI-E/REI-I', _(u'REI-E/REI-I'), u'REI-E/REI-I'),
        ]

        return SimpleVocabulary(items)


ReiLegalBaseVocabularyFactory = ReiLegalBaseVocabulary()


@implementer(IVocabularyFactory)
class MediaVocabulary(object):
    """
    """

    def __call__(self, context):
        items = [
            VocabItem(u'Fortluft', _(u'Fortluft'), u'Fortluft'),
            VocabItem(u'Abwasser', _(u'Abwasser'), u'Abwasser'),
            VocabItem(
                u'Fortluft/Abwasser', _(u'Fortluft/Abwasser'), u'Fortluft/Abwasser'
            ),
        ]

        return SimpleVocabulary(items)


MediaVocabularyFactory = MediaVocabulary()


@implementer(IVocabularyFactory)
class PeriodVocabulary(object):
    """
    """

    def __call__(self, context):
        items = [
            VocabItem(u'1. Quartal', _(u'1. Quartal'), u'1. Quartal'),
            VocabItem(u'2. Quartal', _(u'2. Quartal'), u'2. Quartal'),
            VocabItem(u'3. Quartal', _(u'3. Quartal'), u'3. Quartal'),
            VocabItem(u'4. Quartal', _(u'4. Quartal'), u'4. Quartal'),
            VocabItem(u'1. Halbjahr', _(u'1. Halbjahr'), u'1. Halbjahr'),
            VocabItem(u'2. Halbjahr', _(u'2. Halbjahr'), u'2. Halbjahr'),
            VocabItem(u'Jahr', _(u'Jahr'), u'Jahr'),
            VocabItem(u'Januar', _(u'Januar'), u'Januar'),
            VocabItem(u'Februar', _(u'Februar'), u'Februar'),
            VocabItem(u'März', _(u'März'), u'März'),
            VocabItem(u'April', _(u'April'), u'April'),
            VocabItem(u'Mai', _(u'Mai'), u'Mai'),
            VocabItem(u'Juni', _(u'Juni'), u'Juni'),
            VocabItem(u'Juli', _(u'Juli'), u'Juli'),
            VocabItem(u'August', _(u'August'), u'August'),
            VocabItem(u'September', _(u'September'), u'September'),
            VocabItem(u'Oktober', _(u'Oktober'), u'Oktober'),
            VocabItem(u'November', _(u'November'), u'November'),
            VocabItem(u'Dezember', _(u'Dezember'), u'Dezember'),
        ]

        return SimpleVocabulary(items)


PeriodVocabularyFactory = PeriodVocabulary()


@implementer(IVocabularyFactory)
class PdfVersionVocabulary(object):
    """
    """

    def __call__(self, context):
        items = [
            VocabItem(u'PDF/A-1b', u'PDF/A-1b', u'PDF/A-1b'),
            VocabItem(u'PDF/A-1a', u'PDF/A-1a', u'PDF/A-1a'),
            VocabItem(u'PDF/A-2a', u'PDF/A-2a', u'PDF/A-2a'),
            VocabItem(u'PDF/A-2b', u'PDF/A-2b', u'PDF/A-2b'),
            VocabItem(u'PDF/A-2u', u'PDF/A-2u', u'PDF/A-2u'),
            VocabItem(u'PDF/A-3a', u'PDF/A-3a', u'PDF/A-3a'),
            VocabItem(u'PDF/A-3b', u'PDF/A-3b', u'PDF/A-3b'),
            VocabItem(u'PDF/A-3u', u'PDF/A-3u', u'PDF/A-3u'),
        ]

        return SimpleVocabulary(items)


PdfVersionVocabularyFactory = PdfVersionVocabulary()


@implementer(IVocabularyFactory)
class MstVocabulary(object):
    """
    """

    def __call__(self, context):
        items = [
            VocabItem(u'1002 ', _(u'1002 '), u'SH-LDZ-Kiel '),
            VocabItem(u'1010 ', _(u'1010 '), u'SH-MST2-Geesthacht '),
            VocabItem(u'1011 ', _(u'1011 '), u'SH-KTA-Geesthacht '),
            VocabItem(u'1020 ', _(u'1020 '), u'SH-MST1-Kiel '),
            VocabItem(u'1051 ', _(u'1051 '), u'SH-KTA-Krümmel '),
            VocabItem(u'1062 ', _(u'1062 '), u'shldz1 '),
            VocabItem(u'1071 ', _(u'1071 '), u'SH-KTA-Brunsbüttel '),
            VocabItem(u'1081 ', _(u'1081 '), u'SH-KTA-Brokdorf '),
            VocabItem(u'1181 ', _(u'1181 '), u'SH-KTA-Brokdorf_SZL '),
            VocabItem(u'1551 ', _(u'1551 '), u'SH-KTA-Krümmel_SZL '),
            VocabItem(u'2002 ', _(u'2002 '), u'HH-MIN-Hamburg '),
            VocabItem(u'2010 ', _(u'2010 '), u'HH-MST1-Hamburg '),
            VocabItem(u'2020 ', _(u'2020 '), u'(HH-MST2-Hamburg) '),
            VocabItem(u'2032 ', _(u'2032 '), u'HH-LDZ-Hamburg '),
            VocabItem(u'2041 ', _(u'2041 '), u'HH-ML-Hamburg '),
            VocabItem(u'3010 ', _(u'3010 '), u'NI-MST3-Braunschweig '),
            VocabItem(u'3040 ', _(u'3040 '), u'NI-MST1-Hildesheim '),
            VocabItem(u'3050 ', _(u'3050 '), u'NI-MST6-Hannover '),
            VocabItem(u'3060 ', _(u'3060 '), u'NI-MST2-Hildesheim '),
            VocabItem(u'3070 ', _(u'3070 '), u'NI-MST7-Oldenburg '),
            VocabItem(u'3080 ', _(u'3080 '), u'NI-MST5-Oldenburg '),
            VocabItem(u'3090 ', _(u'3090 '), u'NI-MST4-Cuxhaven '),
            VocabItem(u'3102 ', _(u'3102 '), u'NI-LDZ-Hildesheim '),
            VocabItem(u'3122 ', _(u'3122 '), u'MStZ '),
            VocabItem(u'3132 ', _(u'3132 '), u'NI-MIN-Hannover '),
            VocabItem(u'3141 ', _(u'3141 '), u'NI-KTA-Lingen_KKW '),
            VocabItem(u'3151 ', _(u'3151 '), u'NI-KTA-Stade '),
            VocabItem(u'3161 ', _(u'3161 '), u'NI-KTA-Unterweser '),
            VocabItem(u'3171 ', _(u'3171 '), u'NI-KTA-Grohnde '),
            VocabItem(u'3191 ', _(u'3191 '), u'NI-KTA-Lippe-Ems '),
            VocabItem(u'3201 ', _(u'3201 '), u'NI-KTA-Gorleben '),
            VocabItem(u'3211 ', _(u'3211 '), u'NI-KTA-Konrad '),
            VocabItem(u'3221 ', _(u'3221 '), u'NI-KTA-Lingen_ANF '),
            VocabItem(u'3231 ', _(u'3231 '), u'NI-KTA-Lingen_SZL '),
            VocabItem(u'3561 ', _(u'3561 '), u'NI-KTA-Unterweser_SZL '),
            VocabItem(u'3571 ', _(u'3571 '), u'NI-KTA-Grohnde_SZL '),
            VocabItem(u'4002 ', _(u'4002 '), u'HB-MIN-Bremen '),
            VocabItem(u'4020 ', _(u'4020 '), u'HB-MST1-Bremen '),
            VocabItem(u'4032 ', _(u'4032 '), u'HB-LDZ-Bremen '),
            VocabItem(u'5010 ', _(u'5010 '), u'NW-MST3-Dortmund '),
            VocabItem(u'5020 ', _(u'5020 '), u'NW-MST1-Düsseldorf '),
            VocabItem(u'5030 ', _(u'5030 '), u'NW-MST2-Düsseldorf '),
            VocabItem(u'5050 ', _(u'5050 '), u'NW-ML-Köln '),
            VocabItem(u'5070 ', _(u'5070 '), u'NW-MST5-Münster '),
            VocabItem(u'5080 ', _(u'5080 '), u'NW-MST6-Münster_LUFA '),
            VocabItem(u'5090 ', _(u'5090 '), u'NW-MST7-Dortmund_MPA '),
            VocabItem(u'5091 ', _(u'5091 '), u'NW-KTA-Jülich_FZJ '),
            VocabItem(u'5092 ', _(u'5092 '), u'NW-KTA-Jülich_AVR '),
            VocabItem(u'5100 ', _(u'5100 '), u'NW-MST4-Detmold '),
            VocabItem(u'5112 ', _(u'5112 '), u'NW-MIN-Düsseldorf '),
            VocabItem(u'5122 ', _(u'5122 '), u'NW-LDZ-Essen '),
            VocabItem(u'5141 ', _(u'5141 '), u'NW-KTA-Würgassen '),
            VocabItem(u'5151 ', _(u'5151 '), u'NW-KTA-Hamm '),
            VocabItem(u'5161 ', _(u'5161 '), u'(NW-KTA-Kalkar) '),
            VocabItem(u'5171 ', _(u'5171 '), u'NW-KTA-Ahaus '),
            VocabItem(u'5181 ', _(u'5181 '), u'NW-KTA-Gronau '),
            VocabItem(u'6010 ', _(u'6010 '), u'HE-MST2-Kassel '),
            VocabItem(u'6020 ', _(u'6020 '), u'(HE-MST4-Wiesbaden) '),
            VocabItem(u'6040 ', _(u'6040 '), u'(HE-MST6-Gießen) '),
            VocabItem(u'6050 ', _(u'6050 '), u'(HE-MST7-Kassel) '),
            VocabItem(u'6060 ', _(u'6060 '), u'HE-MST3-Darmstadt '),
            VocabItem(u'6101 ', _(u'6101 '), u'HE-KTA-Biblis '),
            VocabItem(u'6112 ', _(u'6112 '), u'HE-LDZ-Kassel '),
            VocabItem(u'6122 ', _(u'6122 '), u'HE-MIN-Wiesbaden '),
            VocabItem(u'6501 ', _(u'6501 '), u'HE-KTA-Biblis_SZL '),
            VocabItem(u'7002 ', _(u'7002 '), u'RP-LDZ-Mainz '),
            VocabItem(u'7010 ', _(u'7010 '), u'RP-MST1-Mainz '),
            VocabItem(u'7020 ', _(u'7020 '), u'RP-MST4-Mainz '),
            VocabItem(u'7030 ', _(u'7030 '), u'RP-MST2-Speyer '),
            VocabItem(u'7040 ', _(u'7040 '), u'RP-MST5-Speyer '),
            VocabItem(u'7050 ', _(u'7050 '), u'(RP-MST3-Trier) '),
            VocabItem(u'7071 ', _(u'7071 '), u'(RP-KTA-Mainz) '),
            VocabItem(u'7081 ', _(u'7081 '), u'RP-KTA-Mülheim-Kärlich '),
            VocabItem(u'8002 ', _(u'8002 '), u'BW-MIN1-Stuttgart '),
            VocabItem(u'8010 ', _(u'8010 '), u'BW-MST1-Karlsruhe '),
            VocabItem(u'8020 ', _(u'8020 '), u'BW-MST2-Fellbach '),
            VocabItem(u'8031 ', _(u'8031 '), u'BW-ML-Stuttgart '),
            VocabItem(u'8041 ', _(u'8041 '), u'BW-KTA-Karlsruhe '),
            VocabItem(u'8050 ', _(u'8050 '), u'(BW-MST4-Karlsruhe) '),
            VocabItem(u'8061 ', _(u'8061 '), u'BW-MST5-Wangen '),
            VocabItem(u'8070 ', _(u'8070 '), u'BW-MST3-Freiburg '),
            VocabItem(u'8082 ', _(u'8082 '), u'(BW-LDZ-Karlsruhe) '),
            VocabItem(u'8083 ', _(u'8083 '), u'BW-MIN2-Stuttgart_REIAB '),
            VocabItem(u'8101 ', _(u'8101 '), u'BW-KTA-Obrigheim '),
            VocabItem(
                u'8106 ',
                _(u'8106 '),
                u'BW-ML-EggensteinLeopoldshafen_KIT '),
            VocabItem(u'8111 ', _(u'8111 '), u'BW-KTA-Neckarwestheim '),
            VocabItem(u'8121 ', _(u'8121 '), u'BW-KTA-Philippsburg '),
            VocabItem(u'8131 ', _(u'8131 '), u'BW-KTA-Heidelberg '),
            VocabItem(u'8201 ', _(u'8201 '), u'BW-MST4-Weingarten '),
            VocabItem(u'8210 ', _(u'8210 '), u'LFS BW '),
            VocabItem(u'8211 ', _(u'8211 '), u'BW-MM-CBRN '),
            VocabItem(
                u'8221 ',
                _(u'8221 '),
                u'BW-ML-EggensteinLeopoldshafen_KHG '),
            VocabItem(u'8511 ', _(u'8511 '), u'BW-KTA-Neckarwestheim_SZL '),
            VocabItem(u'8521 ', _(u'8521 '), u'BW-KTA-Philippsburg_SZL '),
            VocabItem(u'9010 ', _(u'9010 '), u'(BY-MST1-Augsburg) '),
            VocabItem(u'9011 ', _(u'9011 '), u'BY-MST7-Kulmbach '),
            VocabItem(u'9020 ', _(u'9020 '), u'(BY-MST2-Augsburg) '),
            VocabItem(u'9030 ', _(u'9030 '), u'BY-MST3-Augsburg '),
            VocabItem(u'9040 ', _(u'9040 '), u'(BY-MST6-Oberschleißheim) '),
            VocabItem(u'9051 ', _(u'9051 '), u'BY-ML-Oberschleißheim_01 '),
            VocabItem(u'9052 ', _(u'9052 '), u'BY-ML-Oberschleißheim_02 '),
            VocabItem(u'9060 ', _(u'9060 '), u'(BY-MST5-Erlangen) '),
            VocabItem(u'9070 ', _(u'9070 '), u'(BY-MST4-München) '),
            VocabItem(u'9081 ', _(u'9081 '), u'BY-ML-Nürnberg '),
            VocabItem(u'9091 ', _(u'9091 '), u'BY-MST8-Kempten '),
            VocabItem(u'9111 ', _(u'9111 '), u'BY-KTA-Garching '),
            VocabItem(u'9121 ', _(u'9121 '), u'BY-KTA-Isar '),
            VocabItem(u'9131 ', _(u'9131 '), u'BY-KTA-Grafenrheinfeld '),
            VocabItem(u'9141 ', _(u'9141 '), u'BY-KTA-Gundremmingen '),
            VocabItem(u'9151 ', _(u'9151 '), u'BY-KTA-Kahl '),
            VocabItem(u'9161 ', _(u'9161 '), u'BY-KTA-Erlangen_Siemens '),
            VocabItem(u'9162 ', _(u'9162 '), u'BY-KTA-Erlangen_Framatome '),
            VocabItem(u'9171 ', _(u'9171 '), u'BY-KTA-Karlstein_01 '),
            VocabItem(u'9181 ', _(u'9181 '), u'BY-KTA-Karlstein_02 '),
            VocabItem(u'9192 ', _(u'9192 '), u'BY-LDZ-Augsburg '),
            VocabItem(u'9212 ', _(u'9212 '), u'BY-MIN1-München '),
            VocabItem(u'9222 ', _(u'9222 '), u'BY-MIN2-München '),
            VocabItem(u'9231 ', _(u'9231 '), u'BY-ML-München '),
            VocabItem(u'9301 ', _(u'9301 '), u'BY-MST-Regensburg '),
            VocabItem(u'9521 ', _(u'9521 '), u'BY-KTA-Isar_SZL '),
            VocabItem(u'9531 ', _(u'9531 '), u'BY-KTA-Grafenrheinfeld_SZL '),
            VocabItem(u'9541 ', _(u'9541 '), u'BY-KTA-Gundremmingen_SZL '),
            VocabItem(u'10002 ', _(u'10002 '), u'SL-MIN-Saarbrücken '),
            VocabItem(u'10010 ', _(u'10010 '), u'SL-MST1-Saarbrücken '),
            VocabItem(u'10022 ', _(u'10022 '), u'10-Min '),
            VocabItem(u'10030 ', _(u'10030 '), u'SL-MST2-Saarbrücken '),
            VocabItem(u'10042 ', _(u'10042 '), u'SL-LDZ-Saarbrücken '),
            VocabItem(u'11010 ', _(u'11010 '), u'BE-MST1-Berlin '),
            VocabItem(u'11042 ', _(u'11042 '), u'BE-LDZ-Berlin '),
            VocabItem(u'11061 ', _(u'11061 '), u'BE-KTA-Berlin '),
            VocabItem(u'12002 ', _(u'12002 '), u'BB-MIN-Potsdam '),
            VocabItem(u'12010 ', _(u'12010 '), u'BB-MST1-Oranienburg '),
            VocabItem(u'12020 ', _(u'12020 '), u'BB-MST2-FrankfurtOder '),
            VocabItem(u'12032 ', _(u'12032 '), u'BB-LDZ-FrankfurtOder '),
            VocabItem(u'13002 ', _(u'13002 '), u'MV-MIN-Schwerin '),
            VocabItem(u'13010 ', _(u'13010 '), u'MV-MST1-Stralsund '),
            VocabItem(u'13020 ', _(u'13020 '), u'(MV-MST2-Schwerin) '),
            VocabItem(u'13031 ', _(u'13031 '), u'(MV-KTA-Rubenow) '),
            VocabItem(u'13032 ', _(u'13032 '), u'MV-LDZ-Stralsund '),
            VocabItem(u'13033 ', _(u'13033 '), u'MV-KTA-Lubmin '),
            VocabItem(u'14002 ', _(u'14002 '), u'SN-MIN-Dresden '),
            VocabItem(u'14010 ', _(u'14010 '), u'SN-MST1-Radebeul '),
            VocabItem(u'14020 ', _(u'14020 '), u'SN-MST2-Chemnitz '),
            VocabItem(u'14032 ', _(u'14032 '), u'SN-LDZ-Radebeul '),
            VocabItem(u'14040 ', _(u'14040 '), u'SN-ML-Radeberg '),
            VocabItem(u'14041 ', _(u'14041 '), u'SN-KTA-Rossendorf '),
            VocabItem(u'15002 ', _(u'15002 '), u'ST-MIN-Magdeburg '),
            VocabItem(u'15010 ', _(u'15010 '), u'ST-MST1-HalleSaale '),
            VocabItem(u'15020 ', _(u'15020 '), u'ST-MST2-Osterburg '),
            VocabItem(u'15032 ', _(u'15032 '), u'ST-LDZ-Magdeburg '),
            VocabItem(u'15041 ', _(u'15041 '), u'ST-KTA-Morsleben '),
            VocabItem(u'16002 ', _(u'16002 '), u'TH-MIN-Erfurt '),
            VocabItem(u'16010 ', _(u'16010 '), u'TH-MST1-Jena '),
            VocabItem(u'16020 ', _(u'16020 '), u'TH-MST2-Gera '),
            VocabItem(u'16032 ', _(u'16032 '), u'TH-LDZ-Jena '),
            VocabItem(u'17001 ', _(u'17001 '), u'BUW-München '),
            VocabItem(u'17002 ', _(u'17002 '), u'BUW-Kiel '),
            VocabItem(u'17003 ', _(u'17003 '), u'BUW-Koblenz '),
            VocabItem(u'18001 ', _(u'18001 '), u'EL-KTA-Morsleben '),
            VocabItem(u'18002 ', _(u'18002 '), u'EL-KTA-Aufsicht '),
            VocabItem(u'18003 ', _(u'18003 '), u'EL-KTA-Asse '),
            VocabItem(u'19001 ', _(u'19001 '), u'BfS-MST1-Schulung '),
            VocabItem(u'19002 ', _(u'19002 '), u'BfS-MST2-Schulung.extern '),
            VocabItem(u'20000 ', _(u'20000 '), u'BfS-ZdB '),
            VocabItem(u'20001 ', _(u'20001 '), u'(BfS-ZdB-PARK) '),
            VocabItem(u'20010 ', _(u'20010 '), u'DWD '),
            VocabItem(u'20020 ', _(u'20020 '), u'BfG '),
            VocabItem(u'20030 ', _(u'20030 '), u'BSH '),
            VocabItem(u'20040 ', _(u'20040 '), u'LST-TI-Bremerhaven '),
            VocabItem(u'20050 ', _(u'20050 '), u'MRI '),
            VocabItem(u'20060 ', _(u'20060 '), u'BfS  LSt TW... '),
            VocabItem(u'20070 ', _(u'20070 '), u'BFE '),
            VocabItem(
                u'20080 ',
                _(u'20080 '),
                u'BfS - Kontaktstelle internat. Datenaustausch ',
            ),
            VocabItem(
                u'20090 ',
                _(u'20090 '),
                u'BfS - ODL Messnetz-Zentrale '),
            VocabItem(u'20100 ', _(u'20100 '), u'PTB '),
            VocabItem(u'20110 ', _(u'20110 '), u'BfS  LSt AB '),
            VocabItem(u'20120 ', _(u'20120 '), u'BfS-Spur-Freiburg_01 '),
            VocabItem(u'30000 ', _(u'30000 '), u'Min '),
            VocabItem(u'30011 ', _(u'30011 '), u'PTB '),
            VocabItem(u'30012 ', _(u'30012 '), u'Min '),
            VocabItem(u'30021 ', _(u'30021 '), u'BfS-Berlin '),
        ]

        return SimpleVocabulary(items)


MstVocabularyFactory = MstVocabulary()


@implementer(IVocabularyFactory)
class OriginVocabulary(object):
    """
    """

    def __call__(self, context):
        items = [
            VocabItem(u'Betreiber', _(u'Betreiber'), u'Betreiber'),
            VocabItem(
                u'Unabhängige Messstelle',
                _(u'Unabhängige Messstelle'),
                u'Unabhängige Messstelle',
            ),
        ]

        return SimpleVocabulary(items)


OriginVocabularyFactory = OriginVocabulary()


@implementer(IVocabularyFactory)
class YearVocabulary(object):
    """
    """

    def __call__(self, context):
        items = []
        today = date.today()
        year = today.year
        while year > 1986:
            items.append(
                SimpleVocabulary.createTerm(
                    year, str(year), str(year)))
            year = year - 1
        #       items = [
        #              VocabItem(u'2013', _(u'2013')),
        #              VocabItem(u'2014', _(u'2014')),
        #              VocabItem(u'2015', _(u'2015')),
        #              VocabItem(u'2016', _(u'2016')),
        #              VocabItem(u'2017', _(u'2017')),
        #              VocabItem(u'2018', _(u'2018')),
        #              VocabItem(u'2019', _(u'2019')),
        #              VocabItem(u'2020', _(u'2020')),
        #        ]

        return SimpleVocabulary(items)


YearVocabularyFactory = YearVocabulary()


@implementer(IVocabularyFactory)
class NuclearInstallationVocabulary(object):
    """
    """

    def __call__(self, context):
        items = [
            VocabItem(
                u'UCHL KTA Leibstadt mit Beznau und Villigen ',
                _(u'UCHL KTA Leibstadt mit Beznau und Villigen '),
                u'UCHL KTA Leibstadt mit Beznau und Villigen ',
            ),
            VocabItem(
                u'UELA Endlager für radioaktive Abfälle Asse ',
                _(u'UELA Endlager für radioaktive Abfälle Asse '),
                u'UELA Endlager für radioaktive Abfälle Asse ',
            ),
            VocabItem(
                u'UELM Endlager für radioaktive Abfälle Morsleben (ERAM) ',
                _(u'UELM Endlager für radioaktive Abfälle Morsleben (ERAM) '),
                u'UELM Endlager für radioaktive Abfälle Morsleben (ERAM) ',
            ),
            VocabItem(
                u'UFRC KKW Cattenom ', _(
                    u'UFRC KKW Cattenom '), u'UFRC KKW Cattenom '
            ),
            VocabItem(
                u'UFRF KKW Fessenheim ',
                _(u'UFRF KKW Fessenheim '),
                u'UFRF KKW Fessenheim ',
            ),
            VocabItem(
                u'U01A Helmholtz-Zentrum Geesthacht ',
                _(u'U01A Helmholtz-Zentrum Geesthacht '),
                u'U01A Helmholtz-Zentrum Geesthacht ',
            ),
            VocabItem(
                u'U01B KKW Krümmel ', _(
                    u'U01B KKW Krümmel '), u'U01B KKW Krümmel '
            ),
            VocabItem(
                u'U01C KKW Brunsbüttel ',
                _(u'U01C KKW Brunsbüttel '),
                u'U01C KKW Brunsbüttel ',
            ),
            VocabItem(
                u'U01D KKW Brokdorf ', _(
                    u'U01D KKW Brokdorf '), u'U01D KKW Brokdorf '
            ),
            VocabItem(
                u'U01I Interimslager Krümmel ',
                _(u'U01I Interimslager Krümmel '),
                u'U01I Interimslager Krümmel ',
            ),
            VocabItem(
                u'U01K Standortzwischenlager Krümmel ',
                _(u'U01K Standortzwischenlager Krümmel '),
                u'U01K Standortzwischenlager Krümmel ',
            ),
            VocabItem(
                u'U01L Standortzwischenlager Brunsbüttel ',
                _(u'U01L Standortzwischenlager Brunsbüttel '),
                u'U01L Standortzwischenlager Brunsbüttel ',
            ),
            VocabItem(
                u'U01M Standortzwischenlager Brokdorf ',
                _(u'U01M Standortzwischenlager Brokdorf '),
                u'U01M Standortzwischenlager Brokdorf ',
            ),
            VocabItem(
                u'U03A Standortzwischenlager Grohnde ',
                _(u'U03A Standortzwischenlager Grohnde '),
                u'U03A Standortzwischenlager Grohnde ',
            ),
            VocabItem(
                u'U03B Brennelementefertigungsanl. Lingen ',
                _(u'U03B Brennelementefertigungsanl. Lingen '),
                u'U03B Brennelementefertigungsanl. Lingen ',
            ),
            VocabItem(
                u'U03C Standortzwischenlager Unterweser ',
                _(u'U03C Standortzwischenlager Unterweser '),
                u'U03C Standortzwischenlager Unterweser ',
            ),
            VocabItem(
                u'U03E KKW Emsland ', _(
                    u'U03E KKW Emsland '), u'U03E KKW Emsland '
            ),
            VocabItem(
                u'U03G KKW Grohnde ', _(
                    u'U03G KKW Grohnde '), u'U03G KKW Grohnde '
            ),
            VocabItem(
                u'U03K Endlager Konrad ',
                _(u'U03K Endlager Konrad '),
                u'U03K Endlager Konrad ',
            ),
            VocabItem(
                u'U03L KKW Lingen ',
                _(u'U03L KKW Lingen '),
                u'U03L KKW Lingen '),
            VocabItem(
                u'U03P BGZ - Betrieb Gorleben ',
                _(u'U03P BGZ - Betrieb Gorleben '),
                u'U03P BGZ - Betrieb Gorleben ',
            ),
            VocabItem(
                u'U03S KKW Stade ',
                _(u'U03S KKW Stade '),
                u'U03S KKW Stade '),
            VocabItem(
                u'U03U KKW Unterweser ',
                _(u'U03U KKW Unterweser '),
                u'U03U KKW Unterweser ',
            ),
            VocabItem(
                u'U03Z Standortzwischenlager Lingen ',
                _(u'U03Z Standortzwischenlager Lingen '),
                u'U03Z Standortzwischenlager Lingen ',
            ),
            VocabItem(
                u'U05B BGZ - Brennelement-Zwischenl. Ahaus ',
                _(u'U05B BGZ - Brennelement-Zwischenl. Ahaus '),
                u'U05B BGZ - Brennelement-Zwischenl. Ahaus ',
            ),
            VocabItem(
                u'U05F Forschungszentrum Jülich ',
                _(u'U05F Forschungszentrum Jülich '),
                u'U05F Forschungszentrum Jülich ',
            ),
            VocabItem(
                u'U05G AVR-Versuchskernkraftwerk Jülich ',
                _(u'U05G AVR-Versuchskernkraftwerk Jülich '),
                u'U05G AVR-Versuchskernkraftwerk Jülich ',
            ),
            VocabItem(
                u'U05K KKW Würgassen ',
                _(u'U05K KKW Würgassen '),
                u'U05K KKW Würgassen ',
            ),
            VocabItem(
                u'U05T Thorium-Hochtemp.reakt. Hamm-Uentrop ',
                _(u'U05T Thorium-Hochtemp.reakt. Hamm-Uentrop '),
                u'U05T Thorium-Hochtemp.reakt. Hamm-Uentrop ',
            ),
            VocabItem(
                u'U05U Urananreicherungsanlage Gronau ',
                _(u'U05U Urananreicherungsanlage Gronau '),
                u'U05U Urananreicherungsanlage Gronau ',
            ),
            VocabItem(
                u'U06B KKW Biblis und BE-Zwischenlager ',
                _(u'U06B KKW Biblis und BE-Zwischenlager '),
                u'U06B KKW Biblis und BE-Zwischenlager ',
            ),
            VocabItem(
                u'U07M KKW Mülheim-Kärlich ',
                _(u'U07M KKW Mülheim-Kärlich '),
                u'U07M KKW Mülheim-Kärlich ',
            ),
            VocabItem(
                u'U07U Uni Mainz ',
                _(u'U07U Uni Mainz '),
                u'U07U Uni Mainz '),
            VocabItem(
                u'U08H DKFZ Heidelberg ',
                _(u'U08H DKFZ Heidelberg '),
                u'U08H DKFZ Heidelberg ',
            ),
            VocabItem(
                u'U08K Karlsruher Institut für Technologie - Campus Nord (Einrichtungen am Standort) ',
                _(
                    u'U08K Karlsruher Institut für Technologie - Campus Nord (Einrichtungen am Standort) '
                ),
                u'U08K Karlsruher Institut für Technologie - Campus Nord (Einrichtungen am Standort) ',
            ),
            VocabItem(
                u'U08M Abraumhalde Menz. ',
                _(u'U08M Abraumhalde Menz. '),
                u'U08M Abraumhalde Menz. ',
            ),
            VocabItem(
                u'U08N EnKK Neckarwestheim ',
                _(u'U08N EnKK Neckarwestheim '),
                u'U08N EnKK Neckarwestheim ',
            ),
            VocabItem(
                u'U08O EnKK Obrigheim ',
                _(u'U08O EnKK Obrigheim '),
                u'U08O EnKK Obrigheim ',
            ),
            VocabItem(
                u'U08P EnKK Philippsburg ',
                _(u'U08P EnKK Philippsburg '),
                u'U08P EnKK Philippsburg ',
            ),
            VocabItem(
                u'U08W KKW Wyhl ',
                _(u'U08W KKW Wyhl '),
                u'U08W KKW Wyhl '),
            VocabItem(
                u'U09A KKW Isar 1+2 ', _(
                    u'U09A KKW Isar 1+2 '), u'U09A KKW Isar 1+2 '
            ),
            VocabItem(
                u'U09B KKW Isar1 ',
                _(u'U09B KKW Isar1 '),
                u'U09B KKW Isar1 '),
            VocabItem(
                u'U09C KKW Isar2 ',
                _(u'U09C KKW Isar2 '),
                u'U09C KKW Isar2 '),
            VocabItem(
                u'U09D KKW Grafenrheinfeld ',
                _(u'U09D KKW Grafenrheinfeld '),
                u'U09D KKW Grafenrheinfeld ',
            ),
            VocabItem(
                u'U09E KKW Gundremmingen Block B/C ',
                _(u'U09E KKW Gundremmingen Block B/C '),
                u'U09E KKW Gundremmingen Block B/C ',
            ),
            VocabItem(
                u'U09F Versuchs-AKW Kahl a.M. ',
                _(u'U09F Versuchs-AKW Kahl a.M. '),
                u'U09F Versuchs-AKW Kahl a.M. ',
            ),
            VocabItem(
                u'U09G Forschungsreaktor München ',
                _(u'U09G Forschungsreaktor München '),
                u'U09G Forschungsreaktor München ',
            ),
            VocabItem(
                u'U09H Siemens Brennelementewerk Hanau, Standort Karlstein ',
                _(u'U09H Siemens Brennelementewerk Hanau, Standort Karlstein '),
                u'U09H Siemens Brennelementewerk Hanau, Standort Karlstein ',
            ),
            VocabItem(
                u'U09I Siemens AG, Karlstein ',
                _(u'U09I Siemens AG, Karlstein '),
                u'U09I Siemens AG, Karlstein ',
            ),
            VocabItem(
                u'U09J Framatome GmbH, Forschungszentrum Erlangen-Süd (FZE) ',
                _(u'U09J Framatome GmbH, Forschungszentrum Erlangen-Süd (FZE) '),
                u'U09J Framatome GmbH, Forschungszentrum Erlangen-Süd (FZE) ',
            ),
            VocabItem(
                u'U09K Forschungsneutronenquelle Heinz Maier-Leibnitz ',
                _(u'U09K Forschungsneutronenquelle Heinz Maier-Leibnitz '),
                u'U09K Forschungsneutronenquelle Heinz Maier-Leibnitz ',
            ),
            VocabItem(
                u'U11B Experimentierreakt. II Berlin ',
                _(u'U11B Experimentierreakt. II Berlin '),
                u'U09K Forschungsneutronenquelle Heinz Maier-Leibnitz ',
            ),
            VocabItem(
                u'U12R KKW Rheinsberg ',
                _(u'U12R KKW Rheinsberg '),
                u'U12R KKW Rheinsberg ',
            ),
            VocabItem(
                u'U13A KKW Lubmin/Greifswald ',
                _(u'U13A KKW Lubmin/Greifswald '),
                u'U13A KKW Lubmin/Greifswald ',
            ),
            VocabItem(
                u'U13B Zwischenlager Nord ',
                _(u'U13B Zwischenlager Nord '),
                u'U13B Zwischenlager Nord ',
            ),
            VocabItem(
                u'U14R Forschungszentrum Rossendorf ',
                _(u'U14R Forschungszentrum Rossendorf '),
                u'U14R Forschungszentrum Rossendorf ',
            ),
            VocabItem(
                u'U15M nicht benutzen, jetzt UELM, Endlager für radioaktive Abfälle Morsleben (ERAM) ',
                _(
                    u'U15M nicht benutzen, jetzt UELM, Endlager für radioaktive Abfälle Morsleben (ERAM) '
                ),
                u'U15M nicht benutzen, jetzt UELM, Endlager für radioaktive Abfälle Morsleben (ERAM) ',
            ),
        ]

        return SimpleVocabulary(items)


NuclearInstallationVocabularyFactory = NuclearInstallationVocabulary()


allow_module("docpool.rei.vocabularies")
