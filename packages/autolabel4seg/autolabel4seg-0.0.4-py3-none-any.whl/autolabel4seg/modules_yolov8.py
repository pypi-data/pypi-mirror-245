from autodistill_yolov8 import YOLOv8
#ANNOTATIONS_DIRECTORY_PATH = "dataset/train/labels"
#IMAGES_DIRECTORY_PATH = "dataset/train/images"
DATA_YAML_PATH = "dataset/data.yaml"

def y8_train(model_name,epochs_no,data_yaml_path):
    target_model = YOLOv8(model_name)
    target_model.train(data_yaml_path, epochs=epochs_no)
