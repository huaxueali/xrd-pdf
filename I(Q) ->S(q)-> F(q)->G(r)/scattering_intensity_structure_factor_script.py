
import numpy as np
import matplotlib.pyplot as plt

# Define constants
a = 3.48  # Lattice constant in Angstrom
n_max = 4  # Number of unit cells along each dimension in the cubic lattice
Q_min = 1.0  # Minimum value of the scattering vector
Q_max = 20.0  # Maximum value of the scattering vector
Q_values = np.linspace(Q_min, Q_max, 500)  # Scattering vector magnitudes

# Define atomic form factor for Ni as a function of the scattering vector magnitude Q
def f_G(Q):
    a1, b1 = 12.8376, 3.8785
    a2, b2 = 7.292, 0.2565
    a3, b3 = 4.4438, 12.1763
    a4, b4 = 2.38, 66.3421
    c = 1.0341
    return a1 * np.exp(-b1 * (Q / 4 / np.pi)**2) + a2 * np.exp(-b2 * (Q / 4 / np.pi)**2) + a3 * np.exp(-b3 * (Q / 4 / np.pi)**2) + a4 * np.exp(-b4 * (Q / 4 / np.pi)**2) + c

# Initialize the average coherent scattering intensity I_c_avg to zero
I_c_avg_values = np.zeros(len(Q_values), dtype=complex)

# Loop over all pairs of atoms in the lattice to calculate I_c_avg
for n1_i in range(n_max + 1):
    for n2_i in range(n_max + 1):
        for n3_i in range(n_max + 1):
            r_i = np.array([n1_i, n2_i, n3_i]) * a  # Position vector of the i-th atom
            f_i_values = np.array([f_G(Q) for Q in Q_values])
            
            for n1_j in range(n_max + 1):
                for n2_j in range(n_max + 1):
                    for n3_j in range(n_max + 1):
                        r_j = np.array([n1_j, n2_j, n3_j]) * a  # Position vector of the j-th atom
                        r_ij = np.linalg.norm(r_i - r_j)  # Magnitude of the vector r_ij
                        
                        f_j_values = np.conjugate(f_i_values)  # f_j^* is the complex conjugate of f_i
                        
                        for i, Q in enumerate(Q_values):
                            # Calculate the spherical Bessel function part
                            bessel_part = np.sin(Q * r_ij) / (Q * r_ij) if r_ij != 0 else 1.0  # Handle the r_ij = 0 case
                            # Calculate the contribution to I_c_avg
                            I_c_avg_values[i] += f_j_values[i] * f_i_values[i] * bessel_part

# Calculate the magnitude of I_c_avg for plotting
I_c_avg_magnitude = np.abs(I_c_avg_values)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(Q_values, I_c_avg_magnitude, label='$I_{c, \mathrm{avg}}$')
plt.title('Average Coherent Scattering Intensity $I_{c, \mathrm{avg}}$ for a 5x5x5 Lattice of Ni atoms')
plt.xlabel('Scattering Vector Magnitude Q')
plt.ylabel('$I_{c, \mathrm{avg}}$')
plt.grid(True)
plt.legend()
plt.show()
