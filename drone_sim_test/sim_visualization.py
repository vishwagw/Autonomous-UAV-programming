import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Drone:
    def __init__(self):
        # Initial state: position (x, y, z), velocity (vx, vy, vz), yaw (degrees)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0  # Altitude
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.yaw = 0.0  # Heading in degrees
        self.battery = 100.0  # Battery percentage
        self.is_flying = False
        # Store trajectory for plotting
        self.trajectory = [(self.x, self.y, self.z)]

    def update_state(self, dt):
        """Update drone's position and velocity based on current state."""
        if not self.is_flying:
            return
        
        # Update position based on velocity
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt
        
        # Ensure z doesn't go negative (ground level)
        if self.z < 0:
            self.z = 0
            self.vz = 0
        
        # Simulate battery drain
        self.battery -= 0.1 * dt
        if self.battery <= 0:
            self.land()

        # Record position for trajectory
        self.trajectory.append((self.x, self.y, self.z))

    def takeoff(self, altitude=1.0):
        """Take off to a specified altitude."""
        if not self.is_flying:
            self.is_flying = True
            self.vz = 0.5  # Simple upward velocity
            print(f"Drone taking off to {altitude}m...")
        else:
            print("Drone is already flying.")

    def land(self):
        """Land the drone."""
        if self.is_flying:
            self.is_flying = False
            self.vz = 0.0
            self.z = 0.0
            print("Drone landing...")
        else:
            print("Drone is already on the ground.")

    def set_velocity(self, vx, vy, vz):
        """Set drone velocity."""
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def set_yaw(self, yaw):
        """Set drone heading."""
        self.yaw = yaw % 360

    def get_state(self):
        """Return current state of the drone."""
        return {
            "x": self.x, "y": self.y, "z": self.z,
            "vx": self.vx, "vy": self.vy, "vz": self.vz,
            "yaw": self.yaw, "battery": self.battery,
            "is_flying": self.is_flying
        }

def autonomous_control(drone):
    """Example autonomous control logic."""
    drone.takeoff(altitude=10)
    time.sleep(2)  # Wait to reach altitude
    
    drone.set_velocity(10, 5, 0.0)  # Move forward and slightly right
    time.sleep(5)  # Move for 5 seconds
    
    drone.set_velocity(0.0, 0.0, 0.0)  # Stop
    drone.land()

def simulate(drone, duration=10, dt=0.1):
    """Run the simulation with real-time 3D plotting."""
    print("Starting simulation...")
    
    # Set up the 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Drone Trajectory')
    
    # Simulation loop
    for _ in range(int(duration / dt)):
        drone.update_state(dt)
        state = drone.get_state()
        
        # Print state
        print(f"Position: ({state['x']:.2f}, {state['y']:.2f}, {state['z']:.2f}) | "
              f"Velocity: ({state['vx']:.2f}, {state['vy']:.2f}, {state['vz']:.2f}) | "
              f"Yaw: {state['yaw']:.1f}° | Battery: {state['battery']:.1f}%")
        
        # Update plot
        traj = np.array(drone.trajectory)
        ax.clear()  # Clear previous frame
        ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], 'b-', label='Trajectory')
        ax.scatter([state['x']], [state['y']], [state['z']], color='r', label='Drone')
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.legend()
        plt.pause(0.01)  # Brief pause to update the plot
        
        time.sleep(dt)  # Simulate real-time step
    
    plt.show()  # Keep the final plot open


