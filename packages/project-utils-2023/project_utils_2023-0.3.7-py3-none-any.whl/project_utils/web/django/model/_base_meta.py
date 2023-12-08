from abc import ABCMeta


class BaseMeta(metaclass=ABCMeta):
    db_table: str
    abstract: bool = False
    table_id: int = 1000
