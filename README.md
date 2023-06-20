# ECON-script
updated ECON script for SMPL/SMPL-X data

the contents of this repository are (in order of creation):

-infer_final.py
updated script that outputs SMPL-X information

-infer_final_mat.py
updated version of infer_final.py that outputs rotation matrices instead of Rodriguez vectors.

-raw_to_tranf.py
isolates from the raw SMPL-X information the ones needed for the creation of a transformation matrix

-better_matrix.py
takes the isolated info from raw_to_tranf.py and outputs the actual matrix (with and without the scale)
