# Matrix Class

This is a Python project that implements a matrix using classes.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install matrix_class.

```bash
pip install matrix_class
```

## Usage

```python
from matrix import Matrix

# Create a new Matrix with 3 rows and 3 columns
m = Matrix(3, 3)

# Set the value of the cell at the first row and first column to 1.0
m[0, 0] = 1.0

# Get the value of the cell at the first row and first column
value = m[0, 0]

# Get the number of rows and columns
rows = m.rows
columns = m.columns

# Print the matrix
print(m)

# Calculate the determinant of the matrix
det = m.det

# Add two matrices
m1 = Matrix(3, 3)
m2 = Matrix(3, 3)
m3 = m1 + m2

# Subtract two matrices
m4 = m1 - m2

# Multiply matrix by a number
m5 = m1 * 2

# Multiply two matrices
m6 = m1 * m2
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)