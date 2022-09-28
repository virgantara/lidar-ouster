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