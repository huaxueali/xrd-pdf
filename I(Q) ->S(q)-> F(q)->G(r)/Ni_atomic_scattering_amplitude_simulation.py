import numpy as np
import matplotlib.pyplot as plt

# Define the lattice constant and size of the lattice
a = 3.48  # in Angstrom
n_max = 4  # Size of the lattice (from 0 to n_max in each dimension)

# Define the range of scattering vector Q
Q_values = np.linspace(1, 20, 1000)  # From 1 to 20, sampled at 100 points

# Define the parameters for the atomic form factor f(Q) for Ni
# The atomic form factors were taken from the International Tables for Crystallography: http://it.iucr.org/Cb/ch6o1v0001/.
a_values = [12.8376, 7.292, 4.4438, 2.38]
b_values = [3.8785, 0.2565, 12.1763, 66.3421]
c = 1.0341


# Define the atomic form factor function
def f_G(G):
    sum_terms = sum(a * np.exp(-b * (G / (4 * np.pi)) ** 2) for a, b in zip(a_values, b_values))
    return sum_terms + c

# Initialize the scattering amplitude psi(Q) to zero
psi_values_fQ = np.zeros(len(Q_values), dtype=complex)

# Loop over all atoms in the lattice
for n1 in range(n_max + 1):
    for n2 in range(n_max + 1):
        for n3 in range(n_max + 1):
            r = np.array([n1, n2, n3]) * a  # Position vector of the atom
            for i, Q in enumerate(Q_values):
                Q_vec = np.array([Q, 0, 0])  # We consider Q along x-axis for simplicity
                # Calculate the contribution of this atom to psi(Q)
                psi_i = f_G(Q) * np.exp(1j * np.dot(Q_vec, r))
                psi_values_fQ[i] += psi_i

# Calculate the magnitude of psi(Q) for plotting
psi_magnitude_fQ = np.abs(psi_values_fQ)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(Q_values, psi_magnitude_fQ, label='|ψ(Q)| with f(Q)')
plt.title('Scattering Amplitude |ψ(Q)| for a Simple Cubic Lattice of Ni atoms')
plt.xlabel('Scattering Vector Magnitude Q')
plt.ylabel('|ψ(Q)|')
plt.grid(True)
plt.legend()
plt.show()
