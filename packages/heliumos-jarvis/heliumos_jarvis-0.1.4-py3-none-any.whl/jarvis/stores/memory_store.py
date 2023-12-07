import logging
from abc import ABC

import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from pydantic import BaseModel

logger = logging.getLogger(__name__)
DEFAULT_CONNECTION_STRING = "postgresql://postgres:mypassword@localhost/q_xun"


class Memory(BaseModel):
    id: str
    memory_type: str  # BUFFER, SUMMARY_BUFFER, ENTITY, KNOWLEDGE_GRAPH, VECTOR_STORE
    memory_buffer_window: int
    summary_threshold: int


class MemoryStore(ABC):
    def __init__(
            self,
            connection_string: str = DEFAULT_CONNECTION_STRING,
            table_name: str = "memory_store",
    ):
        try:
            self.connection = psycopg.connect(connection_string)
            self.cursor = self.connection.cursor(row_factory=dict_row)
        except psycopg.OperationalError as error:
            logger.error(error)

        self.table_name = table_name

        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        create_table_query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGINT PRIMARY KEY,
            memory_type VARCHAR(22),
            memory_buffer_window INT DEFAULT 3,
            summary_threshold INT DEFAULT 300
        );"""
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def add_memory(
            self,
            memory_id: str,
            memory_type: str,
            memory_buffer_window: int,
            summary_threshold: int
    ):
        query = sql.SQL(
            "INSERT INTO {} (id, memory_type, memory_buffer_window, summary_threshold) VALUES (%s, %s, %s, %s);").format(
            sql.Identifier(self.table_name)
        )
        self.cursor.execute(
            query, (memory_id, memory_type, memory_buffer_window, summary_threshold)
        )
        self.connection.commit()

    def get_by_id(self, memory_id: str):
        query = (
            f"SELECT * FROM {self.table_name} WHERE id = %s ORDER by id limit 1 ;"
        )
        self.cursor.execute(query, (memory_id,))
        records = self.cursor.fetchall()

        return Memory(
            id=str(records[0]["id"]),
            memory_type=records[0]["memory_type"],
            memory_buffer_window=records[0]["memory_buffer_window"],
            summary_threshold=records[0]["summary_threshold"],
        )

    def exist_by_id(self, memory_id: str):
        query = (
            f"SELECT EXISTS (SELECT 1 FROM {self.table_name} WHERE id = %s ) ;"
        )
        self.cursor.execute(query, (memory_id,))
        records = self.cursor.fetchall()
        return records[0]['exists']
