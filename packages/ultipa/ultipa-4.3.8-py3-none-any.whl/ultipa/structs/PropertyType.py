# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 16:40
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : PropertyType.py
from ultipa.proto import ultipa_pb2

class PropertyTypeStr:
	PROPERTY_INT = 'int32'
	PROPERTY_STRING = 'string'
	PROPERTY_FLOAT = 'float'
	PROPERTY_DOUBLE = 'double'
	PROPERTY_UINT32 = 'uint32'
	PROPERTY_INT64 = 'int64'
	PROPERTY_UINT64 = 'uint64'
	PROPERTY_DATETIME = 'datetime'
	PROPERTY_TIMESTAMP = 'timestamp'
	PROPERTY_TEXT = 'text'
	PROPERTY_UNSET = "unset"
	PROPERTY_POINT = "point"
	PROPERTY_LIST = "list"
	PROPERTY_SET = "set"
	PROPERTY_MAP = "map"
	PROPERTY_BLOB= "blob"
	@staticmethod
	def PROPERTY_DECIMAL(accuracy,scale):
		return f"decimal({accuracy},{scale})"

class PropertyType:
	PROPERTY_UNSET = ultipa_pb2.UNSET
	PROPERTY_INT32 = ultipa_pb2.INT32
	PROPERTY_STRING = ultipa_pb2.STRING
	PROPERTY_FLOAT = ultipa_pb2.FLOAT
	PROPERTY_DOUBLE = ultipa_pb2.DOUBLE
	PROPERTY_UINT32 = ultipa_pb2.UINT32
	PROPERTY_INT64 = ultipa_pb2.INT64
	PROPERTY_UINT64 = ultipa_pb2.UINT64
	PROPERTY_DATETIME = ultipa_pb2.DATETIME
	PROPERTY_TIMESTAMP = ultipa_pb2.TIMESTAMP
	PROPERTY_TEXT = ultipa_pb2.TEXT
	PROPERTY_BLOB = ultipa_pb2.BLOB
	PROPERTY_POINT = ultipa_pb2.POINT
	PROPERTY_DECIMAL = ultipa_pb2.DECIMAL
	PROPERTY_LIST = ultipa_pb2.LIST
	PROPERTY_SET = ultipa_pb2.SET
	PROPERTY_MAP = ultipa_pb2.MAP
	PROPERTY_NULL = ultipa_pb2.NULL_
	PROPERTY_UUID = -1
	PROPERTY_ID = -2
	PROPERTY_FROM = -3
	PROPERTY_FROM_UUID = -4
	PROPERTY_TO = -5
	PROPERTY_TO_UUID = -6
	PROPERTY_IGNORE = -7