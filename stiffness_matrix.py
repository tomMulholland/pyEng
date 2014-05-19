import numpy as np

# for XXXXXXX
# glass fiber reinforced polypropylene
# in this case, principle direction is y
# Equations for ORTHOTROPIC MATERIALS
E1 = 9929.68e6
E2 = E3 = 1819.86e6
rho = 1.22
nu_12 = nu_13 = 0.35
nu_23 = 0.4500488
G12 = 2199.093e6
G13 = G12
G23 = E2 / (2 * (1 + nu_23))
nu_21 = nu_12 * (E2 / E1)1
nu_31 = nu_13 * (E3 / E1)
nu_32 = nu_23 * (E3 / E2)


# matrix elements
S11 = 1 / E1
S12 = -nu_21 / E2
S13 = -nu_31 / E3
S21 = -nu_12 / E1
S22 = 1 / E2
S23 = -nu_32 / E3
S31 = -nu_13 / E1
S32 = -nu_23 / E2
S33 = 1 / E3
S44 = 1 / G23
S55 = 1 / G13
S66 = 1 / G12

elasticity_matrix = np.array([[S11, S12, S13,  0,   0,   0],
                              [S12, S22, S23,  0,   0,   0],
                              [S13, S23, S33,  0,   0,   0],
                              [0,   0,   0,  S44,   0,   0],
                              [0,   0,   0,    0, S55,   0],
                              [0,   0,   0,    0,   0, S66]])

# Stresses
sigma_11 = 20e6
sigma_22 = 5e6
sigma_33 = sigma_23 = sigma_31 = sigma_12 = 0

stress_matrix = np.array([sigma_11, sigma_22, sigma_33, sigma_23, sigma_31, sigma_12])
stress_matrix = np.resize(stress_matrix, (6, 1))

strain_matrix = np.dot(elasticity_matrix, stress_matrix)
eps_11 = strain_matrix[0]
eps_22 = strain_matrix[1]
eps_33 = strain_matrix[2]
eps_23 = strain_matrix[3]
eps_31 = strain_matrix[4]
eps_12 = strain_matrix[5]

# strain_matrix = np.array([eps_11, eps_22, eps_33, eps_23, eps_31, eps_12])
# strain_matrix = np.resize(strain_matrix, (6, 1))


