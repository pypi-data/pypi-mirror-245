from bson.objectid import ObjectId
# from fastapi import Request

from promptengineers.core.interfaces.controllers import IController
from promptengineers.core.interfaces.repos import IUserRepo
from promptengineers.repos.user import UserRepo
from promptengineers.mongo.service import MongoService

class HistoryController(IController):
	def __init__(
		self, 
		# request: Request = None, 
		request = None,
		user_repo: IUserRepo = None, 
		db_name: str = None,
		col_name: str = None
	):
		self.request = request
		self.user_id = getattr(request.state, "user_id", None)
		self.user_repo = user_repo or UserRepo()
		self.history_service = MongoService(
			host=self.user_repo.find_token(self.user_id, 'MONGO_CONNECTION'),
			db=db_name or self.user_repo.find_token(self.user_id, 'MONGO_DB_NAME'),
			collection=col_name or 'history'
		)

	##############################################################
	### Create Chat History
	##############################################################
	async def index(self, page: int = 1, limit: int = 10):
		result = await self.history_service.list_docs(
			{'user_id': ObjectId(self.user_id)},
			limit,
			page
		)
		return result

	##############################################################
	### Create Chat History
	##############################################################
	async def create(self):
		body = await self.request.json()
		body['user_id'] = ObjectId(self.user_id)
		if body.get('setting', False):
			body['setting'] = ObjectId(body['setting'])
		result = await self.history_service.create(dict(body))
		return result

	##############################################################
	### Update Chat History
	##############################################################
	async def show(self, id: str):
		result = await self.history_service.read_one(
			{'_id': ObjectId(id), 'user_id': ObjectId(self.user_id)}
		)
		return result


	##############################################################
	### Update Chat History
	##############################################################
	async def update(self, id: str, body: any):
		body = await self.request.json()
		if body.get('setting', False):
			body['setting'] = ObjectId(body['setting'])
		result = await self.history_service.update_one(
			{'_id': ObjectId(id), 'user_id': ObjectId(self.user_id)},
			dict(body)
		)
		return result

	##############################################################
	### Delete Chat History
	##############################################################
	async def delete(self, id: str):
		result = await self.history_service.delete_one(
			{'_id': ObjectId(id), 'user_id': ObjectId(self.user_id)}
		)
		return result
