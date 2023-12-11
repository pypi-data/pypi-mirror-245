# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 10:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Graph.py
from ultipa.structs.BaseModel import BaseModel

class Graph(BaseModel):
	id: str
	name: str
	totalNodes: str
	totalEdges: str
	description: str
	status: str

	def __init__(self, name: str, description: str = None):
		self.name = name
		self.description = description


