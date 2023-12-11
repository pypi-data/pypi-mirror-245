import cv2
import os
from enum import Enum

class DatasetType(Enum):
    TRAINING = 0
    VALIDATION = 1
    TEST = 2

class DataGenerator:
    
    def __create_dirs(self, dataset_type : DatasetType, img_class : str):
        PATH_DATASET = "dataset/"
        PATH_DT = None
        if not os.path.exists(PATH_DATASET):
            os.mkdir(PATH_DATASET)

        if dataset_type == DatasetType.TRAINING:
            PATH_DT = os.path.join(PATH_DATASET, "training/")
            if not os.path.exists(PATH_DT):
                os.mkdir(PATH_DT)
        elif dataset_type == DatasetType.VALIDATION:
            PATH_DT = os.path.join(PATH_DATASET, "validation/")
            if not os.path.exists(PATH_DT):
                os.mkdir(PATH_DT)
        elif dataset_type == DatasetType.TEST:
            PATH_DT = os.path.join(PATH_DATASET, "test/")
            if not os.path.exists(PATH_DT):
                os.mkdir(PATH_DT)

        PATH_CLASS = os.path.join(PATH_DT, img_class)
        if not os.path.exists(PATH_CLASS):
            os.mkdir(PATH_CLASS)

        return PATH_CLASS

    def generate(self, video_path : str, img_class : str, dataset_type : DatasetType) -> None:
        if os.path.exists(video_path):
            video = cv2.VideoCapture(video_path)
            counter = 0
            img_counter = 0

            PATH_CLASS = self.__create_dirs(dataset_type, img_class)

            while(video.isOpened()):
                ret, frame = video.read()
                if ret == True:
                    if counter == 10:
                        cv2.imwrite(os.path.join(PATH_CLASS, f"{img_counter}.jpg"), frame)
                        img_counter += 1
                        counter = 0
                else:
                    break
                counter += 1