
import numpy as np
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt

# Atomic form factor calculation for Ni
def f_G(Q):
    a1, b1 = 12.8376, 3.8785
    a2, b2 = 7.292, 0.2565
    a3, b3 = 4.4438, 12.1763
    a4, b4 = 2.38, 66.3421
    c = 1.0341
    return a1 * np.exp(-b1 * (Q / 4 / np.pi)**2) + a2 * np.exp(-b2 * (Q / 4 / np.pi)**2) + a3 * np.exp(-b3 * (Q / 4 / np.pi)**2) + a4 * np.exp(-b4 * (Q / 4 / np.pi)**2) + c

# Prepare the Q and r arrays for FFT
Q_max = 20
Q_min = 1
delta_Q = 0.05
Q_values = np.arange(Q_min, Q_max, delta_Q)

# Parameters
n_max = 4  # Size of the lattice
a = 3.48  # Lattice constant in Angstrom
N = (n_max + 1)**3  # Total number of atoms

# Initialize list to store the distances r_ij and corresponding f_i and f_j values
r_values = []
f_values = []

# Loop over all pairs of atoms in the lattice to populate r_values and f_values
for n1_i in range(n_max + 1):
    for n2_i in range(n_max + 1):
        for n3_i in range(n_max + 1):
            r_i = np.array([n1_i, n2_i, n3_i]) * a  # Position vector of the i-th atom
            f_i = f_G(np.linalg.norm(Q_values))
            for n1_j in range(n_max + 1):
                for n2_j in range(n_max + 1):
                    for n3_j in range(n_max + 1):
                        if n1_i == n1_j and n2_i == n2_j and n3_i == n3_j:
                            continue  # Skip the i = j case
                        r_j = np.array([n1_j, n2_j, n3_j]) * a  # Position vector of the j-th atom
                        r_ij = np.linalg.norm(r_i - r_j)  # Magnitude of the vector r_ij
                        f_j = f_G(np.linalg.norm(Q_values))
                        r_values.append(r_ij)
                        f_values.append(f_j)

# Convert to numpy arrays for easier manipulation
r_values = np.array(r_values)
f_values = np.array(f_values)

# Calculate F(Q)
F_Q_values = np.array([(1 / N) * np.sum(f * np.sin(Q * r) / (Q * r)) for f, r, Q in zip(f_values, r_values, Q_values)])

# Use FFT to calculate F(r)
F_r_values_fft = ifft(F_Q_values) * len(Q_values) * delta_Q

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(Q_values, np.abs(F_r_values_fft), label='$\mathcal{F}(r)$ using FFT')
plt.title('Fourier Transform $\mathcal{F}(r)$')
plt.xlabel('Distance r (Angstrom)')
plt.ylabel('$\mathcal{F}(r)$')
plt.grid(True)
plt.legend()
plt.show()
