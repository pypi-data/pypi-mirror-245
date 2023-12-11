# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 16:39
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : ResultType.py
from ultipa.proto import ultipa_pb2
from ultipa.structs.PropertyType import PropertyType


class ResultType:
	RESULT_TYPE_UNSET = ultipa_pb2.RESULT_TYPE_UNSET
	RESULT_TYPE_PATH = ultipa_pb2.RESULT_TYPE_PATH
	RESULT_TYPE_NODE = ultipa_pb2.RESULT_TYPE_NODE
	RESULT_TYPE_EDGE = ultipa_pb2.RESULT_TYPE_EDGE
	RESULT_TYPE_ATTR = ultipa_pb2.RESULT_TYPE_ATTR
	# RESULT_TYPE_ARRAY = ultipa_pb2.RESULT_TYPE_ARRAY
	RESULT_TYPE_TABLE = ultipa_pb2.RESULT_TYPE_TABLE
	RESULT_TYPE_ExplainPlan = "ExplainPlan"

	@staticmethod
	def getTypeStr(type):
		if type == ResultType.RESULT_TYPE_PATH:
			return 'PATH'
		elif type == ResultType.RESULT_TYPE_NODE:
			return 'NODE'
		elif type == ResultType.RESULT_TYPE_EDGE:
			return "EDGE"
		elif type == ResultType.RESULT_TYPE_ATTR:
			return "ATTR"
		elif type == PropertyType.PROPERTY_LIST:
			return "LIST"
		elif type == ResultType.RESULT_TYPE_TABLE:
			return "TABLE"
		elif type == ResultType.RESULT_TYPE_UNSET:
			return "UNSET"
		elif type == ResultType.RESULT_TYPE_ExplainPlan:
			return "EXPLAINPLAN"
		else:
			return type