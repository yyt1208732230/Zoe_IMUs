import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def plot_nudging_profiles():
    """Plot speed vs. time for three different nudging profiles on a white background."""
    # Time intervals and initial conditions
    t = np.linspace(0, 15, 300)
    initial_speed = 12.5  # Starting speed for all profiles
    final_speed = 12.05    # Speed after first deceleration
    max_time = 15           # Total time for simulation

    # Acceleration values for each profile
    a_low = -0.15
    a_medium = -0.25
    a_high = -0.35

    # Calculate deceleration times based on acceleration and speed change
    t_low = (final_speed - initial_speed) / a_low
    t_medium = (final_speed - initial_speed) / a_medium
    t_high = (final_speed - initial_speed) / a_high

    # Creating time arrays
    t = np.linspace(0, max_time, int(max_time * 60))  # using 60 points per second
    s_low = np.full_like(t, initial_speed)
    s_medium = np.full_like(t, initial_speed)
    s_high = np.full_like(t, initial_speed)

    # Set the speed changes during the deceleration phase
    s_low[(t > 5) & (t <= 5 + t_low)] = initial_speed + a_low * (t[(t > 5) & (t <= 5 + t_low)] - 5)
    s_medium[(t > 5) & (t <= 5 + t_medium)] = initial_speed + a_medium * (t[(t > 5) & (t <= 5 + t_medium)] - 5)
    s_high[(t > 5) & (t <= 5 + t_high)] = initial_speed + a_high * (t[(t > 5) & (t <= 5 + t_high)] - 5)

    # Set the speed for the final constant speed phase
    s_low[t > (5 + t_low)] = final_speed
    s_medium[t > (5 + t_medium)] = final_speed
    s_high[t > (5 + t_high)] = final_speed

    # Plotting the graph with a white background
    plt.figure(figsize=(10, 5))
    plt.plot(t, s_low, label='Low Nudging Profile', color='blue')
    plt.plot(t, s_medium, label='Medium Nudging Profile', color='orange')
    plt.plot(t, s_high, label='High Nudging Profile', color='green')

    plt.title('Speed vs. Time Graph for Different Nudging Profiles')
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (m/s)')
    plt.ylim(7, 17)
    plt.xlim(0, max_time)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()
    return plt

if __name__ == "__main__":
    fig = plot_nudging_profiles()
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{current_time}_nudging_profiles.png"
    fig.savefig(filename)
