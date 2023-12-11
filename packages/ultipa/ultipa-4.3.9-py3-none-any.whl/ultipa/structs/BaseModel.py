# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 10:29
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : BaseModel.py
import json
from typing import Dict


class BaseModel:
	def toJSON(self, pretty=False):
		try:
			if pretty:
				return json.dumps(self, default=lambda o: o.__dict__,
								  sort_keys=True, indent=4, ensure_ascii=False)
			else:

				return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, ensure_ascii=False)

		except Exception as e:
			return self

	def toDict(self):
		return json.loads(self.toJSON())

	def __str__(self):
		return str(self.__dict__)
