import meshio
import matplotlib.pyplot as plt
import numpy as np

# Read the mesh file
mesh = meshio.read('t1.msh')

# Extract points and cells
points = mesh.points
cells = mesh.cells_dict["triangle"]

# Plot the mesh
plt.figure(figsize=(10, 8))
for cell in cells:
    polygon = points[cell]
    plt.fill(*zip(*polygon), edgecolor='black', fill=False)

# Plot points for better visualization
plt.scatter(points[:, 0], points[:, 1], color='red', s=10, zorder=5)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Mesh Plot')
plt.show()

# Initialize temperature distribution
num_points = points.shape[0]
temperature = np.zeros(num_points)
new_temperature = np.zeros(num_points)

# Initial condition: set a high temperature at the center of the mesh
center_point = np.mean(points, axis=0)
center_index = np.argmin(np.linalg.norm(points - center_point, axis=1))
temperature[center_index] = 100.0

# Problem parameters
alpha = 0.01  # Diffusion coefficient
dt = 0.01  # Time step size in seconds
time_minutes = 1
time_seconds = time_minutes * 60
nt = int(time_seconds / dt)


# Function to find neighbors of each point
def find_neighbors(cells, num_points):
    neighbors = [[] for _ in range(num_points)]
    for cell in cells:
        for i in range(3):
            for j in range(i + 1, 3):
                neighbors[cell[i]].append(cell[j])
                neighbors[cell[j]].append(cell[i])
    # Remove duplicates
    for i in range(num_points):
        neighbors[i] = list(set(neighbors[i]))
    return neighbors


neighbors = find_neighbors(cells, num_points)


# Function to apply boundary conditions
def apply_boundary_conditions(temperature):
    boundary_indices = np.unique(cells)
    temperature[boundary_indices] = 0.0
    return temperature


# Time-stepping loop
for t in range(nt):
    for i in range(num_points):
        sum_neighbors = 0.0
        for neighbor in neighbors[i]:
            sum_neighbors += temperature[neighbor]
        new_temperature[i] = temperature[i] + alpha * dt * (sum_neighbors - len(neighbors[i]) * temperature[i])

    # Apply boundary conditions
    new_temperature = apply_boundary_conditions(new_temperature)

    # Update the temperature values
    temperature[:] = new_temperature[:]

# Saving the results in a new mesh file
mesh.point_data = {"Temperature": temperature}
meshio.write("temperature_distribution.vtu", mesh)

# Visualizing the final temperature distribution
plt.scatter(points[:, 0], points[:, 1], c=temperature, cmap='hot', s=10)
plt.colorbar(label='Temperature (°C)')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('2D Temperature Distribution at t = 30 mins')
plt.show()
