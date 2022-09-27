from ouster.sdk import viz
from ouster import client
from contextlib import closing
import cv2
import numpy as np
from LIDAR import startLidar, stopLidar, recordLidar, streamLidar,stream_range_and_reflectivity
from more_itertools import nth

hostname = 'os-122215001365.local'
lidar_port = 7502
imu_port = 7503

stream_range_and_reflectivity(hostname, lidar_port)


# startLidar(hostname, lidar_port, imu_port)
# streamLidar(hostname, lidar_port)
# stopLidar(hostname)
# recordLidar(hostname, lidar_port, imu_port)