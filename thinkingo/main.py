import threading
import sys

sys.path.append(".")
from data_source import Source
from data_class import Data

from monitoring import Monitoring
from car_platform import CarPlatform
from sign_cam import SignCam
from planner import MotionPlanner
from control import Control


def main():
    # global data
    database = Data()
    database.start_from_main_flag = True
    
    """
    test from keyboard input
    """
    database.start_from_main_flag = False

    # sensor data
    data_source = Source(database)
    lidar_source_thread = threading.Thread(target=data_source.lidar_stream_main)
    left_cam_source_thread = threading.Thread(target=data_source.left_cam_stream_main)
    right_cam_source_thread = threading.Thread(target=data_source.right_cam_stream_main)
    mid_cam_source_thread = threading.Thread(target=data_source.mid_cam_stream_main)

    lidar_source_thread.start()
    left_cam_source_thread.start()
    right_cam_source_thread.start()
    mid_cam_source_thread.start()

    # Subroutines
    monitoring = Monitoring(data_source, database)
    platform = CarPlatform('COM5', database)  # PLEASE CHECK YOUR COMPORT
    sign_cam = SignCam(data_source, database)
    planner = MotionPlanner(data_source, database)
    control = Control(database)

    monitoring_thread = threading.Thread(target=monitoring.main)
    platform_thread = threading.Thread(target=platform.main)
    sign_cam_thread = threading.Thread(target=sign_cam.main)
    planner_thread = threading.Thread(target=planner.main)
    control_thread = threading.Thread(target=control.main)

    monitoring_thread.start()
    platform_thread.start()
    sign_cam_thread.start()
    planner_thread.start()
    control_thread.start()


if __name__ == "__main__":
    main()
