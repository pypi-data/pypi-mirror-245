from ultralytics import YOLO
from autodistill_yolov8 import YOLOv8
import cv2
import math
import time
import torch
import random
import numpy as np
def image_predict_det(img_path, model_path,img_width,img_height):
    desired_width =img_width
    desired_height = img_height
    model = YOLOv8(model_path)
    img = cv2.imread(img_path)
    # Resize the image
    img = cv2.resize(img, (desired_width, desired_height))
    results = model.predict(img)  # run prediction on img
    # Iterate over results
    for result in results:
        #if not result.boxes.isempty():
            boxes = result.boxes.cpu().numpy()  # get boxes on cpu in numpy
            # Iterate over boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                r = box.xyxy[0].astype(int)  # get corner points as int
                print(r)  # print boxes
                cv2.rectangle(img, tuple(r[:2]), tuple(r[2:]), (255, 255, 255), 2)  # draw boxes on img
                # Class name
                class_name = result.names[int(box.cls[0])]
                print(class_name)
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = [x1, y1]
                fontScale = 1
                color = (255, 255, 0)
                thickness = 1
                cv2.putText(img, class_name, org, font, fontScale, color, thickness)
    # Display the image with bounding boxes
    cv2.imshow('Predictions', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#-------------------------------------------------
def video_predict_det(video_path,model_name,device_type):

    print(torch.cuda.is_available())
    cap = cv2.VideoCapture(video_path)

    # Get the width and height of the video frames
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # model
    model = YOLO(model_name)

    # object classes
    

    # Video writer initialization
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_filename = f"output_{time.strftime('%Y%m%d%H%M%S')}.avi"
    out = cv2.VideoWriter(output_filename, fourcc, 15.0, (width, height))

    # Initialize variables for FPS calculation
    start_time = time.time()
    frames_processed = 0

    while True:
        success, img = cap.read()

        # Check if the video has reached the end
        if not success:
            break

        # Set width and height dynamically
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Update the video capture settings
        cap.set(3, width)
        cap.set(4, height)

        # Measure the time taken for processing each frame
        start_frame_time = time.time()

        # YOLO model prediction
        results = model(img, device=device_type,stream=True)
        #results = model(img, device='cpu',stream=True)

        #results = model(frame, conf=0.70)
        #class_names = results[0].names
        # Coordinates
        for result in results:
            boxes = result.boxes

            for box in boxes:
                # Bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to int values

                # Put box in cam
                #cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                print("Confidence --->", confidence)
                class_name = result.names[int(box.cls[0])]
                # Class name
                cls = int(box.cls[0])
                #if (cls > 0):
                   # print("not person")
                #else:
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
               # print("Class name -->", classNames[cls])
                #man = classNames[cls]
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                    #if (man == "person"):
                cv2.putText(img, class_name, org, font, fontScale, color, thickness)

        # Write the frame to the output video
        out.write(img)

        # Increment frames_processed counter
        frames_processed += 1

        # Calculate and display FPS every 10 frames
        if frames_processed % 10 == 0:
            elapsed_time = time.time() - start_time
            fps = frames_processed / elapsed_time
            print(f"FPS: {fps:.2f}")

        # Display the frame
        cv2.imshow('Video', img)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release video capture and writer
    print(f"successfully saved video out: {output_filename}")
    cap.release()
    out.release()
    cv2.destroyAllWindows()

#------------


    print(torch.cuda.is_available())
    cap = cv2.VideoCapture(video_path)

    # Get the width and height of the video frames
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # model
    model = YOLO(model_name)

    # object classes
    

    # Video writer initialization
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_filename = f"output_{time.strftime('%Y%m%d%H%M%S')}.avi"
    out = cv2.VideoWriter(output_filename, fourcc, 15.0, (width, height))

    # Initialize variables for FPS calculation
    start_time = time.time()
    frames_processed = 0

    while True:
        success, img = cap.read()

        # Check if the video has reached the end
        if not success:
            break

        # Set width and height dynamically
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Update the video capture settings
        cap.set(3, width)
        cap.set(4, height)

        # Measure the time taken for processing each frame
        start_frame_time = time.time()

        # YOLO model prediction
        results = model(img, device='cpu',stream=True)
         # Coordinates
        for result in results:
            boxes = result.boxes

            for box in boxes:
                # Bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to int values

                # Put box in cam
                #cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                print("Confidence --->", confidence)
                class_name = result.names[int(box.cls[0])]
                # Class name
                cls = int(box.cls[0])
                #if (cls > 0):
                   # print("not person")
                #else:
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
               # print("Class name -->", classNames[cls])
                #man = classNames[cls]
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                    #if (man == "person"):
                cv2.putText(img, class_name, org, font, fontScale, color, thickness)

        # Write the frame to the output video
        out.write(img)

        # Increment frames_processed counter
        frames_processed += 1

        # Calculate and display FPS every 10 frames
        if frames_processed % 10 == 0:
            elapsed_time = time.time() - start_time
            fps = frames_processed / elapsed_time
            print(f"FPS: {fps:.2f}")

        # Display the frame
        cv2.imshow('Video', img)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release video capture and writer
    print(f"successfully saved video out: {output_filename}")
    cap.release()
    out.release()
    cv2.destroyAllWindows()
#---------------------------------------------------------

def webcamera_predict_det(model_name,webcamera_no,device_type):

    print(torch.cuda.is_available())
    cap = cv2.VideoCapture(webcamera_no)

    # Get the width and height of the video frames
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # model
    model = YOLO(model_name)

    # object classes
    

    # Video writer initialization
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_filename = f"output_{time.strftime('%Y%m%d%H%M%S')}.avi"
    out = cv2.VideoWriter(output_filename, fourcc, 15.0, (width, height))

    # Initialize variables for FPS calculation
    start_time = time.time()
    frames_processed = 0

    while True:
        success, img = cap.read()

        # Check if the video has reached the end
        if not success:
            break

        # Set width and height dynamically
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Update the video capture settings
        cap.set(3, width)
        cap.set(4, height)

        # Measure the time taken for processing each frame
        start_frame_time = time.time()

        # YOLO model prediction
        results = model(img, device=device_type,stream=True)
         # Coordinates
        for result in results:
            boxes = result.boxes

            for box in boxes:
                # Bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to int values

                # Put box in cam
                #cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                print("Confidence --->", confidence)
                class_name = result.names[int(box.cls[0])]
                # Class name
                cls = int(box.cls[0])
                #if (cls > 0):
                   # print("not person")
                #else:
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
               # print("Class name -->", classNames[cls])
                #man = classNames[cls]
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                    #if (man == "person"):
                cv2.putText(img, class_name, org, font, fontScale, color, thickness)

        # Write the frame to the output video
        out.write(img)

        # Increment frames_processed counter
        frames_processed += 1

        # Calculate and display FPS every 10 frames
        if frames_processed % 10 == 0:
            elapsed_time = time.time() - start_time
            fps = frames_processed / elapsed_time
            print(f"FPS: {fps:.2f}")

        # Display the frame
        cv2.imshow('Video', img)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release video capture and writer
    print(f"successfully saved video out: {output_filename}")
    cap.release()
    out.release()
    cv2.destroyAllWindows()
#-----------------

    print(torch.cuda.is_available())
    cap = cv2.VideoCapture(webcamera_no)

    # Get the width and height of the video frames
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # model
    model = YOLO(model_name)

    # object classes
    

    # Video writer initialization
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_filename = f"output_{time.strftime('%Y%m%d%H%M%S')}.avi"
    out = cv2.VideoWriter(output_filename, fourcc, 15.0, (width, height))

    # Initialize variables for FPS calculation
    start_time = time.time()
    frames_processed = 0

    while True:
        success, img = cap.read()

        # Check if the video has reached the end
        if not success:
            break

        # Set width and height dynamically
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Update the video capture settings
        cap.set(3, width)
        cap.set(4, height)

        # Measure the time taken for processing each frame
        start_frame_time = time.time()

        # YOLO model prediction
        results = model(img, device='cpu',stream=True)
         # Coordinates
        for result in results:
            boxes = result.boxes

            for box in boxes:
                # Bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to int values

                # Put box in cam
                #cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                print("Confidence --->", confidence)
                class_name = result.names[int(box.cls[0])]
                # Class name
                cls = int(box.cls[0])
                #if (cls > 0):
                   # print("not person")
                #else:
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
               # print("Class name -->", classNames[cls])
                #man = classNames[cls]
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                    #if (man == "person"):
                cv2.putText(img, class_name, org, font, fontScale, color, thickness)

        # Write the frame to the output video
        out.write(img)

        # Increment frames_processed counter
        frames_processed += 1

        # Calculate and display FPS every 10 frames
        if frames_processed % 10 == 0:
            elapsed_time = time.time() - start_time
            fps = frames_processed / elapsed_time
            print(f"FPS: {fps:.2f}")

        # Display the frame
        cv2.imshow('Video', img)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release video capture and writer
    print(f"successfully saved video out: {output_filename}")
    cap.release()
    out.release()
    cv2.destroyAllWindows()
#---------------------------
#segmentation inference

def image_predict_seg(img_path,model_path):
    model = YOLOv8(model_path)
    img = cv2.imread(img_path)
    results = model.predict(img)
    #print(results)
    for result in results:
        for mask, box in zip(result.masks.xy, result.boxes):
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            class_name = result.names[int(box.cls[0])]#list(model.names.values())
            classes_ids = [class_name.index(clas) for clas in class_name]
            colors = [random.choices(range(256), k=3) for _ in classes_ids]
            points = np.int32([mask])
            # cv2.polylines(img, points, True, (255, 0, 0), 1)
            color_number = classes_ids.index(int(box.cls[0]))
            cv2.fillPoly(img, points, colors[color_number])
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = [x1, y1]
            fontScale = 1
            color = (255, 255, 0)
            thickness = 1
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
            cv2.putText(img, class_name, org, font, fontScale, color, thickness)
            #print(class_name)
    cv2.imshow("Image Segmentation", img)
    cv2.waitKey(0)

    cv2.imwrite("YourSavePath", img)
#----------
def video_predict_seg(video_path,model_name,device_type):
    
        # Load the YOLOv8 model
    model = YOLO(model_name)
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.set(3, width)
    cap.set(4, height) 
    # Video writer initialization
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_filename = f"output_{time.strftime('%Y%m%d%H%M%S')}.avi"
    out = cv2.VideoWriter(output_filename, fourcc, 15.0, (width, height))
    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame, conf=0.70,device=device_type)
            # Access class names from results
            class_names = results[0].names
            #print(class_names)
            #if(class_names=="squirrel"):
                #index=1
           # else:
               # index=0
            # Display confidence, class name, and bounding box on the frame
            for i, box in enumerate(results[0].boxes.xyxy):
                x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                
                # Extract class information
                #class_index = int(box[4])
                #class_name = class_names[class_index]

                #print(f"Object {i + 1}: Class {class_name}, Confidence: {box[4]:.2f}")

                # Display confidence and class name on the frame
                #text = f"{class_name: class_name}"
                #cv2.putText(frame, class_name, (x1, y1 - 5),
                #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Draw bounding box
                #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            annotated_frame = results[0].plot() 
            #print(results[0].plot())
            out.write(annotated_frame)
            cv2.imshow("YOL0v8 Inference", annotated_frame) 

            # Display the annotated frame
            #cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release video capture
    cap.release()
    out.release()
    cv2.destroyAllWindows()
#camera segmentation
def camera_predict_seg(camera_source,model_name,device_type):
    
        # Load the YOLOv8 model
    model = YOLO(model_name)
    cap = cv2.VideoCapture(camera_source)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.set(3, width)
    cap.set(4, height) 
    # Video writer initialization
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_filename = f"output_{time.strftime('%Y%m%d%H%M%S')}.avi"
    out = cv2.VideoWriter(output_filename, fourcc, 15.0, (width, height))
    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame, conf=0.70,device=device_type)
            # Access class names from results
            class_names = results[0].names
            #print(class_names)
            #if(class_names=="squirrel"):
                #index=1
           # else:
               # index=0
            # Display confidence, class name, and bounding box on the frame
            for i, box in enumerate(results[0].boxes.xyxy):
                x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                
                # Extract class information
                #class_index = index#int(box[4])
                #class_name = class_names[class_index]

                #print(f"Object {i + 1}: Class {class_name}, Confidence: {box[4]:.2f}")

                # Display confidence and class name on the frame
                #text = f"{class_name: class_name}"
                #cv2.putText(frame, class_name, (x1, y1 - 5),
                #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Draw bounding box
                #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            annotated_frame = results[0].plot() 
            #print(results[0].plot())
            out.write(annotated_frame)
            cv2.imshow("YOL0v8 Inference", annotated_frame) 

            # Display the annotated frame
            #cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release video capture
    cap.release()
    out.release()
    cv2.destroyAllWindows()