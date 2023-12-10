from typing import List
import traceback
import ujson

from fastapi import (APIRouter, Depends, Request, Form, status,
                    Response, UploadFile, File, HTTPException)

from promptengineers.exceptions import ValidationException
from promptengineers.models.request import RequestDataLoader, RequestMultiLoader
from promptengineers.models.response import (ResponseFileLoader, ResponseCreateVectorStore,
									ResponseListPineconeVectorStores)
from promptengineers.controllers import VectorSearchController, AuthController
from promptengineers.utils import logger

TAG = "Retrieval"
router = APIRouter()
auth_controller = AuthController()

def get_controller(request: Request) -> VectorSearchController:
	return VectorSearchController(request=request)

#################################################
# Create vectorstore from files
#################################################
@router.post(
	"/vectorstores",
	response_model=ResponseCreateVectorStore,
	tags=[TAG]
)
async def create_vectorstore(
	body: RequestDataLoader,
	controller: VectorSearchController = Depends(get_controller),
):
	"""File Loader endpoint."""
	logger.debug('[POST /vectorstores] Body: %s', str(body))
	try:
		await controller.create_multi_loader_vectorstore(body)

		## Format Response
		data = ujson.dumps({
			"message": 'Vectorstore Created!',
			'vectorstore': body.index_name,
		})
		return Response(
			content=data,
			media_type='application/json',
			status_code=201
		)
	except ValidationException as err:
		logger.warning("ValidationException: %s", err)
		raise HTTPException(
			status_code=400,
			detail=str(err)
		) from err
	except HTTPException as err:
		logger.error("HTTPException: %s", err.detail, stack_info=True)
		raise
	except Exception as err:
		tb = traceback.format_exc()
		logger.error("[routes.vectorstores.create_vectorstore]: %s\n%s", err, tb)
		raise HTTPException(
			status_code=500,
			detail=f"An unexpected error occurred. {str(err)}"
		) from err

#################################################
# Create vectorstore from files
#################################################
@router.post(
	"/vectorstores/file",
	response_model=ResponseFileLoader,
	tags=[TAG]
)
async def create_vectorstore_from_file(
	index_name: str = Form(...),
	files: List[UploadFile] = File(...),
	controller: VectorSearchController = Depends(get_controller),
):
	"""File Loader endpoint."""
	try:
		await controller.create_vectorstore_from_files(
			index_name,
			files
		)

		## Format Response
		data = ujson.dumps({
			"message": 'Vectorstore Created!',
			'vectorstore': index_name,
		})
		return Response(
			content=data,
			media_type='application/json',
			status_code=201
		)
	except ValidationException as err:
		logger.warning("ValidationException: %s", err)
		raise HTTPException(
			status_code=400,
			detail=str(err)
		) from err
	except HTTPException as err:
		logger.error("HTTPException: %s", err.detail, stack_info=True)
		raise
	except Exception as err:
		logger.error("%s", err, stack_info=True)
		raise HTTPException(
			status_code=500,
			detail=f"An unexpected error occurred. {str(err)}"
		) from err


#################################################
# Create vectorstore
#################################################
@router.post(
	"/vectorstores/multi",
	response_model=ResponseCreateVectorStore,
	tags=[TAG],
	# include_in_schema=False # TODO: Needs some work
)
async def create_vectorstore_from_multiple_sources(
	request: Request,
	body: RequestMultiLoader,
	controller: VectorSearchController = Depends(get_controller),
):
	# Get Body
	body = await request.json()
	logger.debug('[POST /vectorstores/multi] Body: %s', str(body))

	try:
		await controller.create_multi_loader_vectorstore(body)
		## Format Response
		data = ujson.dumps({
			'message': 'Vectorstore Created!',
			'data': body
		})
		return Response(
			content=data,
			media_type='application/json',
			status_code=201
		)
	except ValidationException as err:
		logger.warning("ValidationException: %s", err)
		raise HTTPException(
			status_code=400,
			detail=str(err)
		) from err
	except HTTPException as err:
		logger.error("%s", err.detail, stack_info=True)
		raise
	except Exception as err:
		logger.error("%s", err, stack_info=True)
		raise HTTPException(
			status_code=500,
			detail=f"An unexpected error occurred. {str(err)}"
		) from err


######################################
# Retrieve Vector Stores
######################################
@router.get(
	"/vectorstores/pinecone",
	response_model=ResponseListPineconeVectorStores,
	tags=[TAG]
)
async def list_pinecone_vectorstores(controller: VectorSearchController = Depends(get_controller)):
	try:
		result = controller.retrieve_pinecone_vectorstores()
		# Format Response
		data = ujson.dumps({
			**result
		})
		logger.debug("List Pinecone Vectorstores: %s", data)
		return Response(
			content=data,
			media_type='application/json',
			status_code=200
		)
	except ValidationException as err:
		logger.warning("ValidationException: %s", err)
		raise HTTPException(
			status_code=400,
			detail=str(err)
		) from err
	except HTTPException as err:
		logger.error("HTTPException: %s", err.detail)
		raise
	except Exception as err:
		tb = traceback.format_exc()
		logger.error("[routes.retrieval.list_pinecone_vectorstores]: %s\n%s", err, tb)
		raise HTTPException(
			status_code=500,
			detail=f"An unexpected error occurred. {str(err)}"
		) from err

######################################
# Delete Vector Store
######################################
@router.delete(
	"/vectorstores/pinecone",
	status_code=status.HTTP_204_NO_CONTENT,
	tags=[TAG]
)
async def delete_pinecone_vectorstore(
	prefix: str or None = None,
	controller: VectorSearchController = Depends(get_controller)
):
	try:
		controller.delete_pinecone_vectorstore(prefix)
		return Response(status_code=204)
	except ValidationException as err:
		logger.warning("ValidationException: %s", err)
		raise HTTPException(
			status_code=400,
			detail=str(err)
		) from err
	except Exception as err:
		raise HTTPException(status_code=404, detail=str(err)) from err

######################################
# Retrieve Vector Stores
######################################
@router.get(
	"/vectorstores/redis",
	response_model=ResponseListPineconeVectorStores,
	tags=[TAG]
)
async def list_redis_vectorstores(controller: VectorSearchController = Depends(get_controller)):
	try:
		result = controller.retrieve_redis_vectorstores()
		# Format Response
		data = ujson.dumps({
			**result
		})
		logger.debug("List Redis Vectorstores: %s", data)
		return Response(
			content=data,
			media_type='application/json',
			status_code=200
		)
	except ValidationException as err:
		logger.warning("ValidationException: %s", err)
		raise HTTPException(
			status_code=400,
			detail=str(err)
		) from err
	except HTTPException as err:
		logger.error("HTTPException: %s", err.detail)
		raise
	except Exception as err:
		tb = traceback.format_exc()
		logger.error("[routes.vectorstores.list_redis_vectorstores]: %s\n%s", err, tb)
		raise HTTPException(
			status_code=500,
			detail=f"An unexpected error occurred. {str(err)}"
		) from err

######################################
# Delete Vector Store
######################################
@router.delete(
	"/vectorstores/redis",
	status_code=status.HTTP_204_NO_CONTENT,
	tags=[TAG]
)
async def delete_redis_vectorstore(
	prefix: str or None = None,
	controller: VectorSearchController = Depends(get_controller)
):
	try:
		controller.delete_redis_vectorstore(prefix)
		return Response(status_code=204)
	except ValidationException as err:
		logger.warning("ValidationException: %s", err)
		raise HTTPException(
			status_code=400,
			detail=str(err)
		) from err
	except Exception as err:
		raise HTTPException(status_code=404, detail=str(err)) from err