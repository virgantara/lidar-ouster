import numpy as np
import copy
import open3d as o3d
from helper import *

pcd = o3d.io.read_point_cloud("20230301/PCD/45Deg/duduk_depan/obj_000000.pcd")
# vis = o3d.visualization.VisualizerWithEditing(-1, False, "")
vis = o3d.visualization.Visualizer()
vis.create_window()
vis.add_geometry(pcd)

# bbox_min = np.array([2,-0.7,-1])
# bbox_max = np.array([4,1,1])
#
# bbox = draw_bounding_box(bbox_min, bbox_max)
# vis.add_geometry(bbox)
opt = vis.get_render_option()
opt.show_coordinate_frame = True
opt.background_color = np.asarray([0.5, 0.5, 0.5])
vis.run()
vis.destroy_window()
# cropped_geometry= vis.get_cropped_geometry()
# o3d.io.write_point_cloud("20230301/PCD/45Deg/berdiri/cropped_000000.pcd", cropped_geometry)