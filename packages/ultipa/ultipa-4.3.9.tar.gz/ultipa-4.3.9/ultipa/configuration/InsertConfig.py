# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 18:14
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : InsertConfig.py
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.structs.InsertType import InsertType
from ultipa.structs.Retry import Retry


class InsertConfig(RequestConfig):
	def __init__(self, insertType: InsertType, graphName: str = '', timeout: int = 3600,
				 retry: Retry = Retry(), stream: bool = False, useHost: str = None, useMaster: bool = False,
				 CreateNodeIfNotExist: bool = False, timeZone=None, timeZoneOffset=None, **kwargs):
		super().__init__(graphName, timeout, retry, stream, useHost, useMaster, timeZone=timeZone,
						 timeZoneOffset=timeZoneOffset)
		self.insertType = insertType
		if kwargs.get("silent") is not None:
			self.silent = kwargs.get("silent")
		else:
			self.silent = True
		if kwargs.get("batch") is not None:
			self.batch = kwargs.get("batch")
		if kwargs.get("n") is not None:
			self.n = kwargs.get("n")
		if kwargs.get("timeoutWithSeconds") is not None:
			self.timeoutWithSeconds = kwargs.get("timeoutWithSeconds")
		self.createNodeIfNotExist = CreateNodeIfNotExist
