# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 10:46
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : requestConfig.py
from ultipa.structs.Retry import Retry


class RequestConfig:

	def __init__(self, graphName: str = '', timeout: int = 3600, retry: Retry = Retry(),
				 stream: bool = False, host: str = None, useMaster: bool = False, threadNum: int = None,
				 timeZone: str = None, timeZoneOffset: any = None):
		self.graphName = graphName
		self.timeoutWithSeconds = timeout
		self.retry = retry
		self.stream = stream
		self.useHost = host
		self.useMaster = useMaster
		self.threadNum = threadNum
		self.timeZone = timeZone
		self.timeZoneOffset = timeZoneOffset

