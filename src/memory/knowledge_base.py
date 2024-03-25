from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine
from contextlib import closing

from src.config import Config

class Knowledge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tag: str
    contents: str

class KnowledgeBase:
    def __init__(self):
        config = Config()
        sqlite_path = config.get_sqlite_db()
        self.engine = create_engine(f"sqlite:///{sqlite_path}", connect_args={"timeout": 15, "check_same_thread": False}, future=True)

    def add_knowledge(self, tag: str, contents: str):
        knowledge = Knowledge(tag=tag, contents=contents)
        with closing(self.engine.connect()) as conn:
            with conn.begin():
                conn.exec(knowledge.insert())

    def get_knowledge(self, tag: str) -> Optional[str]:
        """
        Retrieve the contents associated with the given tag.

        Returns:
            str: The contents associated with the tag, if it exists. Otherwise, None.
        """
        with closing(self.engine.connect()) as conn:
            result = conn.exec(Knowledge.select().where(Knowledge.tag == tag)).first()
            if result:
                return result.contents
            return None

# TODO: Implement BM25 search for the tag check.
