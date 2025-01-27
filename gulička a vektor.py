import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk

# Nastavenia valca
radius = 2.0  # polomer valca
height = 5.0  # výška valca
gulička_rýchlosť = 400 / 3.6  # 400 km/h prepočítané na m/s


def random_unit_vector():
    """Vytvorí náhodný jednotkový vektor pre pohyb guličky."""
    phi = np.random.uniform(0, 2 * np.pi)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

# Počiatočné súradnice guličky
position = np.array([0.0, 0.0, 0.0])
velocity = random_unit_vector() * gulička_rýchlosť  # jednotkový vektor * rýchlosť

# Ukladanie súradníc zrážok
collision_points = []
vektory = []

# Vytvorenie hlavného okna pre logovanie
root = tk.Tk()
root.title("Log vektorov a nárazov")
log = tk.Text(root, bg="white", fg="black", font=("Consolas", 10))
log.pack(fill=tk.BOTH, expand=True)

def log_update(text):
    log.insert(tk.END, text + "\n")
    log.see(tk.END)

# Simulácia pohybu guličky
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Kreslenie valca
z = np.linspace(-height / 2, height / 2, 100)
angle = np.linspace(0, 2 * np.pi, 100)
x = radius * np.cos(angle)
y = radius * np.sin(angle)
for i in z:
    ax.plot(x, y, zs=i, zdir='z', color='lightblue', alpha=0.6)

# Simulácia
for _ in range(1000):
    position += velocity * 0.01  # krok simulácie (časový krok = 0.01 s)

    # Kontrola kolízie s bočnými stenami valca
    radial_distance = np.sqrt(position[0]**2 + position[1]**2)
    if radial_distance >= radius:
        normal = np.array([position[0], position[1], 0]) / radial_distance
        velocity -= 2 * np.dot(velocity, normal) * normal
        position[:2] = normal[:2] * radius
        collision_points.append(position.copy())
        log_update(f"Náraz na bočnú stenu: x={position[0]:.2f}, y={position[1]:.2f}, z={position[2]:.2f}")

    # Kontrola kolízie s hornou alebo dolnou stenou valca
    if position[2] >= height / 2 or position[2] <= -height / 2:
        velocity[2] = -velocity[2]
        position[2] = np.clip(position[2], -height / 2, height / 2)
        collision_points.append(position.copy())
        log_update(f"Náraz na hornú/dolnú stenu: x={position[0]:.2f}, y={position[1]:.2f}, z={position[2]:.2f}")

    # Uloženie aktuálneho vektora
    vektory.append(velocity.copy())
    log_update(f"Vektor rýchlosti: vx={velocity[0]:.2f}, vy={velocity[1]:.2f}, vz={velocity[2]:.2f}")

    # Kreslenie guličky
    ax.cla()
    ax.set_xlim([-radius * 1.5, radius * 1.5])
    ax.set_ylim([-radius * 1.5, radius * 1.5])
    ax.set_zlim([-height / 2 * 1.5, height / 2 * 1.5])
    ax.scatter(position[0], position[1], position[2], color='red', s=50)

    # Prekreslenie valca
    for i in z:
        ax.plot(x, y, zs=i, zdir='z', color='lightblue', alpha=0.6)

    plt.pause(0.01)

plt.show()
root.mainloop()