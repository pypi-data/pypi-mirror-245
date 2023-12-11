from typing import TypeVar, List, Tuple, overload

from .exceptions import ColumnOutOfBoundsException, RowOutOfBoundsException, MatrixIsNotSquare, MatrixSizesAreDifferent, \
    MatrixSizesAreWrongForMul, MatrixHaveNotInverseVersion

SPACE_BETWEEN_COLUMNS = 2
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

    def __setitem__(self, key: Tuple[int, int], value: _NumberT):
        self.set_item(key[0], key[1], value)

    def set_item(self, row: int, column: int, value: _NumberT):
        if row < 0 or row >= self._rows:
            raise RowOutOfBoundsException(row, self._rows)
        if column < 0 or column >= self._columns:
            raise ColumnOutOfBoundsException(column, self._columns)
        self._matrix[row][column] = float(value)

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
            det += sign * self._matrix[0][column] * self._get_det_of_minor(0, column)
        return det

    def _get_det_of_minor(self, row: int, column: int) -> float:
        minor = Matrix(self.rows - 1, self.columns - 1)
        for current_row in range(self._rows):
            for current_column in range(self._columns):
                if current_row == row or current_column == column:
                    continue
                minor_row = current_row
                if current_row > row:
                    minor_row -= 1
                minor_column = current_column
                if current_column > column:
                    minor_column -= 1
                minor[minor_row, minor_column] = self._matrix[current_row][current_column]
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

    @overload
    def __mul__(self, other: _NumberT) -> "Matrix":
        pass

    @overload
    def __mul__(self, other: "Matrix") -> "Matrix":
        pass

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.get_times_by_matrix(other)
        if isinstance(other, (int, float)):
            return self.get_times_by_number(other)
        raise NotImplementedError()

    def get_times_by_matrix(self, other: "Matrix") -> "Matrix":
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

    def get_times_by_number(self, number: _NumberT) -> "Matrix":
        result = Matrix(self._rows, self._columns)
        for row in range(self._rows):
            for column in range(self._columns):
                result[row, column] = self._matrix[row][column] * number
        return result

    def get_transported(self) -> "Matrix":
        """
        changing rows to columns and columns to rows
        :return: Transposed matrix
        """
        result = Matrix(self._columns, self._rows)
        for row in range(self._rows):
            for column in range(self._columns):
                result[column, row] = self._matrix[row][column]
        return result

    def to_transported(self) -> None:
        matrix = self.get_transported()
        self._matrix = matrix._matrix
        self._rows = matrix.rows
        self._columns = matrix.columns

    def get_complement(self) -> "Matrix":
        if self._columns != self._rows:
            raise MatrixIsNotSquare(self._rows, self._columns)
        result = Matrix(self._rows, self._columns)
        for row in range(self._rows):
            for column in range(self._columns):
                result[row, column] = self._get_complement_item(row, column)
        return result

    def to_complement(self) -> None:
        self._matrix = self.get_complement()._matrix

    def _get_complement_item(self, row: int, column: int) -> float:
        sign = -1 if (row + column) % 2 == 1 else 1
        return sign * self._get_det_of_minor(row, column)

    def get_inverse(self) -> "Matrix":
        det = self.det
        if det == 0.0:
            raise MatrixHaveNotInverseVersion()
        return self.get_complement().get_transported() * (1 / det)

    def to_inverse(self) -> None:
        self._matrix = self.get_inverse()._matrix
