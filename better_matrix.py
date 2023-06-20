import os
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Prompt the user to select a file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# Read the file
with open(file_path, 'r') as file:
    contents = file.read()

# Find the start and end indices of the desired elements (first row)
start_index_1 = contents.find("[[[[") + 4
end_index_1 = contents.find(",", start_index_1)

start_index_2 = end_index_1 + 1
end_index_2 = contents.find(",", start_index_2)

start_index_3 = end_index_2 + 1
end_index_3 = contents.find("]", start_index_3)

# Find the start and end indices of the desired elements (second row)
start_index_4 = contents.find("[", end_index_3) + 1
end_index_4 = contents.find(",", start_index_4)

start_index_5 = end_index_4 + 1
end_index_5 = contents.find(",", start_index_5)

start_index_6 = end_index_5 + 1
end_index_6 = contents.find("]", start_index_6)

# Find the start and end indices of the desired elements (third row)
start_index_7 = contents.find("[", end_index_6) + 1
end_index_7 = contents.find(",", start_index_7)

start_index_8 = end_index_7 + 1
end_index_8 = contents.find(",", start_index_8)

start_index_9 = end_index_8 + 1
end_index_9 = contents.find("]]]]", start_index_9)

# Find the start and end indices of the desired elements (fourth column)
start_index_10 = contents.find("[[", end_index_9) + 2
end_index_10 = contents.find(",", start_index_10)

start_index_11 = end_index_10 + 1
end_index_11 = contents.find(",", start_index_11)

start_index_12 = end_index_11 + 1
end_index_12 = contents.find("]]", start_index_12)

# Find the start and end indices of the desired elements (last element)
start_index_13 = contents.find("[[", end_index_12) + 2
end_index_13 = contents.find("]]", start_index_13)


# Extract the desired element
element_1 = float(contents[start_index_1:end_index_1])
element_2 = float(contents[start_index_2:end_index_2])
element_3 = float(contents[start_index_3:end_index_3])

element_4 = float(contents[start_index_4:end_index_4])
element_5 = float(contents[start_index_5:end_index_5])
element_6 = float(contents[start_index_6:end_index_6])

element_7 = float(contents[start_index_7:end_index_7])
element_8 = float(contents[start_index_8:end_index_8])
element_9 = float(contents[start_index_9:end_index_9])

element_10 = float(contents[start_index_10:end_index_10])
element_11 = float(contents[start_index_11:end_index_11])
element_12 = float(contents[start_index_12:end_index_12])

element_13 = float(contents[start_index_13:end_index_13])

# Create a 4x4 matrix with the elements
matrix_1 = np.zeros((4, 4))
matrix_1[3,3] = 1

matrix_1[0, 0] = element_1
matrix_1[0, 1] = element_2
matrix_1[0, 2] = element_3

matrix_1[1, 0] = element_4
matrix_1[1, 1] = element_5
matrix_1[1, 2] = element_6

matrix_1[2, 0] = element_7
matrix_1[2, 1] = element_8
matrix_1[2, 2] = element_9

matrix_1[0, 3] = element_10
matrix_1[1, 3] = element_11
matrix_1[2, 3] = element_12


# Create a 4x4 matrix with the elements
matrix_2 = np.zeros((4, 4))
matrix_2[3,3] = 1

matrix_2[0, 0] = (element_1 * element_13)
matrix_2[0, 1] = element_2
matrix_2[0, 2] = element_3

matrix_2[1, 0] = element_4
matrix_2[1, 1] = (element_5 * element_13)
matrix_2[1, 2] = element_6

matrix_2[2, 0] = element_7
matrix_2[2, 1] = element_8
matrix_2[2, 2] = (element_9 * element_13)

matrix_2[0, 3] = element_10
matrix_2[1, 3] = element_11
matrix_2[2, 3] = element_12

print("Matrix (no scale):")
print(matrix_1)
print("Matrix (with scale):")
print(matrix_2)

# Create the output file path
output_file_path = os.path.splitext(file_path)[0] + 'ransf.txt'

# Write the matrices to the output file
with open(output_file_path, 'w') as output_file:
    output_file.write("Matrix (no scale):\n")
    output_file.write(str(matrix_1))
    output_file.write("\n\n")
    output_file.write("Matrix (with scale):\n")
    output_file.write(str(matrix_2))

print("Results exported to:", output_file_path)