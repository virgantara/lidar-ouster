from LIDAR import display_recorded, get_range
import matplotlib.pyplot as plt
import numpy as np
import cv2
from ouster import client
from more_itertools import nth
from ouster import pcap
meta_path = "orang/tangan_samping/OS-1-32-U2_122215001365_1024x10_20221026_164244.json"
pcap_path = "orang/tangan_samping/OS-1-32-U2_122215001365_1024x10_20221026_164244.pcap"
#
# display_recorded(pcap_path=pcap_path,meta_path=meta_path)
with open(meta_path, 'r') as f:
    info = client.SensorInfo(f.read())

source = pcap.Pcap(pcap_path, info)
meta = source.metadata
scans = client.Scans(source)

print(scans)
scan = nth(scans, 0)

i = 0
for scan in scans:
    rng = client.destagger(meta, scan.field(client.ChanField.RANGE))
    rng = (rng / np.max(rng) * 255).astype(np.uint8)
# rng = cv2.resize(rng, (1800, 250))
    i = i + 1
    cv2.imwrite("orang/tangan_samping_"+str(i)+".jpg", rng)
# img = get_range(pcap_path=pcap_path,meta_path=meta_path)
#
# plt.imshow(img,cmap='gray')
# plt.show()