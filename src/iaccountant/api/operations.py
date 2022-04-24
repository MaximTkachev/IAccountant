from fastapi import APIRouter, Depends
from typing import List, Optional

from iaccountant.models.operations import OperationKind
from iaccountant.services.auth import get_current_user
from iaccountant.services.operations import OperationsService
from iaccountant.models.operations import Operation
from iaccountant.models.auth import User
from iaccountant.models.operations import OperationCreate
from iaccountant.api.files import router as files_router

from iaccountant.tables import Operation as op

router = APIRouter(
    prefix='/operations',
    tags=['Operations']
)
router.include_router(files_router)


@router.get('/', response_model=List[Operation])
def get_all_operations_of_current_user(
        kind: Optional[OperationKind] = None,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends()
):
    return service.get_all_operations_of_current_user(
        user_id=user.id, kind=kind
    )


@router.post('/', response_model=Operation)
def create_operation(
        operation_data: OperationCreate,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends()
):
    return service.create(
        user_id=user.id, operation_data=operation_data
    )


@router.post('/{operation_id}', response_model=Operation)
def get_operation_by_id(
        operation_id: int,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends()
):
    return service.get_operation_by_id(operation_id=operation_id, author_id=user.id)
