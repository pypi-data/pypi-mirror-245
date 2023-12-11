
# Matrix Class Library

This Python library provides an implementation of a matrix using classes, offering a range of functionalities for matrix operations.

## Installation

Install the library using pip:

```bash
pip install matrix_class
```

## Features

- **Initialization**: Create matrices with specified rows and columns.
- **Item Assignment and Retrieval**: Set and get values of specific cells in the matrix.
- **Matrix Properties**: Access the number of rows and columns in the matrix.
- **String Representation**: Print the matrix in a readable format.
- **Determinant Calculation**: Compute the determinant of the matrix.
- **Matrix Arithmetic**: Perform addition, subtraction, and multiplication (with both scalars and other matrices).
- **Matrix Transposition**: Transpose the matrix, swapping rows with columns.
- **Matrix Inversion**: Invert a matrix, provided it is square and has a non-zero determinant.
- **Matrix Complementation**: Calculate the complement of a matrix.

## Usage

Below are some examples of how to use the Matrix class:

```python
from matrix import Matrix

# Create a new Matrix with specified dimensions
matrix = Matrix(3, 3)

# Set and get values
matrix[1, 1] = 5.0
value = matrix[1, 1]

# Access matrix properties
rows = matrix.rows
columns = matrix.columns

# Print the matrix
print(matrix)

# Perform arithmetic operations
sum_matrix = matrix1 + matrix2
difference = matrix1 - matrix2
product = matrix1 * matrix2
scaled_matrix = matrix * 2.0

# Transpose and invert matrices
transposed_matrix = matrix.get_transported()
inverse_matrix = matrix.get_inverse()
```

## Contributing

Contributions to enhance the Matrix Class Library are welcomed. Please open an issue first to discuss proposed changes. Ensure to update tests as appropriate.

## License

This library is released under the [MIT License](https://choosealicense.com/licenses/mit/).
