from ouster import client
from ouster import pcap
from LIDAR import get_xyz_from_pcap
import numpy as np
import matplotlib.pyplot as plt
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
# get single scan
# metadata, scans = client.Scans.sample(hostname, 1, lidar_port)
# scan = next(scans)[0]

scan = next(scans,1)

# set up figure


plt.title("3D Points from {}".format(hostname))

# graph xyz
x, y, z = get_xyz_from_pcap(pcap_path, meta_path)
# plt.figure()
ax = plt.axes(projection='3d')
r = 3
ax.set_xlim3d([-r, r])
ax.set_ylim3d([-r, r])
ax.set_zlim3d([-r, r])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.scatter(x, y, z, c=z / max(z), s=0.2)
plt.show()