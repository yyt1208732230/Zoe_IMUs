import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.animation import FuncAnimation

def read_imu_data(csv_file_path):
    df = pd.read_csv(csv_file_path, usecols=['timestamp', 'X', 'Y', 'Z'])
    return df

def set_axes_equal(ax):
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()
    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)
    plot_radius = 0.5*max([x_range, y_range, z_range])
    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

def visualize_imu_data(df):
    t = df['timestamp']
    x = df['X']
    y = df['Y']
    z = df['Z']
    
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111, projection='3d')
    norm = Normalize(vmin=min(t), vmax=max(t))
    cmap = plt.get_cmap('jet')
    mappable = ScalarMappable(norm=norm, cmap=cmap)
    
    for i in range(len(x)-1):
        ax.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=mappable.to_rgba(t[i]))
    
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    plt.title('Real IMU Data Visualization')
    set_axes_equal(ax)
    cbar_ax = fig.add_axes([0.92, 0.1, 0.03, 0.8])  # [left, bottom, width, height]
    cbar = fig.colorbar(mappable, cax=cbar_ax)
    cbar.set_label('Time')
    plt.show()
    pass

def animate_imu_data(df, filename='imu_data_animation.gif'):
    """
    Animate the IMU data and save it as a GIF.
    
    Parameters:
    - df: DataFrame with the IMU data, including 'timestamp', 'X', 'Y', 'Z'.
    - filename: Filename for the saved GIF.
    """
    # Setup figure and 3D axis
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    norm = Normalize(vmin=df['timestamp'].min(), vmax=df['timestamp'].max())
    cmap = plt.get_cmap('jet')

    # Initialization function: plot the background of each frame
    def init():
        ax.clear()
        set_axes_equal(ax)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        plt.title('IMU Data Visualization')

    # Animation update function
    def update(frame):
        ax.clear()
        set_axes_equal(ax)  # Ensure consistent axes scale
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        t, x, y, z = df['timestamp'], df['X'], df['Y'], df['Z']
        ax.plot(x[:frame], y[:frame], z[:frame], color='blue')

    ani = FuncAnimation(fig, update, frames=len(df), init_func=init, blit=False, interval=50)

    # Save the animation
    ani.save(filename, writer='imagemagick', fps=30)

# Integrate this function into your existing script where you define the main method
# and ensure to call this function with the appropriate DataFrame and filename.


def main():
    # Path to your CSV file
    csv_file_path = './imuLog_1710860418.csv'  # Change this to the path of your CSV file

    # Reading the IMU data from the CSV file
    df = read_imu_data(csv_file_path)

    # Visualizing the IMU data
    visualize_imu_data(df)
    # animate_imu_data(df)

if __name__ == "__main__":
    main()
