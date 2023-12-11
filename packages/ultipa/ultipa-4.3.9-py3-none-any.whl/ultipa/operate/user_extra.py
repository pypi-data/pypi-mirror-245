from ultipa.operate.base_extra import BaseExtra
from ultipa.utils import UQLMAKER, CommandList
from ultipa.types import ULTIPA_REQUEST, ULTIPA_RESPONSE
from ultipa.utils.errors import ParameterException
from ultipa.utils.format import FormatType
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.configuration.RequestConfig import RequestConfig

JSONSTRING_KEYS = ["graphPrivileges", "systemPrivileges", "policies", "policy", "privilege"]
formatdata = ['graph_privileges']


class UserExtra(BaseExtra):

	def GRPATH_PRIVILEGES_DATA_FORMAT(self, obj):
		if isinstance(obj.get('graph_privileges'), list):
			resr = FormatType.graphPrivileges(obj.get('graph_privileges'))
			return resr
		else:
			return '[]'

	def showUser(self,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListUser:
		'''
		:EXP: conn.listUser()
		:return:
		'''
		uqlMaker = UQLMAKER(command=CommandList.showUser, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(jsonKeys=JSONSTRING_KEYS, dataFormat=formatdata))
		return res

	def getUser(self, username:str,
				requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseUser:
		'''
		:EXP: conn.getUser(ULTIPA_REQUEST.GetUser(username='Test'))
		:param request: ULTIPA_REQUEST
		:return:
		'''
		uqlMaker = UQLMAKER(command=CommandList.getUser, commonParams=requestConfig)
		uqlMaker.setCommandParams(username)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(jsonKeys=JSONSTRING_KEYS, dataFormat=formatdata))
		if isinstance(res.data, list) and len(res.data) > 0:
			res.data = res.data[0]
		return res

	def getSelfInfo(self,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		:EXP: conn.getUser(ULTIPA_REQUEST.GetUser(username='Test'))
		:param request: ULTIPA_REQUEST
		:return:
		'''
		uqlMaker = UQLMAKER(command=CommandList.getSelfInfo, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(jsonKeys=JSONSTRING_KEYS, dataFormat=formatdata))

		return res

	def createUser(self, request: ULTIPA_REQUEST.CreateUser,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		:EXP: conn.createUser(ULTIPA_REQUEST.CreateUser(username="Test", password="Test"))
		:param request: ULTIPA_REQUEST
		:return:
		'''
		uqlMaker = UQLMAKER(command=CommandList.createUser, commonParams=requestConfig)
		params = []
		if request.username:
			params.append(request.username)
		else:
			raise ParameterException(err='username is a required parameter')

		if request.password:
			params.append(request.password)
		else:
			raise ParameterException(err='password is a required parameter')

		if request.graph_privileges:
			params.append(request.graph_privileges)
		else:
			params.append({})

		if request.system_privileges:
			params.append(request.system_privileges)
		else:
			params.append([])

		if request.policies:
			params.append(request.policies)
		else:
			params.append([])

		uqlMaker.setCommandParams(params)
		return self.uqlSingle(uqlMaker=uqlMaker)

	def dropUser(self, username:str,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		:EXP: conn.deleteUser(ULTIPA_REQUEST.DeleteUser(username=username))
		:param request: ULTIPA_REQUEST
		:return:
		'''
		uqlMaker = UQLMAKER(command=CommandList.dropUser, commonParams=requestConfig)
		uqlMaker.setCommandParams(username)
		return self.uqlSingle(uqlMaker=uqlMaker)

	def alterUser(self, request: ULTIPA_REQUEST.AlterUser,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		:EXP: conn.updateUser(ULTIPA_REQUEST.UpdateUser(username='Test',password='test',privileges=['DELETE','UPDATE'],policies=['ROOT']))
		:param request: ULTIPA_REQUEST
		:return:
		'''
		uqlMaker = UQLMAKER(command=CommandList.alterUser, commonParams=requestConfig)
		if request.username:
			uqlMaker.setCommandParams(request.username)
		else:
			raise ParameterException(err='username is a required parameter')

		paramsDict = {}
		if request.password:
			paramsDict.setdefault('password', request.password)

		if request.graph_privileges:
			paramsDict.setdefault('graph_privileges', request.graph_privileges)

		if request.system_privileges:
			paramsDict.setdefault('system_privileges', request.system_privileges)

		if request.policies:
			paramsDict.setdefault('policies', request.policies)

		uqlMaker.addParam('set', paramsDict)
		return self.uqlSingle(uqlMaker=uqlMaker)
