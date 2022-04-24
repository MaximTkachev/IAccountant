from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from typing import List, Optional

from iaccountant.database import get_session
from iaccountant.models.operations import OperationKind
from iaccountant.models.operations import OperationCreate
from .. import tables


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_all_operations_of_current_user(self, kind: Optional[OperationKind], user_id: int) -> List[tables.Operation]:
        query = (
            self.session
            .query(tables.Operation)
            .filter_by(author_id=user_id)
        )

        if kind:
            query = query.filter_by(kind=kind)

        operations = query.all()
        return operations

    def create(self, user_id: int, operation_data: OperationCreate) -> tables.Operation:
        operation = tables.Operation(
            author_id=user_id,
            **operation_data.dict()
        )

        self.session.add(operation)
        self.session.commit()

        return operation

    def get_operation_by_id(self, operation_id: int, author_id) -> tables.Operation:
        operation = (
            self.session
            .query(tables.Operation)
            .filter_by(id=operation_id)
            .filter_by(author_id=author_id)
            .first()
        )

        if not operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return operation
