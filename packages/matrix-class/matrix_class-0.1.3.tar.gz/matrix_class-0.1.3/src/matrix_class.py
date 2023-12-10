from typing import TypeVar, List, Tuple

from .exceptions import ColumnOutOfBoundsException, RowOutOfBoundsException, MatrixIsNotSquare, MatrixSizesAreDifferent, \
    MatrixSizesAreWrongForMul

SPACE_BETWEEN_COLUMNS = 2
_MulT = TypeVar("_MulT", float, int, "Matrix")
_NumberT = TypeVar("_NumberT", float, int)


class Matrix:
    _matrix: List[List[float]] = []
    _rows: int
    _columns: int

    def __init__(self, rows: int, columns: int):
        self._rows = rows
        self._columns = columns
        self._matrix = [[0.0 for _ in range(columns)] for _ in range(rows)]

    def __getitem__(self, item: Tuple[int, int]) -> float:
        return self.get_item(item[0], item[1])

    def __setitem__(self, key: Tuple[int, int], value: float):
        self.set_item(key[0], key[1], value)

    def set_item(self, row: int, column: int, value: float):
        if row < 0 or row >= self._rows:
            raise RowOutOfBoundsException(row, self._rows)
        if column < 0 or column >= self._columns:
            raise ColumnOutOfBoundsException(column, self._columns)
        self._matrix[row][column] = value

    def get_item(self, row: int, column: int) -> float:
        if row < 0 or row >= self._rows:
            raise RowOutOfBoundsException(row, self._rows)
        if column < 0 or column >= self._columns:
            raise ColumnOutOfBoundsException(column, self._columns)
        return self._matrix[row][column]

    @property
    def columns(self) -> int:
        return self._columns

    @property
    def rows(self) -> int:
        return self._rows

    def __str__(self) -> str:
        text = ""
        max_number_length = self._get_max_number_length() + SPACE_BETWEEN_COLUMNS
        for row in range(self._rows):
            for column in range(self._columns):
                number = self._get_number_as_str(row, column)
                text += number.rjust(max_number_length)
            text += "\n"
        return text

    def _get_max_number_length(self) -> int:
        max_len = 0
        for row in range(self._rows):
            for column in range(self._columns):
                number = self._get_number_as_str(row, column)
                max_len = max(max_len, len(number))
        return max_len

    def _get_number_as_str(self, row: int, column: int) -> str:
        number = self._matrix[row][column]
        if number == int(number):
            return str(int(number))
        else:
            return str(number)

    @property
    def det(self) -> float:
        if self._columns != self._rows:
            raise MatrixIsNotSquare(self._rows, self._columns)
        if self._columns == 1:
            return self._matrix[0][0]
        if self._columns == 2:
            return self._matrix[0][0] * self._matrix[1][1] - self._matrix[0][1] * self._matrix[1][0]
        det = 0.0
        for column in range(self._columns):
            sign = -1 if column % 2 == 1 else 1
            det += sign * self._matrix[0][column] * self._get_det_of_minor(column)
        return det

    def _get_det_of_minor(self, column: int) -> float:
        minor = Matrix(self.rows - 1, self.columns - 1)
        for row in range(self._rows):
            for current_column in range(self._columns):
                if row == 0 or current_column == column:
                    continue
                minor_row = row - 1
                minor_column = current_column
                if current_column > column:
                    minor_column -= 1
                minor[minor_row, minor_column] = self._matrix[row][current_column]
        return minor.det

    def __add__(self, other: "Matrix") -> "Matrix":
        if self._rows != other._rows or self._columns != other._columns:
            raise MatrixSizesAreDifferent(self._rows, self._columns, other._rows, other._columns)
        result = Matrix(self._rows, self._columns)
        for row in range(self._rows):
            for column in range(self._columns):
                result[row, column] = self._matrix[row][column] + other._matrix[row][column]
        return result

    def __sub__(self, other: "Matrix") -> "Matrix":
        if self._rows != other._rows or self._columns != other._columns:
            raise MatrixSizesAreDifferent(self._rows, self._columns, other._rows, other._columns)
        result = Matrix(self._rows, self._columns)
        for row in range(self._rows):
            for column in range(self._columns):
                result[row, column] = self._matrix[row][column] - other._matrix[row][column]
        return result

    def __mul__(self, other: _MulT) -> "Matrix":
        if isinstance(other, Matrix):
            return self.times_by_matrix(other)
        else:
            return self.times_by_number(other)

    def times_by_matrix(self, other: "Matrix") -> "Matrix":
        if self._columns != other._rows:
            raise MatrixSizesAreWrongForMul(self._columns, other._rows)
        result = Matrix(self._rows, other._columns)
        for row in range(self._rows):
            for column in range(other._columns):
                result[row, column] = self._get_mul_item_matrix(row, column, other)
        return result

    def _get_mul_item_matrix(self, row: int, column: int, other: "Matrix") -> float:
        item = 0.0
        for i in range(self._columns):
            item += self._matrix[row][i] * other._matrix[i][column]
        return item

    def times_by_number(self, number: _NumberT) -> "Matrix":
        result = Matrix(self._rows, self._columns)
        for row in range(self._rows):
            for column in range(self._columns):
                result[row, column] = self._matrix[row][column] * number
        return result
