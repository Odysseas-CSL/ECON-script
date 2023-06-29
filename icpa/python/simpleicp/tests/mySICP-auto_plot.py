"""
Read two point clouds from xyz files and run simpleICP.
"""

import os
import time
from pathlib import Path
import plotly.graph_objects as go

import numpy as np
from simpleicp import PointCloud, SimpleICP



# User inputs
dataset = "Mes"
export_results = True
plot_results = True

tests_dirpath = Path(__file__).parent

# Function to generate unique file name with counter
def generate_unique_filename(base_filename):
    counter = 1
    filename = f"{base_filename}_{counter}"
    while (target_dir / filename).is_file():
        counter += 1
        filename = f"{base_filename}_{counter}"
    return filename

# TO_DO fix problem: overwrites existing files filename_i instead of creating filename_i+1


def run_simpleicp(X_fix, X_mov, kwargs):
    """Small helper function to run simpleICP for each dataset."""

    # Create point cloud for fixed point cloud
    pc_fix = PointCloud(X_fix, columns=["x", "y", "z"])

    # Create point cloud for movable point cloud (copy=True to keep original X_mov for plot)
    pc_mov = PointCloud(X_mov, columns=["x", "y", "z"], copy=True)

    # Create simpleICP object, add point clouds, and run algorithm!
    icp = SimpleICP()
    icp.add_point_clouds(pc_fix, pc_mov)
    res = icp.run(**kwargs)
    _, X_mov_transformed, *_ = res

    return X_mov_transformed



if dataset == "Mes" or dataset == "all":
    print('Processing dataset "Mes"')


    input_data_dir = tests_dirpath.joinpath(Path("../../../mydata/input_data/"))

    # Find all files in the input_data directory that end with "_0_full.xyz"
    file_list = sorted(input_data_dir.glob("*_0_full.xyz"))

    if len(file_list) > 0:
        # Sort the file list alphabetically and select the first file
        X_fix_file = sorted(file_list)[0]
    else:
        raise FileNotFoundError("No file ending with '_0_full.xyz' found in the input_data directory.")

    # Read the file and assign it to X_fix
    X_fix = np.genfromtxt(X_fix_file)




    if len(file_list) >= 2:
        # Sort the file list alphabetically and select the second file
        X_mov_file = sorted(file_list)[1]
    else:
        raise FileNotFoundError("Less than two files ending with '_0_full.xyz' found in the input_data directory.")

    # Read the file and assign it to X_mov
    X_mov = np.genfromtxt(X_mov_file)




    if len(file_list) >= 3:
        # Sort the file list alphabetically and select the second file
        X_mov_file_2 = sorted(file_list)[2]
    else:
        raise FileNotFoundError("Less than three files ending with '_0_full.xyz' found in the input_data directory.")

    # Read the file and assign it to X_mov
    X_mov_2 = np.genfromtxt(X_mov_file_2)



    kwargs = {
        "debug_dirpath": str(Path("debug").joinpath(f"Mes_{time.time()}"))
    }
    X_mov_transformed = run_simpleicp(X_fix, X_mov, kwargs)


    kwargs_2 = {
        "debug_dirpath": str(Path("debug").joinpath(f"Mes_{time.time()}"))
    }
    X_mov_transformed_2 = run_simpleicp(X_fix, X_mov_2, kwargs_2)

# Export original and adjusted point clouds to xyz files to check the result
if export_results:
    target_dir = Path("../../../mydata/output_data/")
    target_dir.mkdir(parents=True, exist_ok=True)

   

    # Generate unique file names for export
    base_filename_fix = "X_fix"
    base_filename_mov = "X_mov"
    base_filename_mov_2 = "X_mov_2"
    base_filename_transf = "X_mov_transf"
    base_filename_transf_2 = "X_mov_transf_2"

    unique_filename_fix = generate_unique_filename(base_filename_fix)
    unique_filename_mov = generate_unique_filename(base_filename_mov)
    unique_filename_mov_2 = generate_unique_filename(base_filename_mov_2)
    unique_filename_transf = generate_unique_filename(base_filename_transf)
    unique_filename_transf_2 = generate_unique_filename(base_filename_transf_2)


    # Save point clouds with unique file names
    np.savetxt(target_dir.joinpath(Path(f"{unique_filename_fix}.xyz")), X_fix)
    np.savetxt(target_dir.joinpath(Path(f"{unique_filename_mov}.xyz")), X_mov)
    np.savetxt(target_dir.joinpath(Path(f"{unique_filename_mov_2}.xyz")), X_mov_2)
    np.savetxt(target_dir.joinpath(Path(f"{unique_filename_transf}.xyz")), X_mov_transformed)
    np.savetxt(target_dir.joinpath(Path(f"{unique_filename_transf_2}.xyz")), X_mov_transformed_2)

    print("Files exported to:")
    print(target_dir.joinpath(Path(f"{unique_filename_fix}.xyz")))
    print(target_dir.joinpath(Path(f"{unique_filename_mov}.xyz")))
    print(target_dir.joinpath(Path(f"{unique_filename_mov_2}.xyz")))
    print(target_dir.joinpath(Path(f"{unique_filename_transf}.xyz")))
    print(target_dir.joinpath(Path(f"{unique_filename_transf_2}.xyz")))

# Plot original and adjusted point clouds with matplotlib
if plot_results:

    # We need to select a small subset of points for the plot as scatter plots are very slow in mpl
    # https://stackoverflow.com/questions/18179928/speeding-up-matplotlib-scatter-plots
    no_points_to_plot = 10000
    idx_points_fix = np.random.permutation(np.shape(X_fix)[0])[0:no_points_to_plot]
    idx_points_mov = np.random.permutation(np.shape(X_mov)[0])[0:no_points_to_plot]
    idx_points_mov_2 = np.random.permutation(np.shape(X_mov_2)[0])[0:no_points_to_plot]

    fig = go.Figure(data=[
    go.Scatter3d(
        x=X_fix[idx_points_fix, 0],
        y=X_fix[idx_points_fix, 1],
        z=X_fix[idx_points_fix, 2],
        mode='markers',
        marker=dict(color='red', size=3),
        name='X_fix'
    ),
    go.Scatter3d(
        x=X_mov[idx_points_mov, 0],
        y=X_mov[idx_points_mov, 1],
        z=X_mov[idx_points_mov, 2],
        mode='markers',
        marker=dict(color='green', size=3),
        name='X_mov'
    ),
    go.Scatter3d(
        x=X_mov_transformed[idx_points_mov, 0],
        y=X_mov_transformed[idx_points_mov, 1],
        z=X_mov_transformed[idx_points_mov, 2],
        mode='markers',
        marker=dict(color='blue', size=3),
        name='X_mov_transformed'
    ),
    go.Scatter3d(
        x=X_mov_2[idx_points_mov_2, 0],
        y=X_mov_2[idx_points_mov_2, 1],
        z=X_mov_2[idx_points_mov_2, 2],
        mode='markers',
        marker=dict(color='yellow', size=3),
        name='X_mov_2'
    ),
    go.Scatter3d(
        x=X_mov_transformed_2[idx_points_mov_2, 0],
        y=X_mov_transformed_2[idx_points_mov_2, 1],
        z=X_mov_transformed_2[idx_points_mov_2, 2],
        mode='markers',
        marker=dict(color='cyan', size=3),
        name='X_mov_transformed_2'
    )
])

# Set the axis labels
fig.update_layout(scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='z'))

# Specify the directory path
output_directory = '/content/ECON-script/icpa/mydata/output_data'

# Create the directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Set the file path for saving the plot
file_path = os.path.join(output_directory, 'interactive_plot.html')

# Export the interactive plot as an HTML file
fig.write_html(file_path)

# Display a message indicating the file export
print("Interactive plot exported to:", file_path)