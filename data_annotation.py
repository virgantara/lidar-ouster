from helper import *
from pathlib import Path

for folder in sorted(Path('20230301/PCD/45Deg').iterdir()):
    folder_name = Path(folder).stem
    for subfolder in sorted(Path(folder).iterdir()):
        tmp = Path(subfolder).stem
        if not os.path.exists("20230301/PCD_Cropped/"):
            os.makedirs("20230301/PCD_Cropped/")

        if not os.path.exists("20230301/PCD_Cropped/45Deg/"):
            os.makedirs("20230301/PCD_Cropped/45Deg/")

        if not os.path.exists("20230301/PCD_Cropped/45Deg/"+folder_name):
            os.makedirs("20230301/PCD_Cropped/45Deg/"+folder_name)


        pcd = o3d.io.read_point_cloud("20230301/PCD/45Deg/"+folder_name+"/"+tmp+".pcd")

        bbox_min = np.array([2, -1.6, -1])
        bbox_max = np.array([4, 1.8, 1])

        # bbox_min = np.array([2,-0.7,-1])
        # bbox_max = np.array([4,1,1])

        bbox = o3d.geometry.AxisAlignedBoundingBox()
        bbox.color = np.array([1,0,0])
        bbox.min_bound = bbox_min
        bbox.max_bound = bbox_max

        crop_pcd = pcd.crop(bbox)
        file_output_path = "20230301/PCD_Cropped/45Deg/"+str(folder_name)+"/cropped_"+tmp+".pcd"
        print("Writing " + folder_name + " PCD to " + file_output_path)
        o3d.io.write_point_cloud(file_output_path, crop_pcd)
        # exit(0)
# vis.add_geometry(crop_pcd)
# opt = vis.get_render_option()
# opt.show_coordinate_frame = True
# opt.background_color = np.asarray([0.5, 0.5, 0.5])
# vis.run()
# vis.destroy_window()
# cropped_geometry= vis.get_cropped_geometry()
# o3d.io.write_point_cloud("20230301/PCD/45Deg/berdiri/cropped_000000.pcd", cropped_geometry)