# -*- coding: utf-8 -*-
class ObjectDuplicateException(Exception):
    def __init__(self, dubletten, formular):
        self.dubletten = dubletten
        self.formular = formular