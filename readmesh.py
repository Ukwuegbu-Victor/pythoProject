# Code to read mesh file
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
