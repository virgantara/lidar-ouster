import ouster.sdk.viz
from ouster.sdk import viz
from ouster import client
from ouster import pcap
import matplotlib.pyplot as plt
from contextlib import closing
import cv2
import numpy as np
from LIDAR import startLidar, stopLidar, recordLidar, streamLidar, stream_range_and_reflectivity
from more_itertools import nth
import time

hostname = 'os-122215001365.local'
lidar_port = 7502
imu_port = 7503



# ranges = scan.field(client.ChanField.RANGE)
# destagger ranges, notice `metadata` use, that is needed to get
# sensor intrinsics and correctly data transforms
# ranges_destaggered = client.destagger(source.metadata, ranges)
# ranges_destaggered = (ranges_destaggered / np.max(ranges_destaggered) * 255).astype(np.uint8)
# ranges_destaggered = cv2.resize(ranges_destaggered,(1600, 200))
# plt.imshow(ranges_destaggered, cmap='gray', resample=False)
# plt.show()
# scan = client.LidarScan(
#     info.format.pixels_per_column,
#     info.format.columns_per_frame,
#     info.format.udp_profile_lidar
# )
#
#
# signal = scan.field(client.ChanField.RANGE)
# signal = client.destagger(meta, signal)
# print(signal.shape)


# signal = np.divide(signal, np.amax(signal), dtype=np.float32)
# startLidar(hostname,lidar_port,imu_port)
# stream_range_and_reflectivity()
# Creating a point viz instance

# point_viz = viz.PointViz("Example Viz")
# viz.add_default_controls(point_viz)
# # ... add objects here
# update internal objects buffers and run visualizer
#
# try:
#
#     with closing(client.Scans.stream(hostname, lidar_port, complete=False)) as stream:
#         show = True
#         # while show:
#         for scan in stream:
#             meta = stream.metadata
#             signal = scan.field(client.ChanField.REFLECTIVITY)
#             signal = client.destagger(meta, signal)
#             signal = np.divide(signal, np.amax(signal), dtype=np.float32)
#             xyzlut = client.XYZLut(meta)
#             xyz = xyzlut(scan.field(client.ChanField.RANGE))
#             cloud_xyz = viz.Cloud(xyz.shape[0] * xyz.shape[1])
#             cloud_xyz.set_xyz(np.reshape(xyz, (-1, 3)))
#             cloud_xyz.set_key(signal.ravel())
#             point_viz.add(cloud_xyz)
#             point_viz.update()
#             point_viz.run()
#             # print(meta)
#             # img_aspect = (meta.beam_altitude_angles[0] - meta.beam_altitude_angles[-1]) / 360.0
#             # img_screen_height = 0.4  # [0..2]
#             # img_screen_len = img_screen_height / img_aspect
#             #
#             # # signal adalah citra proyeksi 360 derajat
#             # # signal = client.destagger(stream.metadata, scan.field(client.ChanField.REFLECTIVITY))
#             # # signal = (signal / np.max(signal) * 255).astype(np.uint8)
#             # # signal = cv2.resize(signal, (1800, 250))
#             #
#             # # range adalah citra 2.5-dimensi
#             # range = client.destagger(stream.metadata, scan.field(client.ChanField.RANGE))
#             # range = (range / np.max(range) * 255).astype(np.uint8)
#             # range = cv2.resize(range, (1800, 250))
#             # range_img = viz.Image()
#             # range_img.set_image(range)
#             # range_img.set_position(-img_screen_len / 2, img_screen_len / 2, 1 - img_screen_height, 1)
#             # point_viz.add(range_img)
#
#                 #
#                 # img_vstack = np.vstack((signal, range))
#                 # cv2.imshow("Range & Reflectivity (Press Q to Close)", img_vstack)
#                 # cv2.imshow("scaled reflectivity", range)
#                 # key = cv2.waitKey(1) & 0xFF
#                 # if key & 0xFF == ord('q'):
#                 #     show = False
#                 #     break
#     # cv2.destroyAllWindows()
# except Exception as e:
#     print("Error:", e)



# stopLidar(hostname)

# startLidar(hostname, lidar_port, imu_port)
# streamLidar(hostname, lidar_port)
# stopLidar(hostname)
# recordLidar(hostname, lidar_port, imu_port, 20)