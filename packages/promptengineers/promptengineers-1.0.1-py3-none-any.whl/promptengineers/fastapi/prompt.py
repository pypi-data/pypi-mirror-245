"""Routes to get chat history"""
import json
import traceback

from fastapi import APIRouter, HTTPException, Response, Depends, Request, status
from promptengineers.fastapi.controllers import PromptController
from promptengineers.models.request import ReqBodyPromptSystem
from promptengineers.models.response import ResponsePromptSystemList, ResponsePromptSystem
from promptengineers.mongo.utils import JSONEncoder
from promptengineers.core.utils import logger

router = APIRouter()
TAG = "Prompt"

def get_controller(request: Request) -> PromptController:
	return PromptController(request=request)

#################################################
# List Chat Histories
#################################################
@router.get(
	"/prompt/system",
	tags=[TAG],
	response_model=ResponsePromptSystemList
)
async def index(
	page: int = 1,
	limit: int = 50,
	controller: PromptController = Depends(get_controller),
):
	"""List resources"""
	try:
		result = await controller.index(page, limit)
		# Format Response
		data = json.dumps({
			'prompts': result,
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
	"/prompt/system",
	tags=[TAG],
	response_model=ResponsePromptSystem
)
async def create(
	body: ReqBodyPromptSystem,
	controller: PromptController = Depends(get_controller)
):
	"""Creates resource"""
	try:
		result = await controller.create(body)
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
	"/prompt/system/{prompt_id}",
	tags=[TAG],
	response_model=ResponsePromptSystem,
)
async def show(
    prompt_id: str,
    controller: PromptController = Depends(get_controller),
):
	"""Retrieve resource"""
	try:
		result = await controller.show(prompt_id)

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
	"/prompt/system/{prompt_id}",
	tags=[TAG],
	response_model=ResponsePromptSystem,
)
async def update(
	prompt_id: str,
	body: ReqBodyPromptSystem,
	controller: PromptController = Depends(get_controller),
):
	"""Update resource"""
	try:
		await controller.update(prompt_id, body)
		data = json.dumps({
			'message': 'Chat history updated successfully.'
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
	"/prompt/system/{prompt_id}",
	tags=[TAG],
	status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
	prompt_id: str,
	controller: PromptController = Depends(get_controller),
):
	"""Delete Resource"""
	try:
		await controller.delete(prompt_id)
		# Format Response
		return Response(status_code=204)
	except BaseException as err:
		tb = traceback.format_exc()
		logger.error("[delete_chat_history]: %s\n%s", err, tb)
		raise HTTPException(status_code=404, detail=str(err)) from err