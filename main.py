import ouster.sdk.viz
import os
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
from helper import *
import glob
from pathlib import Path

hostname = 'os-122215001365.local'
lidar_port = 7502
imu_port = 7503

from itertools import islice
def showPoints():
    csv_dir = "csv"
    csv_base = "test"
    csv_ext = "csv"
    meta_path = "OS-1-32-U2_122215001365_1024x10_20220929_100745.json"
    pcap_path = "OS-1-32-U2_122215001365_1024x10_20220929_100745.pcap"
    # precompute xyzlut to save computation in a loop
    with open(meta_path, 'r') as f:
        info = client.SensorInfo(f.read())

    source = pcap.Pcap(pcap_path, info)
    metadata = source.metadata
    print(info)
    xyzlut = client.XYZLut(metadata)
    # create an iterator of LidarScans from pcap and bound it if num is specified
    scans = iter(client.Scans(source))
    # if num:
    #     scans = islice(scans, num)
    counter=0
    for idx, scan in enumerate(scans):
        # initialize the field names for csv header
        counter += 1
        # if not field_names or not field_fmts:
        #     field_names, field_fmts = get_fields_info(scan)

        # copy per-column timestamps for each channel
        timestamps = np.tile(scan.timestamp, (scan.h, 1))
        # grab channel data
        fields_values = [scan.field(ch) for ch in scan.fields]

        # use integer mm to avoid loss of precision casting timestamps
        xyz = (xyzlut(scan.field(client.ChanField.RANGE)) * 1000).astype(np.int64)


        # get all data as one H x W x num fields int64 array for savetxt()
        frame = np.dstack((timestamps, *fields_values, xyz))


        # not necessary, but output points in "image" vs. staggered order
        frame = client.destagger(metadata, frame)
        # print(xyz)
        print(xyz.shape)
        # print(np.array(fields_values).shape)
        # write csv out to file

        # csv_path = os.path.join(csv_dir, f'{csv_base}_{idx:06d}.{csv_ext}')
        # print(f'write frame #{idx}, to file: {csv_path}')
        # header = '\n'.join([f'frame num: {idx}', field_names])
        #x
        # np.savetxt(csv_path, frame.reshape(-1, frame.shape[2]), fmt=field_fmts,delimiter=',',header=header)
# print("Total",counter)
# startLidar(hostname, lidar_port, imu_port,azimuth_start=90000, azimuth_end=270000)
# streamLidar(hostname, lidar_port)
# stopLidar(hostname)
#
# dataset_type = "HumanMovement"
# if not os.path.exists("20230301/45Deg/"+dataset_type):
#     os.mkdir("20230301/45Deg/"+dataset_type)
#
# label = 'WalkingCrouchSideLeft'
# if not os.path.exists("20230301/45Deg/"+dataset_type+"/"+label):
#     os.mkdir("20230301/45Deg/"+dataset_type+"/"+label)
#
# recordLidar('20230301/45Deg/'+dataset_type+'/'+label,hostname, lidar_port, imu_port, 15)

for folder in Path('20230301/45Deg/Pose').iterdir():
    tmp = Path(folder).stem
    # print(folder, tmp)

    for subfolder in Path(folder).rglob('*.json'):
        meta_file = Path(subfolder).stem
        f = os.path.join(folder, meta_file)
        meta_path = f+".json"
        pcap_path = f+".pcap"
        with open(meta_path, 'r') as f:
            info = client.SensorInfo(f.read())

        source = pcap.Pcap(pcap_path, info)
        meta = source.metadata
        scans = client.Scans(source)
        if not os.path.exists("20230301/PCD/"):
            os.makedirs("20230301/PCD/")

        if not os.path.exists("20230301/PCD/45Deg/"):
            os.makedirs("20230301/PCD/45Deg/")

        if not os.path.exists("20230301/PCD/45Deg/"+tmp):
            os.makedirs("20230301/PCD/45Deg/"+tmp)

        write_path = "20230301/PCD/45Deg/"+str(tmp)
        print("Writing PCD to: ",write_path)
        pcap_to_pcd(source=source,metadata=meta, pcd_base=write_path+"/obj")