import numpy as np

# -----------------------------
# Parameters
# -----------------------------
R = 0.0005       # 0.5 mm (hexagon radius) [m]
h = 0.0036        # starting height above substrate [m]
n_beams = 6

# Angle definitions
angles = np.linspace(0, 2*np.pi, n_beams, endpoint=False)

# Laser inclination
theta = np.deg2rad(30.0)   # angle from vertical

# Containers
impact_points = []
directions = []
start_points = []

for ang in angles:
    # -----------------------------
    # 1. Impact point (on substrate)
    # -z is scanning direction, x is transverse up
    # -----------------------------
    x = -R * np.sin(ang)
    z = -R * np.cos(ang)
    impact = np.array([x, 0.0, z])
    
    # -----------------------------
    # 2. Direction vector
    # -----------------------------
    # Radial inward direction (toward center)
    radial_in = np.array([np.sin(ang), 0.0, np.cos(ang)])
    
    # Normalize radial (already unit, but safe)
    radial_in = radial_in / np.linalg.norm(radial_in)
    
    # Combine vertical + radial
    d = np.zeros(3)
    d[0] = np.sin(theta) * radial_in[0]
    d[1] = np.cos(theta)   # downward
    d[2] = np.sin(theta) * radial_in[2]
    
    # Normalize (safety)
    d = d / np.linalg.norm(d)
    
    # -----------------------------
    # 3. Starting point at height h
    # -----------------------------
    # We want y_start = h, so solve:
    # impact = start + s * d  → find s
    s = (h - 0.0) / d[1]   # since y_impact = 0
    
    start = impact - s * d
    
    # Store
    impact_points.append(impact)
    directions.append(d)
    start_points.append(start)

# Convert to arrays
impact_points = np.array(impact_points)
directions = np.array(directions)
start_points = np.array(start_points)

# -----------------------------
# Output
# -----------------------------
print("Impact points (m):")
print(impact_points)

print("\nDirection vectors:")
print(directions)

print("\nStarting points (m):")
print(start_points)

# -----------------------------
# Scanning motion parameters
# -----------------------------
v_scan = 0.450 / 60.0   # m/s
t_end = 2.0                        # total simulation time [s] (CHANGE as needed)

# Total displacement along -z
dz = -v_scan * t_end

# -----------------------------
# Final positions of laser origins
# -----------------------------
start_points_final = start_points.copy()
start_points_final[:, 2] += dz   # shift all z-coordinates

# -----------------------------
# Output
# -----------------------------
print("\nScan speed (m/s):", v_scan)
print("Simulation time (s):", t_end)
print("Total displacement in z (m):", dz)

print("\nFinal starting points after scan (m):")
print(start_points_final)