import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Počiatočné nastavenia
space_size = 5  # Veľkosť priestoru (kocka +- space_size)
num_particles = 20  # Počet častíc
particle_radius = 0.5  # Polomer častíc
initial_speed = 20.0  # Počiatočná rýchlosť častíc

def random_unit_vector():
    """Vytvorí náhodný jednotkový vektor."""
    phi = np.random.uniform(0, 2 * np.pi)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

# Inicializácia polôh a rýchlostí častíc
positions = np.random.uniform(-space_size / 2, space_size / 2, (num_particles, 3))
velocities = np.array([random_unit_vector() * initial_speed for _ in range(num_particles)])

# Ukladanie informácií o zrážkach
collisions = []

# Simulácia
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def update_positions(dt):
    """Aktualizuje polohy a kontroluje zrážky."""
    global positions, velocities, collisions

    # Aktualizácia polohy
    positions += velocities * dt

    # Kontrola zrážok so stenami
    for i in range(num_particles):
        for j in range(3):  # Pre x, y, z osi
            if positions[i, j] - particle_radius <= -space_size / 2 or positions[i, j] + particle_radius >= space_size / 2:
                velocities[i, j] *= -1  # Odrážanie od stien

    # Kontrola zrážok medzi časticami
    for i in range(num_particles):
        for j in range(i + 1, num_particles):
            distance = np.linalg.norm(positions[i] - positions[j])
            if distance <= 2 * particle_radius:  # Zrážka
                # Výpočet novej rýchlosti na základe elastickej zrážky
                normal = (positions[i] - positions[j]) / distance
                relative_velocity = velocities[i] - velocities[j]
                velocities[i] -= np.dot(relative_velocity, normal) * normal
                velocities[j] += np.dot(relative_velocity, normal) * normal

                # Zaznamenanie zrážky
                collisions.append((positions[i].copy(), positions[j].copy()))

# Parametre simulácie
simulation_time = 15  # Celkový čas simulácie (s)
dt = 0.02  # Časový krok

# Animácia
for _ in range(int(simulation_time / dt)):
    ax.cla()
    update_positions(dt)

    # Nastavenie hraníc grafu
    ax.set_xlim([-space_size / 2, space_size / 2])
    ax.set_ylim([-space_size / 2, space_size / 2])
    ax.set_zlim([-space_size / 2, space_size / 2])

    # Kreslenie častíc
    for pos in positions:
        ax.scatter(pos[0], pos[1], pos[2], color='red', s=100)

    # Kreslenie priestoru
    ax.set_box_aspect([1, 1, 1])

    plt.pause(0.01)

plt.show()

# Výstup zrážok
print("Zaznamenané zrážky:")
for collision in collisions:
    print(f"Častica 1: {collision[0]}, Častica 2: {collision[1]}")
