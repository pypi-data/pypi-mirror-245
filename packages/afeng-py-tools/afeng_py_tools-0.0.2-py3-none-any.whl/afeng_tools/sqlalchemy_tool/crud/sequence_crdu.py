from sqlalchemy import Sequence
from sqlalchemy.orm import Session
from sqlalchemy.sql.ddl import DropSequence, CreateSequence

from afeng_tools.sqlalchemy_tool.core.sqlalchemy_session_decorator import auto_commit_db


@auto_commit_db()
def create_sequence(sequence_name: str, db: Session = None):
    # create sequence {sequence_name} start with 1 increment by 1 nocache nocycle
    db.execute(CreateSequence(Sequence(name=sequence_name, start=1, increment=1, cycle=False, cache=False),
                              if_not_exists=True))


@auto_commit_db()
def drop_sequence(sequence_name: str, db: Session = None):
    db.execute(DropSequence(Sequence(sequence_name)))
