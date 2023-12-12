import cv2
from cv2 import CAP_PROP_FRAME_COUNT
import os

TRAINING = 0
VALIDATION = 1
TEST = 2

class DataGenerator:
    
    def __create_dirs(self, dataset_path, dataset_type : int, img_class : str):
        PATH_DATASET = dataset_path
        PATH_DT = None
        if not os.path.exists(PATH_DATASET):
            os.mkdir(PATH_DATASET)

        if dataset_type == TRAINING:
            PATH_DT = os.path.join(PATH_DATASET, "training/")
            if not os.path.exists(PATH_DT):
                os.mkdir(PATH_DT)
        elif dataset_type == VALIDATION:
            PATH_DT = os.path.join(PATH_DATASET, "validation/")
            if not os.path.exists(PATH_DT):
                os.mkdir(PATH_DT)
        elif dataset_type == TEST:
            PATH_DT = os.path.join(PATH_DATASET, "test/")
            if not os.path.exists(PATH_DT):
                os.mkdir(PATH_DT)

        PATH_CLASS = os.path.join(PATH_DT, img_class)
        if not os.path.exists(PATH_CLASS):
            os.mkdir(PATH_CLASS)

        return PATH_CLASS
    
    def __findName(self, img_class, path : str) -> int:
        counter = 0;
        img_name = f"{img_class}_{counter}_.jpg"
        while os.path.exists(os.path.join(path, img_name)):
            counter += 1 
            img_name = f"{img_class}_{counter}_.jpg"
        return counter

    def generate(self, video_path : str, img_class : str, dataset_path = "dataset/") -> None:
        '''Generates a dataset from a video.'''
        if os.path.exists(video_path):
            video = cv2.VideoCapture(video_path)

            frame_count = video.get(CAP_PROP_FRAME_COUNT)

            train_frames = int(frame_count * 0.6)
            validation_frames = int(frame_count * 0.3)
            test_frames = int(frame_count * 0.1)
            PATH_TRAINIG = self.__create_dirs(dataset_path, TRAINING, img_class)
            PATH_TEST = self.__create_dirs(dataset_path, TEST, img_class)
            PATH_VALIDATION = self.__create_dirs(dataset_path, VALIDATION, img_class)

            first_name_train = self.__findName(img_class, PATH_TRAINIG)
            first_name_validate = self.__findName(img_class, PATH_VALIDATION)
            first_name_test = self.__findName(img_class, PATH_TEST)

            train_completed = False
            validate_completed = False
            
            counter = first_name_train
            while(video.isOpened()):
                ret, frame = video.read()
                img_name = f"{img_class}_{counter}.jpg"
                if ret == True:
                    if train_frames > 0:
                        cv2.imwrite(os.path.join(PATH_TRAINIG, img_name), frame)
                        train_frames -= 1
                    elif not train_completed:
                        counter = first_name_validate
                        train_completed = True
                        img_name = f"{img_class}_{counter}.jpg"

                    if validation_frames > 0 and train_completed:
                        cv2.imwrite(os.path.join(PATH_VALIDATION, img_name), frame)
                        validation_frames-= 1
                    elif not validate_completed and train_completed: 
                        counter = first_name_test
                        validate_completed = True
                        img_name = f"{img_class}_{counter}.jpg"

                    if test_frames > 0 and validate_completed:
                        cv2.imwrite(os.path.join(PATH_TEST, img_name), frame)
                        validation_frames-= 1
                else:
                    break
                counter += 1
            video.release()