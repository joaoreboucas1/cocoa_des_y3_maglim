import numpy as np
from numpy import log10

cosmosis_scale_cuts_file = "./y3_linear_scale_cuts.ini"

num_blocks = 50
angular_bins = 20
min_angle = 2.5 # arcmin
max_angle = 250 # arcmin
angular_bin_limits = np.logspace(log10(min_angle), log10(max_angle), angular_bins + 1)
angles = np.zeros((angular_bins))
for i in range(angular_bins):
    angles[i] = (angular_bin_limits[i+1] + angular_bin_limits[i])/2

with open(cosmosis_scale_cuts_file, "r") as f:
	lines = f.read().splitlines()[1:]

mask = []
for i, line in enumerate(lines):
	min_angle = float(line.split()[2])
	mask += [0 if angle < min_angle else 1 for angle in angles]
with open("Y3_LINEAR_mask.txt", "w") as f:
	for i, element in enumerate(mask):
		f.write(f"{i} {element:.1f}\n")

print(f"Elements remaining: {mask.count(1)}")