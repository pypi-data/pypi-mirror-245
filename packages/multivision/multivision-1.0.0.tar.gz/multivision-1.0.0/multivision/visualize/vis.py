from IPython.display import Image as IPImage, display
import cv2
import os
import os
import cv2
import matplotlib.pyplot as plt

def images_google_colab(folder_path):
    # Get a list of all image files in the specified folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        # Display the image name without extension
        print(os.path.splitext(image_file)[0])

        # Display the image using IPython.display
        display(IPImage(filename=os.path.join(folder_path, image_file), width=600))
#---------------------------

def display_images_cv(folder_path,scale_factor):
    scale_factor=scale_factor
    # Get a list of all image files in the specified folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        # Read the image using OpenCV
        image_path = os.path.join(folder_path, image_file)
        img = cv2.imread(image_path)

        # Resize the image (optional)
        #img = cv2.resize(img, (img.shape[1], img.shape[0]))

        # Get image dimensions
        height, width, _ = img.shape
        img= cv2.resize(img, (int(width * scale_factor), int(height * scale_factor)))

        #img = cv2.resize(img, (height,width))
        # Add text annotation for image dimensions
        text = f"Dimensions: {width} x {height}"
        print(text)
        #cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Create a window with a specific name
        #cv2.namedWindow(os.path.splitext(image_file)[0], cv2.WINDOW_NORMAL)

        # Move the window to the center of the screen
        #cv2.moveWindow(os.path.splitext(image_file)[0], 100, 100)

        # Display the image
        cv2.imshow(os.path.splitext(image_file)[0], img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


#-------------------


def display_images_with_grid(folder_path, rows, cols):
    # Get a list of all image files in the specified folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    fig, axes = plt.subplots(rows, cols, figsize=(10, 10))

    for i, image_file in enumerate(image_files):
        # Read the image using OpenCV
        image_path = os.path.join(folder_path, image_file)
        img = cv2.imread(image_path)

        # Resize the image (optional)
        img = cv2.resize(img, (img.shape[1], img.shape[0]))

        # Get image dimensions
        height, width, _ = img.shape

        # Add text annotation for image dimensions
        text = f"Dimensions: {width} x {height}"
        cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Display the image on the subplot
        ax = axes[i // cols, i % cols]
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax.set_title(os.path.splitext(image_file)[0])
        ax.axis('off')

    plt.tight_layout()
    plt.show()



#---------------
def plot(annotation_path,images_dir_path,yaml_path,samples_no):
        ANNOTATIONS_DIRECTORY_PATH = annotation_path#"dataset/train/labels"
        IMAGES_DIRECTORY_PATH = images_dir_path#"dataset/train/images"
        DATA_YAML_PATH = yaml_path
        SAMPLE_SIZE = samples_no
        SAMPLE_GRID_SIZE = (samples_no // 4, samples_no // 4)
        SAMPLE_PLOT_SIZE = (samples_no, samples_no)
        dataset = sv.DetectionDataset.from_yolo(
            images_directory_path=IMAGES_DIRECTORY_PATH,
            annotations_directory_path=ANNOTATIONS_DIRECTORY_PATH,
            data_yaml_path=DATA_YAML_PATH
        )
        len(dataset)
        image_names = list(dataset.images.keys())[:SAMPLE_SIZE]
        mask_annotator = sv.MaskAnnotator()
        box_annotator = sv.BoxAnnotator()
        images = []
        for image_name in image_names:
            image = dataset.images[image_name]
            annotations = dataset.annotations[image_name]
            labels = [
                dataset.classes[class_id]
                for class_id
                in annotations.class_id]
            annotates_image = mask_annotator.annotate(
                scene=image.copy(),
                detections=annotations)
            annotates_image = box_annotator.annotate(
                scene=annotates_image,
                detections=annotations,
                labels=labels)
            images.append(annotates_image)
        sv.plot_images_grid(
            images=images,
            titles=image_names,
            grid_size=SAMPLE_GRID_SIZE,
            size=SAMPLE_PLOT_SIZE)
