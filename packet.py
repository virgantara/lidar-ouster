from ouster import client
from ouster import pcap


hostname = 'os-122215001365.local'
lidar_port = 7502
imu_port = 7503

meta_path = "OS-1-32-U2_122215001365_1024x10_20220929_100745.json"
pcap_path = "OS-1-32-U2_122215001365_1024x10_20220929_100745.pcap"

with open(meta_path, 'r') as f:
    info = client.SensorInfo(f.read())

source = pcap.Pcap(pcap_path, info)

for packet in source:
    if isinstance(packet, client.LidarPacket):
        # Now we can process the LidarPacket. In this case, we access
        # the measurement ids, timestamps, and ranges
        measurement_ids = packet.measurement_id
        timestamps = packet.timestamp
        ranges = packet.field(client.ChanField.RANGE)
        print(f'  encoder counts = {measurement_ids.shape}')
        print(f'  timestamps = {timestamps.shape}')
        print(f'  ranges = {ranges.shape}')

    elif isinstance(packet, client.ImuPacket):
        # and access ImuPacket content
        print(f'  acceleration = {packet.accel}')
        print(f'  angular_velocity = {packet.angular_vel}')