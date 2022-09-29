### Device Information
- Model: OS-1-32-U2
- Channel: 32
- Horizontal resolution: 512, 1024 (default), 2048
- Range: 120 m
- Vertical FOV: 45° (±22.5º)
- Points per second: 655.360
- Precision: ±0.7 – 5 cm

### Requirements
- Python >= 3.7 and pip >= 19.0
- Linux distribution x86_64 and ARM64 platforms
- Windows 10 x86_64 
- macOS >= 10.13 on x86_64 platforms (macosx_10_13_x86_64)
- macOS >= 11.0 on Apple M1 for Python >= 3.8 (macosx_11_0_arm64)
### Instalasi

```commandline
pip install ouster-sdk
```

### LiDAR OUSTER SETUP

Di project ini ada satu file main.py yang isinya beberapa fungsi berikut:
1. startLidar -- berfungsi untuk mengubah mode LIDAR ke NORMAL
2. stopLidar -- berfungsi untuk mengubah mode LIDAR ke STANDBY (5 Watt)
3. recordLidar -- berfungsi untuk merekam data selama beberapa waktu dalam satuan detik dan disimpan dalam format pcap
4. streamLidar -- berfungsi untuk streaming LIDAR

### Referensi:
- [Quickstart](https://static.ouster.dev/sdk-docs/python/quickstart.html)
- [PointViz Tutorial](https://static.ouster.dev/sdk-docs/python/viz/viz-api-tutorial.html#structured-point-cloud)
- [LidarScan API](https://static.ouster.dev/sdk-docs/reference/lidar-scan.html)

### Misc
- [PointViz Threading for Real-time visualization](https://github.com/ouster-lidar/ouster_example/blob/master/python/src/ouster/sdk/viz.py)