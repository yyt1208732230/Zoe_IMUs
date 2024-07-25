import matplotlib.pyplot as plt
import numpy as np

def plot_nudging_profiles():
    """Plot speed vs. time for three different nudging profiles on a white background, with acceleration and deceleration phases."""
    # Constants
    # initial_speed = 12.5  # Starting speed for all profiles
    # final_speed = 12.05    # Speed after first deceleration
    # max_time = 15           # Total time for simulation
    initial_speed = 13.89  # Starting speed for all profiles
    final_speed = 13.33    # Speed after first deceleration
    max_time = 15           # Total time for simulation

    # Acceleration values for each profile
    a_low = -0.15
    a_medium = -0.25
    a_high = -0.35

    # Calculate times for deceleration and acceleration phases
    t_low = abs((final_speed - initial_speed) / a_low)
    t_medium = abs((final_speed - initial_speed) / a_medium)
    t_high = abs((final_speed - initial_speed) / a_high)

    # Time arrays for plotting
    t = np.linspace(0, max_time, 1000)  # High resolution for smooth curves

    # Initialize speed arrays
    s_low = np.full_like(t, initial_speed)
    s_medium = np.full_like(t, initial_speed)
    s_high = np.full_like(t, initial_speed)

    # Calculate speeds during deceleration and acceleration phases
    for profile, a, t_change in zip((s_low, s_medium, s_high), (a_low, a_medium, a_high), (t_low, t_medium, t_high)):
        profile[(t > 5) & (t <= 5 + t_change)] = initial_speed + a * (t[(t > 5) & (t <= 5 + t_change)] - 5)
        profile[(t > 5 + t_change) & (t <= 5 + 2 * t_change)] = final_speed - a * (t[(t > 5 + t_change) & (t <= 5 + 2 * t_change)] - (5 + t_change))

    # Plotting the graph with a white background
    plt.figure(figsize=(10, 5))
    plt.plot(t, s_high, label='High Nudging Profile', color='red')
    plt.plot(t, s_medium, label='Medium Nudging Profile', color='orange')
    plt.plot(t, s_low, label='Low Nudging Profile', color='green')

    plt.title('Speed vs. Time Graph for Different Nudging Profiles')
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (m/s)')
    plt.ylim(7, 17)
    plt.xlim(0, max_time)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.savefig('nudging_profiles.png')  # Save the figure to a file
    plt.show()
    pass

if __name__ == "__main__":
    plot_nudging_profiles()
