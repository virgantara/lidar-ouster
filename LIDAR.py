from ouster import client
from ouster.sdk import viz
from ouster import pcap
from contextlib import closing
from more_itertools import time_limited
from datetime import datetime
import cv2
import numpy as np
from more_itertools import nth

hostname = 'os-122215001365.local'
lidar_port = 7502
imu_port = 7503

def read_sensor_status(hostname):
    try:
        with closing(client.Sensor(hostname)) as source:
            # print some useful info from
            print("Retrieved metadata:")
            print(f"  serial no:        {source.metadata.sn}")
            print(f"  firmware version: {source.metadata.fw_rev}")
            print(f"  product line:     {source.metadata.prod_line}")
            print(f"  lidar mode:       {source.metadata.mode}")
            print(f"Writing to: {hostname}.json")

            # write metadata to disk
            source.write_metadata(f"{hostname}.json")
    except Exception as e:
        print("Error:",e)
def startLidar(hostname,lidar_port, imu_port, azimuth_start=0, azimuth_end=360000):
    config = client.SensorConfig()
    config.lidar_mode = client.LidarMode.MODE_2048x10
    config.azimuth_window = (azimuth_start, azimuth_end)
    config.udp_port_lidar = lidar_port
    config.udp_port_imu = imu_port
    config.operating_mode = client.OperatingMode.OPERATING_NORMAL
    client.set_config(hostname, config, persist=True, udp_dest_auto=True)

def stopLidar(hostname):
    config = client.SensorConfig()
    config.operating_mode = client.OperatingMode.OPERATING_STANDBY
    client.set_config(hostname, config, persist=True, udp_dest_auto=True)


def recordLidar(dir, hostname, lidar_port, imu_port, record_duration=1):

    with closing(client.Sensor(hostname, lidar_port, imu_port, buf_size=640)) as source:

        time_part = datetime.now().strftime("%Y%m%d_%H%M%S")
        print("Start Recording")
        meta = source.metadata
        fname_base = f"{meta.prod_line}_{meta.sn}_{meta.mode}_{time_part}"
        #
        print(f"Saving sensor metadata to: {fname_base}.json")

        fpath = dir+'/'+fname_base
        source.write_metadata(f"{fpath}.json")

        print(f"Writing to: {fname_base}.pcap (Ctrl-C to stop early)")
        source_it = time_limited(record_duration, source)

        n_packets = pcap.record(source_it, f"{fpath}.pcap")
        print(f"Captured {n_packets} packets")

def streamLidar(hostname, lidar_port):

    # kode ini untuk membaca status LIDAR saat kondisi NORMAL
    # komen kode ini jika tidak diperlukan
    # read_sensor_status(hostname)
    with closing(client.Scans.stream(hostname, lidar_port,complete=False)) as stream:
        show = True
        while show:
            for scan in stream:
                reflectivity = client.destagger(stream.metadata, scan.field(client.ChanField.REFLECTIVITY))
                reflectivity = (reflectivity / np.max(reflectivity) * 255).astype(np.uint8)
                reflectivity = cv2.resize(reflectivity, (1800, 250))
                cv2.imshow("scaled reflectivity", reflectivity)
                key = cv2.waitKey(1) & 0xFF
                if key & 0xFF == ord('q'):
                    show = False
                    break
    cv2.destroyAllWindows()

def stream_range_and_reflectivity(hostname, lidar_port):
    try:
        with closing(client.Scans.stream(hostname, lidar_port, complete=False)) as stream:
            show = True
            while show:
                for scan in stream:

                    # signal adalah citra proyeksi 360 derajat
                    signal = client.destagger(stream.metadata, scan.field(client.ChanField.REFLECTIVITY))
                    signal = (signal / np.max(signal) * 255).astype(np.uint8)
                    signal = cv2.resize(signal, (1800, 250))

                    # range adalah citra 2.5-dimensi
                    range = client.destagger(stream.metadata, scan.field(client.ChanField.RANGE))
                    range = (range / np.max(range) * 255).astype(np.uint8)
                    range = cv2.resize(range, (1800, 250))
                    img_vstack = np.vstack((signal, range))
                    cv2.imshow("Range & Reflectivity (Press Q to Close)", img_vstack)
                    # cv2.imshow("scaled reflectivity", range)
                    key = cv2.waitKey(1) & 0xFF
                    if key & 0xFF == ord('q'):
                        show = False
                        break
        cv2.destroyAllWindows()
    except Exception as e:
        print("Error:",e)

def display_recorded(pcap_path, meta_path):
    with open(meta_path, 'r') as f:
        info = client.SensorInfo(f.read())


    source = pcap.Pcap(pcap_path, info)
    meta = source.metadata
    scans = client.Scans(source)
    # iterate `scans` and get the 84th LidarScan (it can be different with your data)
    # Creating a point viz instance

    point_viz = viz.PointViz("Example Viz")
    viz.add_default_controls(point_viz)

    # ... add objects here
    scan = nth(scans, 0)
    signal = scan.field(client.ChanField.REFLECTIVITY)

    signal = client.destagger(meta, signal)

    signal = np.divide(signal, np.amax(signal), dtype=np.float32)

    rng = client.destagger(meta, scan.field(client.ChanField.RANGE))
    rng = (rng / np.max(rng) * 255).astype(np.uint8)
    # rng = cv2.resize(rng, (1800, 250))

    cv2.imwrite("rng.jpg", rng)

    cloud_scan = viz.Cloud(meta)
    cloud_scan.set_range(scan.field(client.ChanField.RANGE))
    cloud_scan.set_key(signal)
    point_viz.add(cloud_scan)
    point_viz.update()
    point_viz.run()


def get_range(pcap_path, meta_path):
    with open(meta_path, 'r') as f:
        info = client.SensorInfo(f.read())

    source = pcap.Pcap(pcap_path, info)
    meta = source.metadata
    scans = client.Scans(source)
    # iterate `scans` and get the 84th LidarScan (it can be different with your data)

    print(scans)
    scan = nth(scans, 0)


    rng = client.destagger(meta, scan.field(client.ChanField.RANGE))
    rng = (rng / np.max(rng) * 255).astype(np.uint8)
    # rng = cv2.resize(rng, (1800, 250))

    cv2.imwrite("rng.jpg", rng)

    return rng
def get_xyz_from_pcap(frame_num=0, pcap_path='', meta_path=''):
    with open(meta_path, 'r') as f:
        info = client.SensorInfo(f.read())

    source = pcap.Pcap(pcap_path, info)
    metadata = source.metadata
    scans = iter(client.Scans(source))
    # get single scan
    # metadata, scans = client.Scans.sample(hostname, 1, lidar_port)
    # scan = next(scans)[0]

    scan = next(scans, frame_num)

    # [doc-stag-plot-xyz-points]
    # transform data to 3d points
    xyzlut = client.XYZLut(metadata)
    xyz = xyzlut(scan.field(client.ChanField.RANGE))
    # [doc-etag-plot-xyz-points]

    # graph xyz
    [x, y, z] = [c.flatten() for c in np.dsplit(xyz, 3)]

    return x, y, z