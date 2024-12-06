import numpy as np

asset_a = np.array([100, 101, 102, 103, 104])
asset_b = np.array([100.6, 101.9, 102.5, 103.4, 104.5])
spread = asset_b - asset_a
print(asset_b - asset_a)
print(np.mean(spread))