from ouster import client
from ouster import pcap
from LIDAR import get_xyz_from_pcap
import numpy as np
import matplotlib.pyplot as plt
import cv2

hostname = 'os-122215001365.local'
lidar_port = 7502
imu_port = 7503

meta_path = "OS-1-32-U2_122215001365_1024x10_20220929_100745.json"
pcap_path = "OS-1-32-U2_122215001365_1024x10_20220929_100745.pcap"
# precompute xyzlut to save computation in a loop
with open(meta_path, 'r') as f:
    info = client.SensorInfo(f.read())

source = pcap.Pcap(pcap_path, info)
metadata = source.metadata
scans = iter(client.Scans(source))

# scan = next(scans)[0]
scan = next(scans,1)

# graph xyz
x, y, z = get_xyz_from_pcap(pcap_path, meta_path)

r = np.sqrt(x**2 + y**2)
rad_alpha = np.arctan2(x, y)
deg_alpha = np.degrees(rad_alpha)
depth = r * 255 / np.max(r)

h_res = 1024
v_res = 32

img_x = np.floor(h_res * deg_alpha / np.max(deg_alpha)).astype(int)
img_y = np.floor(v_res * z / np.max(z)).astype(int)

img = np.zeros((np.max(img_x), np.max(img_y)))

img = depth.reshape(1024,32)
img = img.reshape(32,1024)
img = cv2.resize(img, (h_res, v_res * 5))

plt.title("Front View")
plt.imshow(img)
plt.show()

