from datetime import datetime
from docpool.dbaccess.interfaces import Idbadmin
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility

import time


def getTool():
    return getUtility(Idbadmin)


def portalMessage(self, msg, type='info'):
    ptool = getToolByName(self, 'plone_utils')
    ptool.addPortalMessage(msg, type)


def dtFromString(date):
    try:
        return datetime(*(time.strptime(date, "%d.%m.%Y %H:%M:%S")[0:6]))
    except BaseException:
        pass
    try:
        return datetime(*(time.strptime(date, "%d.%m.%Y %H:%M")[0:6]))
    except BaseException:
        pass
    try:
        return datetime(*(time.strptime(date, "%d.%m.%Y")[0:6]))
    except BaseException:
        pass
    return None


def stringFromDT(dt):
    """expects DateTime"""
    return "%02d.%02d.%04d %02d:%02d:%02d" % (
        dt.day(),
        dt.month(),
        dt.year(),
        dt.hour(),
        dt.minute(),
        dt.second(),
    )


def stringFromDatetime(dt, long=True):
    """
    expects datetime
    """
    if int:
        return "%02d.%02d.%04d %02d:%02d:%02d" % (
            dt.day,
            dt.month,
            dt.year,
            dt.hour,
            dt.minute,
            dt.second,
        )
    else:
        return "%02d.%02d.%04d" % (dt.day, dt.month, dt.year)


def unicode_csv_reader(unicode_csv_data, delimiter, fieldnames):
    import csv

    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.DictReader(
        utf_8_encoder(unicode_csv_data), delimiter=delimiter, fieldnames=fieldnames
    )
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        res = {}
        for field in row.keys():
            try:
                res[field] = str(row[field], 'utf-8')
            except BaseException:
                res[field] = row[field]
            if row[field] == '0':
                res[field] = False
            elif row[field] == '1':
                res[field] = True
        yield res


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.decode('latin-1').encode('utf-8')
