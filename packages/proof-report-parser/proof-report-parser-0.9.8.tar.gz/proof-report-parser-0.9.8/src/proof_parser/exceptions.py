class RowNotFoundException(Exception):
    def __init__(self, flag_str) -> None:
        self.flag_str = flag_str

    def __repr__(self) -> str:
        return f"can't find row by flag_str [{self.flag_str}]"


class TableNotFoundException(Exception):
    def __init__(self, table_desc) -> None:
        self.table_desc = table_desc

    def __repr__(self) -> str:
        return f"can't find table [{self.table_desc}]"
