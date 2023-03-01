from ouster import client
from ouster import pcap
from LIDAR import get_xyz_from_pcap
import numpy as np
import matplotlib.pyplot as plt
import cv2
from helper import normalize

hostname = 'os-122215001365.local'
lidar_port = 7502
imu_port = 7503

meta_path = "berdiri_kanan/OS-1-32-U2_122215001365_1024x10_20221026_162913.json"
pcap_path = "berdiri_kanan/OS-1-32-U2_122215001365_1024x10_20221026_162913.pcap"

# graph xyz
x, y, z = get_xyz_from_pcap(
    frame_num=0,
    pcap_path=pcap_path,
    meta_path=meta_path
)

r = np.sqrt(x**2 + y**2)
rad_alpha = np.arctan2(x, y)
deg_alpha = np.degrees(rad_alpha)

depth = normalize(r)

h_res = 1024
v_res = 32
#
px, py, pz = x, y, z
deg_alpha = normalize(deg_alpha)
pz = normalize(pz)

img_x = np.floor(h_res * deg_alpha / np.max(deg_alpha)).astype(int)
img_y = np.floor(v_res * pz / np.max(pz)).astype(int)
# print("X:",np.min(img_x),np.max(img_x))
# print("Y:",np.min(img_y),np.max(img_y))


img = np.zeros((np.max(img_x), np.max(img_y)))
#
img = depth.reshape(h_res,v_res)
img = img.reshape(v_res,h_res)
img = cv2.resize(img, (h_res, v_res * 5))
#
plt.title("Front View")
plt.imshow(img,cmap='gray')
plt.show()

