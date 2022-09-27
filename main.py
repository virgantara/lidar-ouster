from ouster import client
from ouster import pcap
from contextlib import closing
from more_itertools import time_limited
from datetime import datetime
import cv2
import numpy as np

hostname = 'os-122215001365.local'
lidar_port = 7502
imu_port = 7503

def startLidar(hostname):
    config = client.SensorConfig()
    config.lidar_mode = client.LidarMode.MODE_1024x10
    config.udp_port_lidar = 7502
    config.udp_port_imu = 7503
    config.operating_mode = client.OperatingMode.OPERATING_NORMAL
    client.set_config(hostname, config, persist=True, udp_dest_auto=True)

def setStanbyLidar(hostname):
    config = client.SensorConfig()
    config.operating_mode = client.OperatingMode.OPERATING_STANDBY
    client.set_config(hostname, config, persist=True, udp_dest_auto=True)

# with closing(client.Sensor(hostname)) as source:
#     # print some useful info from
#     print("Retrieved metadata:")
#     print(f"  serial no:        {source.metadata.sn}")
#     print(f"  firmware version: {source.metadata.fw_rev}")
#     print(f"  product line:     {source.metadata.prod_line}")
#     print(f"  lidar mode:       {source.metadata.mode}")
#     print(f"Writing to: {hostname}.json")
#
#     # write metadata to disk
#     source.write_metadata(f"{hostname}.json")
def recordLidar(hostname, lidar_port, imu_port, record_duration=1):

    with closing(client.Sensor(hostname, lidar_port, imu_port, buf_size=640)) as source:

        time_part = datetime.now().strftime("%Y%m%d_%H%M%S")

        meta = source.metadata
        fname_base = f"{meta.prod_line}_{meta.sn}_{meta.mode}_{time_part}"

        print(f"Saving sensor metadata to: {fname_base}.json")
        source.write_metadata(f"{fname_base}.json")

        print(f"Writing to: {fname_base}.pcap (Ctrl-C to stop early)")
        source_it = time_limited(record_duration, source)

        n_packets = pcap.record(source_it, f"{fname_base}.pcap")
        print(f"Captured {n_packets} packets")

def streamLidar(hostname, lidar_port):
    with closing(client.Scans.stream(hostname, lidar_port,complete=False)) as stream:
        show = True
        while show:
            for scan in stream:
                reflectivity = client.destagger(stream.metadata,
                                                scan.field(client.ChanField.REFLECTIVITY))

                reflectivity = (reflectivity / np.max(reflectivity) * 255).astype(np.uint8)
                print(reflectivity.shape)
                reflectivity = cv2.resize(reflectivity, (1800, 250))
                cv2.imshow("scaled reflectivity", reflectivity)
                key = cv2.waitKey(1) & 0xFF
                if key & 0xFF == ord('q'):
                    show = False
                    break
    cv2.destroyAllWindows()

startLidar(hostname)
streamLidar(hostname, lidar_port)
setStanbyLidar(hostname)
# recordLidar(hostname, lidar_port, imu_port)