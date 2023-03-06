from helper import *
from pathlib import Path
import shutil

output_folder = "hands_up"

if not os.path.exists("20230301/PCD_Cropped/merged_half/"):
    os.makedirs("20230301/PCD_Cropped/merged_half/")

if not os.path.exists("20230301/PCD_Cropped/merged_half/"+output_folder):
    os.makedirs("20230301/PCD_Cropped/merged_half/"+output_folder)

counter = 0

BASE_OUTPUT_PATH = "20230301/PCD_Cropped/merged_half/"+output_folder

for folder in Path('20230301/PCD/45Deg').rglob("tangan_atas*"):
    tmp = Path(folder).stem
    # print(folder, tmp)

    for f in Path(folder).rglob('*.pcd'):
        counter = counter + 1
        # file_name = Path(f).stem
        base, extension = os.path.splitext(f)
        f_output_name = BASE_OUTPUT_PATH + "/" +str(counter) + extension
        print("Copying PCD to: ", f_output_name)
        shutil.copy(f, f_output_name)
        # if not os.path.exists("20230301/PCD/"):
        #     os.makedirs("20230301/PCD/")
        #
        # if not os.path.exists("20230301/PCD/45Deg/"):
        #     os.makedirs("20230301/PCD/45Deg/")
        #
        # if not os.path.exists("20230301/PCD/45Deg/"+tmp):
        #     os.makedirs("20230301/PCD/45Deg/"+tmp)
        #
        # write_path = "20230301/PCD/45Deg/"+str(tmp)

