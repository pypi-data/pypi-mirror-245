from autodistill_yolov8 import YOLOv8

def y8d_train(model_name,epochs_no,data_yaml_path):
    target_model = YOLOv8(model_name)
    target_model.train(data_yaml_path, epochs=epochs_no)
#----------for segmentation tarining

def y8s_train(model_name,epochs_no,data_yaml_path):
    target_model = YOLOv8(model_name)
    target_model.train(data_yaml_path, epochs=epochs_no)

