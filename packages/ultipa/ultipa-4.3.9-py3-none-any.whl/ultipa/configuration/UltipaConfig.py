# -*- coding: utf-8 -*-
# @Time    : 2023/8/10 18:25
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : UltipaConfig.py
from typing import List

from ultipa.utils.logger import LoggerConfig


class UltipaConfig:
	hosts: List[str] = []
	defaultGraph: str = 'default'
	timeoutWithSeconds: int = 3600
	responseWithRequestInfo: bool = False
	# 读一致性,如果为False 负载取节点执行
	consistency: bool = False
	uqlLoggerConfig: LoggerConfig = None
	heartBeat: int = 10
	maxRecvSize: int
	Debug: bool = False
	timeZone = None
	timeZoneOffset = None

	def __init__(self, hosts=None, username=None, password=None, crtFilePath=None, defaultGraph: str = defaultGraph,
				 timeout: int = timeoutWithSeconds, responseWithRequestInfo: bool = responseWithRequestInfo,
				 consistency: bool = consistency, heartBeat: int = 10, maxRecvSize: int = -1,
				 uqlLoggerConfig: LoggerConfig = uqlLoggerConfig, debug: bool = False, timeZone=None,
				 timeZoneOffset=None, **kwargs):
		if hosts is None:
			hosts = []
		self.hosts = hosts
		self.username = username
		self.password = password
		self.crtFilePath = crtFilePath
		self.defaultGraph = defaultGraph
		self.timeoutWithSeconds = timeout
		self.responseWithRequestInfo = responseWithRequestInfo
		self.consistency = consistency
		self.uqlLoggerConfig = uqlLoggerConfig
		self.heartBeat = heartBeat
		self.maxRecvSize = maxRecvSize
		self.Debug = debug
		self.timeZone = timeZone
		self.timeZoneOffset = timeZoneOffset
		if kwargs.get("timeoutWithSeconds") is not None:
			self.timeoutWithSeconds = kwargs.get("timeoutWithSeconds")

	def setDefaultGraphName(self, graph: str):
		self.defaultGraph = graph