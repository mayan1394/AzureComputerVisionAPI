#!/usr/bin/env python
# coding: utf-8

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from array import array
import os
from PIL import Image
import sys
import time
import pandas as pd

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# In[4]:
os.chdir("C:\Project Work\Mayank_Data\GCP Test")


# In[5]:
def getimagedescription(image):
    image = open(image,"rb")
    description_result = computervision_client.describe_image_in_stream(image)
    if (len(description_result.captions) == 0):
        caption = "No description detected."
    else:
        for caption in description_result.captions:
            caption = "'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100)
    return caption


def getimagecategories(image):
    image = open(image,"rb")
    category1=""
    categorize_results_local = computervision_client.analyze_image_in_stream(image, ["categories"])
    print("Categories from local image: ")
    if (len(categorize_results_local.categories) == 0):
        category="No categories detected."
    else:
        for category in categorize_results_local.categories:
            category="'{}' with confidence {:.2f}%".format(category.name, category.score * 100)
            category1+=category
        return category1
    

def getimagetags(image):
    image=open(image,"rb")
    tags1=""
    tags_result_local = computervision_client.tag_image_in_stream(image)
    if (len(tags_result_local.tags) == 0):
        tags="No tags detected"
    else:
        for tag in tags_result_local.tags:
            tags= "'{}' with confidence {:.2f}% ".format(tag.name, tag.confidence * 100)
            tags1+=tags
    return tags1


def detectfaces(image):
    image=open(image,"rb")
    detect_faces_results_local = computervision_client.analyze_image_in_stream(image, ["faces"])
    finalfaceresult=""
    # Print results with confidence score
    print("Faces in the local image: ")
    if (len(detect_faces_results_local.faces) == 0):
        finalfaceresult="No faces detected"
    else:
        for face in detect_faces_results_local.faces:
            faces="'{}' of age {} at location {}, {}, {}, {} ".format(face.gender, face.age,             face.face_rectangle.left, face.face_rectangle.top,             face.face_rectangle.left + face.face_rectangle.width,             face.face_rectangle.top + face.face_rectangle.height)
            finalfaceresult+=faces
        return finalfaceresult


def detectadultcontent(image):
    image = open(image, "rb")
    # Select visual features you want
    # Call API with local image and features
    detect_adult_results_local = computervision_client.analyze_image_in_stream(image, ["adult"])

    # Print results with adult/racy score
    #print("Analyzing local image for adult or racy content ... ")
    adult_content="Is adult content: {} with confidence {:.2f}".format(detect_adult_results_local .adult.is_adult_content, detect_adult_results_local .adult.adult_score * 100)
    racy_content="Has racy content: {} with confidence {:.2f}".format(detect_adult_results_local .adult.is_racy_content, detect_adult_results_local .adult.racy_score * 100)
    return adult_content,racy_content #Returns Tuple
    

def detectcolor(image):
    local_image = open(image, "rb")
    # Select visual feature(s) you want
    local_image_features = ["color"]
    # Call API with local image and features
    detect_color_results_local = computervision_client.analyze_image_in_stream(local_image, local_image_features)

    # Print results of the color scheme detected
    #print("Getting color scheme of the local image: ")
    #print("Is black and white: {}".format(detect_color_results_local.color.is_bw_img))
    #Accent Color = Most vibrant color in the image
    #print("Accent color: {}".format(detect_color_results_local.color.accent_color))
    #print("Dominant background color: {}".format(detect_color_results_local.color.dominant_color_background))
    #print("Dominant foreground color: {}".format(detect_color_results_local.color.dominant_color_foreground))
    dominantcolors = "Dominant colors: {}".format(detect_color_results_local.color.dominant_colors)
    return dominantcolors


def getcelebrities(image):  #return value
    #print("===== Detect Domain-specific Content - local =====")
    # Open local image file containing a celebtriy
    image = open(image, "rb")
    # Call API with the type of content (celebrities) and local image
    detect_domain_results_celebs_local = computervision_client.analyze_image_by_domain_in_stream("celebrities", image)
    celeb=""
    # Print which celebrities (if any) were detected
    print("Celebrities in the local image:")
    if len(detect_domain_results_celebs_local.result["celebrities"]) == 0:
        print("No celebrities detected.")
    else:
        for celeb in detect_domain_results_celebs_local.result["celebrities"]:
            print (celeb)
            print(celeb["name"])

            
def getlandmarks(image): #return value
    #local_image_path_landmark = "resources\\landmark.jpg"
    image = open(image, "rb")
    # Call API with type of content (landmark) and local image
    detect_domain_results_landmark_local = computervision_client.analyze_image_by_domain_in_stream("landmarks", image)
    print()

    # Print results of landmark detected
    print("Landmarks in the local image:")
    if len(detect_domain_results_landmark_local.result["landmarks"]) == 0:
        print("No landmarks detected.")
    else:
        for landmark in detect_domain_results_landmark_local.result["landmarks"]:
            print(landmark["name"])
    print()
    

def detectobjects(image):
    print("===== Detect Objects - local =====")
    # Get local image with different objects in it
    #local_image_path_objects = "resources\\objects.jpg"
    image = open(image, "rb")
    # Call API with local image
    detect_objects_results_local = computervision_client.detect_objects_in_stream(image)
    #s=""
    # Print results of detection with bounding boxes
    print("Detecting objects in local image:")
    #print(detect_objects_results_local.objects)
    s=""
    if len(detect_objects_results_local.objects) == 0:
        print("No objects detected.")
    else:
        
        for object in detect_objects_results_local.objects:
            #print("Object : {} with confidence: {}".format(\object.object_property,object.confidence))            
            obj="object= {} , confidence= {} ".format(object.object_property, object.confidence)
            s+=obj
    return s


def detectbrands(image):
    print("===== Detect Brands - local =====")
    # Open image file
    #local_image_path_shirt = "resources\\gray-shirt-logo.jpg"
    image = open(image, "rb")
    # Select the visual feature(s) you want
    local_image_features = ["brands"]
    # Call API with image and features
    detect_brands_results_local = computervision_client.analyze_image_in_stream(image, ["brands"])
    s=""
    # Print detection results with bounding box and confidence score
    print("Detecting brands in local image: ")
    if len(detect_brands_results_local.brands) == 0:
        print("No brands detected.")
    else:
        #s=""
        for brand in detect_brands_results_local.brands:
            obj="'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {} ".format(             brand.name, brand.confidence * 100, brand.rectangle.x, brand.rectangle.x + brand.rectangle.w,             brand.rectangle.y, brand.rectangle.y + brand.rectangle.h)
            s+=obj
    return s
    
def detecttext(image):
    # Get an image with printed text
    #local_image_printed_text_path = "resources\\printed_text.jpg"
    image = open(image, "rb")

    ocr_result_local = computervision_client.recognize_printed_text_in_stream(image)
    test=""
    for region in ocr_result_local.regions:
        #s=""
        for line in region.lines:
            #print(line)
            #print("Bounding box: {}".format(line.bounding_box))
            #s = ""
            text=""
            for word in line.words:
                text=word.text+" "
                test += text
            
        return test


def main():
    #time.sleep() is used to counter Azure's limitation of 20 calls API per minute, The time.sleep() functions below limit it to only 15 API calls per minute.    
    full_list=[]
    for photos in os.listdir():
        description=getimagedescription(photos)
        time.sleep(4)
        tags=getimagetags(photos)
        time.sleep(4)
        category=getimagecategories(photos)
        time.sleep(4)
        faces=detectfaces(photos)
        time.sleep(4)
        safesearch=detectadultcontent(photos)
        time.sleep(4)
        adult_content,racy_content=detectadultcontent(photos)
        time.sleep(4)
        color=detectcolor(photos)
        time.sleep(4)
        celebrities=getcelebrities(photos)
        time.sleep(4)
        objects=detectobjects(photos)
        time.sleep(4)
        brands=detectbrands(photos)
        time.sleep(4)
        text=detecttext(photos)
        time.sleep(2)
        full_list.append([photos,description,tags,category,faces,safesearch,adult_content,racy_content,color,celebrities,objects,brands,text])
    df=pd.DataFrame(full_list,columns=['FileName','Description','Tags','Category','Faces','Safesearch','Adult Content','Racy Content','Color','Celebrities','Objects','Brands','Text'])
    df.to_csv('Testazure.csv')
    
            
if __name__ == "__main__":
    main()           


# In[ ]:




