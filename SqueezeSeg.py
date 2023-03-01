from ouster import client
from ouster import pcap
from LIDAR import get_xyz_from_pcap
import numpy as np
import matplotlib.pyplot as plt
import cv2
from helper import normalize

meta_path = "berdiri_kanan/OS-1-32-U2_122215001365_1024x10_20221026_162913.json"
pcap_path = "berdiri_kanan/OS-1-32-U2_122215001365_1024x10_20221026_162913.pcap"
# precompute xyzlut to save computation in a loop

x, y, z = get_xyz_from_pcap(
    frame_num=0,
    pcap_path=pcap_path,
    meta_path=meta_path
)

sqrt = np.sqrt(x**2 + y**2 + z**2)
div_sqrt = np.divide(z, sqrt, out=np.zeros_like(z), where= sqrt != 0)
azimuth = np.arcsin(div_sqrt)


xy_sqrt = np.sqrt(x**2 + y**2)
div_xy = np.divide(y, xy_sqrt, out=np.zeros_like(y), where= xy_sqrt != 0)
zenith = np.arcsin(div_xy)

