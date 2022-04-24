import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String, unique=True, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    password_hash = sa.Column(sa.String, nullable=False)

    operations = relationship("Operation", cascade="all, delete")


class Operation(Base):
    __tablename__ = 'operations'

    id = sa.Column(sa.Integer, primary_key=True)
    author_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), index=True)
    date = sa.Column(sa.Date, nullable=False)
    kind = sa.Column(sa.String, nullable=False)
    amount = sa.Column(sa.Integer, nullable=False)
    description = sa.Column(sa.String, nullable=True)

    file = relationship("File", back_populates='operation', uselist=False, cascade="all, delete")


class File(Base):
    __tablename__ = 'files'

    id = sa.Column(sa.String, primary_key=True)
    operation_id = sa.Column(sa.Integer, sa.ForeignKey('operations.id'), index=True)
    origin_name = sa.Column(sa.String, nullable=False)
    media_type = sa.Column(sa.String, nullable=False)

    operation = relationship("Operation", back_populates='file')
