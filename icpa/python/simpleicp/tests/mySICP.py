"""
Read two point clouds from xyz files and run simpleICP.
"""

import time
from pathlib import Path

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
    X_fix = np.genfromtxt(tests_dirpath.joinpath(Path("../../../mydata/input_data/A_0_full.xyz")))
    X_mov = np.genfromtxt(tests_dirpath.joinpath(Path("../../../mydata/input_data/B_0_full.xyz")))
    kwargs = {
        "debug_dirpath": str(Path("debug").joinpath(f"Mes_{time.time()}"))
    }
    X_mov_transformed = run_simpleicp(X_fix, X_mov, kwargs)


if dataset == "Dragon" or dataset == "all":
    print('Processing dataset "Dragon"')
    X_fix = np.genfromtxt(tests_dirpath.joinpath(Path("../../../data/dragon1.xyz")))
    X_mov = np.genfromtxt(tests_dirpath.joinpath(Path("../../../data/dragon2.xyz")))
    kwargs = {
        "debug_dirpath": str(Path("debug").joinpath(f"Dragon_{time.time()}"))
    }
    X_mov_transformed = run_simpleicp(X_fix, X_mov, kwargs)

if dataset == "Airborne Lidar" or dataset == "all":
    print('Processing dataset "Airborne Lidar"')
    X_fix = np.genfromtxt(
        tests_dirpath.joinpath(Path("../../../data/airborne_lidar1.xyz"))
    )
    X_mov = np.genfromtxt(
        tests_dirpath.joinpath(Path("../../../data/airborne_lidar2.xyz"))
    )
    kwargs = {
        "debug_dirpath": str(Path("debug").joinpath(f"Airborne_Lidar_{time.time()}"))
    }
    X_mov_transformed = run_simpleicp(X_fix, X_mov, kwargs)


# Export original and adjusted point clouds to xyz files to check the result
if export_results:
    target_dir = Path("../../../mydata/output_data/")
    target_dir.mkdir(parents=True, exist_ok=True)

   

    # Generate unique file names for export
    base_filename_fix = "X_fix"
    base_filename_mov = "X_mov"
    base_filename_transf = "X_mov_transf"

    unique_filename_fix = generate_unique_filename(base_filename_fix)
    unique_filename_mov = generate_unique_filename(base_filename_mov)
    unique_filename_transf = generate_unique_filename(base_filename_transf)

    # Save point clouds with unique file names
    np.savetxt(target_dir.joinpath(Path(f"{unique_filename_fix}.xyz")), X_fix)
    np.savetxt(target_dir.joinpath(Path(f"{unique_filename_mov}.xyz")), X_mov)
    np.savetxt(target_dir.joinpath(Path(f"{unique_filename_transf}.xyz")), X_mov_transformed)

    print("Files exported to:")
    print(target_dir.joinpath(Path(f"{unique_filename_fix}.xyz")))
    print(target_dir.joinpath(Path(f"{unique_filename_mov}.xyz")))
    print(target_dir.joinpath(Path(f"{unique_filename_transf}.xyz")))

# Plot original and adjusted point clouds with matplotlib
if plot_results:
    import matplotlib.pyplot as plt

    # We need to select a small subset of points for the plot as scatter plots are very slow in mpl
    # https://stackoverflow.com/questions/18179928/speeding-up-matplotlib-scatter-plots
    no_points_to_plot = 10000
    idx_points_fix = np.random.permutation(np.shape(X_fix)[0])[0:no_points_to_plot]
    idx_points_mov = np.random.permutation(np.shape(X_mov)[0])[0:no_points_to_plot]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(
        X_fix[idx_points_fix, 0],
        X_fix[idx_points_fix, 1],
        X_fix[idx_points_fix, 2],
        c="r",
        marker=".",
    )
    ax.scatter(
        X_mov[idx_points_mov, 0],
        X_mov[idx_points_mov, 1],
        X_mov[idx_points_mov, 2],
        c="g",
        marker=".",
    )
    ax.scatter(
        X_mov_transformed[idx_points_mov, 0],
        X_mov_transformed[idx_points_mov, 1],
        X_mov_transformed[idx_points_mov, 2],
        c="b",
        marker=".",
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.show()
