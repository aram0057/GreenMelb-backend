# classification/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import FileSystemStorage
import torch
import cv2
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model
import os
from django.conf import settings
from .serializers import ImageUploadSerializer

# Load YOLO model
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True)
# Load classification model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(settings.BASE_DIR, 'backend', 'models', 'waste_classification_model.h5')
classification_model = load_model(model_path)
class_labels = ['E-Waste', 'Organic', 'Recyclable']
# Load VGG16 for feature extraction
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))
feature_extractor = Model(inputs=base_model.input, outputs=base_model.output)

def preprocess_and_extract_features(cropped_pil_image):
    img_array = keras_image.img_to_array(cropped_pil_image.resize((150, 150)))
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    features = feature_extractor.predict(img_array)
    features_flattened = features.reshape(features.shape[0], -1)
    return features_flattened

class ImageUploadView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['uploaded_file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)

            # Process the image
            original_image = cv2.imread(file_path)
            results = yolo_model(original_image)
            detections = results.xyxy[0].numpy()

            confidence_threshold = 0.5
            detections = [detection for detection in detections if detection[4] >= confidence_threshold]

            background_colors = {
                'E-Waste': (255, 153, 153),   
                'Organic': (153, 255, 153),   
                'Recyclable': (153, 153, 255)
            }
            
            total = []
            for detection in detections:
                x1, y1, x2, y2, conf, cls = detection
                xmin, ymin, xmax, ymax = int(x1), int(y1), int(x2), int(y2)
                
                cropped_image = original_image[ymin:ymax, xmin:xmax]
                cropped_pil_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
                
                features_flattened = preprocess_and_extract_features(cropped_pil_image)
                
                prediction = classification_model.predict(features_flattened)
                predicted_class_index = np.argmax(prediction, axis=1)[0]
                predicted_class_label = class_labels[predicted_class_index]
                total.append(predicted_class_label)
                class_color = background_colors[predicted_class_label]
                
                font_scale = max(0.5, min(xmax - xmin, ymax - ymin) / 400)
                font_thickness = int(max(1, min(xmax - xmin, ymax - ymin) / 100))
                
                label = f"{predicted_class_label}: {conf:.2f}"
                text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
                text_x, text_y = xmin, max(ymin - 10, text_size[1] + 10)
                box_coords = ((text_x, text_y - text_size[1] - 10), (text_x + text_size[0] + 10, text_y + 5))
                
                cv2.rectangle(original_image, box_coords[0], box_coords[1], class_color, cv2.FILLED)
                
                text_color = (0, 0, 0)
                
                # Increase the thickness of the bounding box
                thicker_box_thickness = 10  # Set the thickness to a higher value
                cv2.rectangle(original_image, (xmin, ymin), (xmax, ymax), class_color, thicker_box_thickness)
                
                cv2.putText(original_image, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 
                            font_scale, text_color, font_thickness, lineType=cv2.LINE_AA)

            processed_image_path = os.path.join(settings.MEDIA_ROOT, f"processed_{filename}")
            print(f"Writing processed image to: {os.path.abspath(processed_image_path)}")
            cv2.imwrite(processed_image_path, original_image)
            processed_file_url = fs.url(f"processed_{filename}")

            return Response({
                'status': 'file processed successfully',
                'processed_file_url': processed_file_url,
                'classifications': total
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)