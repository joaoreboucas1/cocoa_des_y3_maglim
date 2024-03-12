# Plot data vector
import numpy as np
from numpy import log10, sqrt
import matplotlib.pyplot as plt

data_vector_file_path = "./Y3_MAGLIM.datavector"
data_vector_full = np.loadtxt(data_vector_file_path, unpack=True, usecols=(1))
len_dv = len(data_vector_full)

cov_file_path = "./Y3_covariance.txt"
cov_data = np.loadtxt(cov_file_path)

errors = np.zeros((len_dv))

# Parsing cov data
for line in cov_data:
    i, j, cov_ij = line
    if int(i) == int(j): errors[int(i)] = sqrt(cov_ij)

angular_bins = 20
min_angle = 2.5 # arcmin
max_angle = 250 # arcmin
angular_bin_limits = np.logspace(log10(min_angle), log10(max_angle), angular_bins + 1)
print(angular_bin_limits)
angles = np.zeros((angular_bins))
for i in range(angular_bins):
    angles[i] = (angular_bin_limits[i+1] + angular_bin_limits[i])/2
redshift_bins_source = 4
redshift_bins_lens = 6

fig, axs = plt.subplots(redshift_bins_source, redshift_bins_source + 2, sharex=True, sharey=True, figsize=(12, 8))
plt.subplots_adjust(wspace=0, hspace=0)

row_col_mapping = {
    (0, 0): 3,
    (1, 0): 2,
    (2, 0): 1,
    (3, 0): 0,
    (0, 1): 6,
    (1, 1): 5,
    (2, 1): 4,
    (0, 2): 8,
    (1, 2): 7,
    (0, 3): 9,
    (0, 5): 10,
    (1, 5): 11,
    (2, 5): 12,
    (3, 5): 13,
    (1, 4): 14,
    (2, 4): 15,
    (3, 4): 16,
    (2, 3): 17,
    (3, 3): 18,
    (3, 2): 19,
}

for row in range(redshift_bins_source):
    for col in range(redshift_bins_source + 2):
        try:
            index = row_col_mapping[(row, col)]
        except KeyError:
            continue
        axs[row, col].scatter(angles, data_vector_full[index*20:(index+1)*20], c='black', s=4)
        axs[row, col].errorbar(angles, data_vector_full[index*20:(index+1)*20], yerr=errors[index*20:(index+1)*20], c='black', fmt='none')
        axs[row, col].set_xscale('log')
        axs[row, col].set_yscale('log')
        axs[row, col].text(100, 5e-5, f"{col + 1}, {4 - row}")
        

axs[0, 0].set_ylim([1e-7, 1e-4])
axs[0, 0].set_xlim([2.4, 251])

for row in range(redshift_bins_source):
    for col in range(redshift_bins_source + 2):
        axs[row, col].tick_params(which="both", direction="in")

for row in range(1, 5):
    col = 4 - row
    axs[col, row].remove()
plt.show()