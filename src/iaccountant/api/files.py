from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from fastapi.responses import FileResponse

from iaccountant.models.auth import User
from iaccountant.services.auth import get_current_user
from iaccountant.services.files import FileService
from iaccountant.services.operations import OperationsService
from iaccountant import tables

router = APIRouter(
    prefix='/{operation_id}/file',
    tags=['Files']
)


def _check_authorization(
        operation_id: int,
        user: User,
        service: OperationsService
) -> tables.Operation:
    operation = service.get_operation_by_id(
        operation_id=operation_id,
        author_id=user.id
    )  # проверка на то, существует ли операция с таким id и имеет
    if not operation:  # ли пользователь доступ к ней
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Операция не найдена")
    return operation


@router.get('/')
def get_file_of_operation(
        operation_id: int,
        user: User = Depends(get_current_user),
        service: FileService = Depends(),
        operation_service: OperationsService = Depends()
):
    _check_authorization(operation_id=operation_id, user=user, service=operation_service)
    return service.get_file(operation_id=operation_id)


@router.post('/')
def upload_file(
        operation_id: int,
        file: UploadFile,
        user: User = Depends(get_current_user),
        service: FileService = Depends(),
        operation_service: OperationsService = Depends()
):
    operation = _check_authorization(operation_id=operation_id, user=user, service=operation_service)
    if operation.file is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Операция может хранить лишь 1 файл")
    service.upload_file(file=file, operation_id=operation_id)


@router.delete('/')
def delete_file(
        operation_id: int,
        user: User = Depends(get_current_user),
        service: FileService = Depends(),
        operation_service: OperationsService = Depends()
):
    _check_authorization(operation_id=operation_id, user=user, service=operation_service)
    service.delete_file(operation_id=operation_id)
