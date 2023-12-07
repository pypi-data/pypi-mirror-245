# -*- coding: utf-8 -*-


# 经营体检
class DiagnosisService:

    __client = None

    def __init__(self, client):
        self.__client = client

