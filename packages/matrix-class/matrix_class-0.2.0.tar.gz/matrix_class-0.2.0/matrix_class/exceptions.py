class RowOutOfBoundsException(KeyError):
    def __init__(self, given_row: int, rows: int):
        super().__init__(f"Row {given_row} out of bounds. Matrix has {rows} rows.")


class ColumnOutOfBoundsException(KeyError):
    def __init__(self, given_column: int, columns: int):
        super().__init__(f"Column {given_column} out of bounds. Matrix has {columns} columns.")


class MatrixIsNotSquare(Exception):
    def __init__(self, rows: int, columns: int):
        super().__init__(f"Matrix is not square. Matrix has {rows} rows and {columns} columns.")


class MatrixSizesAreDifferent(Exception):
    def __init__(self, rows1: int, columns1: int, rows2: int, columns2: int):
        super().__init__(f"Matrix sizes are different. Matrix 1 has {rows1} rows and {columns1} columns. "
                         f"Matrix 2 has {rows2} rows and {columns2} columns.")


class MatrixSizesAreWrongForMul(Exception):
    def __init__(self, columns1: int, rows2: int):
        super().__init__(f"Two matrix must have the same number of first columns and second rows."
                         f"Matrix 1 has {columns1} columns and Matrix 2 has {rows2} rows.")


class MatrixHaveNotInverseVersion(Exception):
    def __init__(self):
        super().__init__("Matrix have not inverse version. Det = 0.")


