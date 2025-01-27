import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Fyzikálne konštanty
R = 8.314  # Univerzálna plynová konštanta (J/(mol·K))
Avogadro = 6.022e23  # Avogadrova konštanta (molekuly/mol)
energy_per_fusion = 5.6e-13  # Energia uvoľněná pri jednej fúzi (J)

# Počiatočné podmienky
initial_volume = 1e-3  # m^3 (1 liter)
initial_temperature = 300  # K (izbová teplota)
initial_pressure = 101325  # Pa (atmosférický tlak)
molecular_mass_deuterium = 2.014 / 1000  # kg/mol
n_moles = 0.01  # Počet molov deutéria

# Simulačné parametre
k = 0.1  # Rýchlosť exponenciálneho zmenšovania objemu
simulation_time = 10  # Celkový čas simulácie (s)
time_steps = 200  # Počet krokov simulácie
time = np.linspace(0, simulation_time, time_steps)

# Inicializácia premenných
volumes = initial_volume * np.exp(-k * time)
temperatures = np.zeros_like(time)
pressures = np.zeros_like(time)
energy_released = np.zeros_like(time)
molecule_positions = []  # Na uloženie pozícií molekúl

# Počiatočné hodnoty
temperatures[0] = initial_temperature
pressures[0] = (n_moles * R * initial_temperature) / initial_volume

# Generovanie náhodných počiatočných pozícií molekúl (zmenšený počet na vizualizáciu)
sample_molecules = 10000  # Počet molekúl pre simuláciu
molecule_positions.append(np.random.rand(sample_molecules, 3) * initial_volume**(1/3))

# Výpočet simulácie
for i in range(1, time_steps):
    # Aktualizácia tlaku podľa stavovej rovnice ideálneho plynu
    pressures[i] = (n_moles * R * temperatures[i-1]) / volumes[i]

    # Aktualizácia teploty podľa adiabatického stlačenia (približne)
    temperatures[i] = temperatures[i-1] * (volumes[i-1] / volumes[i])**(1.4 - 1)  # pre γ = 1.4 (pre dvojatómové plyny)

    # Ak teplota prekročí prah pre fúziu, vypočíta sa energia
    if temperatures[i] > 1e7:  # Prahová teplota pre fúziu
        # Hustota molekúl deutéria
        number_density = (n_moles * Avogadro) / volumes[i]  # molekuly/m^3

        # Pravdepodobný počet fúzvoch reakcií
        fusion_rate = (number_density**2) * 1e-24  # Jednoduchá aproximácia (m^3/s)
        energy_released[i] = fusion_rate * energy_per_fusion * (time[1] - time[0])

    # Aktualizácia pozícií molekúl (približná simulácia pohybu)
    molecule_positions.append(
        molecule_positions[-1] * (volumes[i] / volumes[i-1])**(1/3)
    )

# Kumulatívna energia
cumulative_energy = np.cumsum(energy_released)

# 3D Vizualizácia
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# Vizualizácia počiatočných a finálnych pozícií molekúl
ax.scatter(
    molecule_positions[0][:, 0], 
    molecule_positions[0][:, 1], 
    molecule_positions[0][:, 2], 
    color='blue', alpha=0.3, label='Počiatočná distribúcia'
)
ax.scatter(
    molecule_positions[-1][:, 0], 
    molecule_positions[-1][:, 1], 
    molecule_positions[-1][:, 2], 
    color='red', alpha=0.6, label='Finálna distribúcia'
)

# Nastavenie grafu
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Simulácia molekulárneho pohybu deutéria")
ax.legend()
plt.show()

# Grafy
plt.figure(figsize=(12, 8))

# Teplota v čase
plt.subplot(3, 1, 1)
plt.plot(time, temperatures, label="Teplota (K)", color="red")
plt.axhline(1e7, color="black", linestyle="--", label="Prah fúzie (10^7 K)")
plt.xlabel("Čas (s)")
plt.ylabel("Teplota (K)")
plt.legend()
plt.grid()

# Tlak v čase
plt.subplot(3, 1, 2)
plt.plot(time, pressures, label="Tlak (Pa)", color="blue")
plt.xlabel("Čas (s)")
plt.ylabel("Tlak (Pa)")
plt.legend()
plt.grid()

# Uvoľněná energia v čase
plt.subplot(3, 1, 3)
plt.plot(time, cumulative_energy, label="Kumulatívna energia (J)", color="green")
plt.xlabel("Čas (s)")
plt.ylabel("Energia (J)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
