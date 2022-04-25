import shutil, os

from sqlalchemy.orm import Session
from fastapi import UploadFile, Depends, HTTPException, status
from fastapi.responses import FileResponse

from iaccountant.database import get_session
from .. import tables


class FileService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_file_entity_by_opration(self, operation_id: int) -> tables.File:
        file = (
            self.session
            .query(tables.File)
            .filter_by(operation_id=operation_id)
            .first()
        )

        if not file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return file

    def upload_file(self, file: UploadFile, operation_id: int):
        file_entity = tables.File(
            operation_id=operation_id,
            origin_name=file.filename,
            media_type=file.content_type
        )

        self.session.add(file_entity)
        self.session.commit()

        with open(f'{file.filename}', "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        shutil.move(file.filename, "uploads/" + str(file_entity.id))

    def get_file(self, operation_id: int) -> FileResponse:
        file = self._get_file_entity_by_opration(operation_id=operation_id)

        file_path = "uploads/" + str(file.id)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return FileResponse(file_path, media_type=file.media_type, filename=file.origin_name)

    def delete_file(self, operation_id: int):
        file = self._get_file_entity_by_opration(operation_id=operation_id)

        self.session.delete(file)
        self.session.commit()

