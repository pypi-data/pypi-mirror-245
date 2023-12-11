"""Routes to get chat history"""
import json
import traceback

from fastapi import APIRouter, HTTPException, Response, Depends, Request, status
from promptengineers.fastapi.controllers import HistoryController
from promptengineers.models.request import ReqBodyHistory
from promptengineers.models.response import (ResponseHistoryShow, ResponseHistoryIndex, 
                                            ResponseCreate, ResponseUpdate)
from promptengineers.mongo.utils import JSONEncoder
from promptengineers.core.utils import logger

router = APIRouter()
TAG = "Chat"

def get_controller(request: Request) -> HistoryController:
	return HistoryController(request=request)

#################################################
# List Chat Histories
#################################################
@router.get(
	"/chat/history",
	tags=[TAG],
	response_model=ResponseHistoryIndex
)
async def list_chat_histories(
	page: int = 1,
	limit: int = 50,
	controller: HistoryController = Depends(get_controller),
):
	"""List histories"""
	try:
		result = await controller.index(page, limit)
		# Format Response
		data = json.dumps({
			'histories': result
		}, cls=JSONEncoder)
		return Response(
			content=data,
			media_type='application/json',
			status_code=200
		)
	except HTTPException as err:
		logger.error(err.detail)
		raise
	except BaseException as err:
		tb = traceback.format_exc()
		logger.error("[list_chat_histories]: %s\n%s", err, tb)
		raise HTTPException(
			status_code=500,
			detail=f"An unexpected error occurred. {str(err)}"
		) from err

#################################################
# Create Chat History
#################################################
@router.post(
	"/chat/history",
	tags=[TAG],
	response_model=ResponseCreate
)
async def create_chat_history(
	body: ReqBodyHistory,
	controller: HistoryController = Depends(get_controller)
):
	"""Create history"""
	try:
		result = await controller.create()
		# Format Response
		data = json.dumps({
			**result
		})
		return Response(
			content=data,
			media_type='application/json',
			status_code=200
		)
	except HTTPException as err:
		logger.error(err.detail)
		raise
	except BaseException as err:
		tb = traceback.format_exc()
		logger.error("[create_chat_history]: %s\n%s", err, tb)
		raise HTTPException(
			status_code=500,
			detail=f"An unexpected error occurred. {str(err)}"
		) from err

#################################################
# Show Chat History
#################################################
@router.get(
	"/chat/history/{history_id}",
	tags=[TAG],
	response_model=ResponseHistoryShow,
)
async def show_chat_history(
    history_id: str,
    controller: HistoryController = Depends(get_controller),
):
	"""Show history"""
	try:
		result = await controller.show(history_id)

		# Format Response
		data = json.dumps({
			**result
		}, cls=JSONEncoder)
		return Response(
			content=data,
			media_type='application/json',
			status_code=200
		)
	except HTTPException as err:
		logger.error("%s", err.detail)
		raise
	except BaseException as err:
		tb = traceback.format_exc()
		logger.error("[show_chat_history]: %s\n%s", err, tb)
		raise HTTPException(
			status_code=500,
			detail=f"An unexpected error occurred. {str(err)}"
		) from err

#################################################
# Update Chat History
#################################################
@router.put(
	"/chat/history/{history_id}",
	tags=[TAG],
	response_model=ResponseUpdate,
)
async def update_chat_history(
	history_id: str,
	body: ReqBodyHistory,
	controller: HistoryController = Depends(get_controller),
):
	"""Update history"""
	try:
		await controller.update(history_id, body)
		data = json.dumps({
			'message': f'History [{history_id}] updated successfully.'
		})
		# Format Response
		return Response(status_code=200, content=data)
	except HTTPException as err:
		logger.error("%s", err.detail)
		raise
	except BaseException as err:
		tb = traceback.format_exc()
		logger.error("[update_chat_history]: %s\n%s", err, tb)
		raise HTTPException(
			status_code=500,
			detail=f"An unexpected error occurred. {str(err)}"
		) from err

#################################################
# Delete Chat History
#################################################
@router.delete(
	"/chat/history/{history_id}",
	tags=[TAG],
	status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_chat_history(
	history_id: str,
	controller: HistoryController = Depends(get_controller),
):
	"""Deletes history"""
	try:
		await controller.delete(history_id)
		# Format Response
		return Response(status_code=204)
	except BaseException as err:
		tb = traceback.format_exc()
		logger.error("[delete_chat_history]: %s\n%s", err, tb)
		raise HTTPException(status_code=404, detail=str(err)) from err