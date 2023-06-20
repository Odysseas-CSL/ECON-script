import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def copy_text(input_file, output_file):
    # Open the input file in read mode
    with open(input_file, 'r') as file:
        # Read the content of the input file
        content = file.read()

        
        # Specify the start and end markers for the first part
        start_marker_1 = "globalorient_mat:"
        end_marker_1 = "transl:"

        # Specify the start and end markers for the second part
        start_marker_2 = "transl:"
        end_marker_2 = "expression:"

        # Specify the start and end markers for the third part
        start_marker_3 = "scale:"
        

        # Find the start and end indices of the first part
        start_index_1 = content.find(start_marker_1)
        end_index_1 = content.find(end_marker_1, start_index_1)

        # Adjust the end index of the first part to exclude the end marker
        end_index_1 = content.rfind('\n', start_index_1, end_index_1)

        # Find the start and end indices of the second part
        start_index_2 = content.find(start_marker_2, end_index_1)
        end_index_2 = content.find(end_marker_2, start_index_2)

        # Adjust the end index of the second part to exclude the end marker
        end_index_2 = content.rfind('\n', start_index_2, end_index_2)

        # Find the start index of the third part
        start_index_3 = content.find(start_marker_3)

        # Extract the desired parts of the content
        extracted_text_1 = content[start_index_1:end_index_1]
        extracted_text_2 = content[start_index_2:end_index_2]
        extracted_text_3 = content[start_index_3:]

    # Get the base name of the input file
    input_base_name = os.path.basename(input_file)

    # Create the output file name
    output_file_name = f"{os.path.splitext(input_base_name)[0]}_T.txt"
    
    # Use the same directory as the input file for the output file
    output_dir = os.path.dirname(os.path.abspath(input_file))
    
    # Create the output file path
    output_file_path = os.path.join(output_dir, output_file_name)

 

    # Open the output file in write mode
    with open(output_file_path, 'w') as file:
        # Write the extracted text to the output file
        file.write(extracted_text_1 + '\n')
        file.write(extracted_text_2 + '\n')
        file.write(extracted_text_3)

    print(f"Extraction and copying complete.Location: {output_file_path} Output file: {output_file_name}")


# Prompt the user to select the input file
Tk().withdraw()  # Hide the tkinter root window
input_file_path = askopenfilename(title="Select Input File", filetypes=[("Text Files", "*.txt")])

if not input_file_path:
    print("No input file selected. Exiting...")
    exit()

# Call the function to perform the extraction and copying
copy_text(input_file_path, "")
