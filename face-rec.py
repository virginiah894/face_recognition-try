import face_recognition
import os
import cv2
 
KNOWN_IMAGES_DIR = "known_photos"
UNKNOWN_IMAGES_DIR = "unknown_photos"

TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "cnm" #hog

def name_to_color(name):
    # Take 3 first letters, tolower()
    # lowercased character ord() value rage is 97 to 122, substract 97, multiply by 8
    color = [(ord(c.lower())-97)*8 for c in name[:3]]
    return color

print('loading_known_faces')

known_faces = []
known_names = []

for  name in os.listdir(KNOWN_IMAGES_DIR):
    for filename in os.listdir(f'{KNOWN_IMAGES_DIR}/{name}'):
        image = face_recognition.load_image_file(f'{KNOWN_IMAGES_DIR}/{name}/{filename}')
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)
print('Finding Unkown faces')
for filename in os.listdir(UNKNOWN_IMAGES_DIR):
    print(f'Filename{filename}', end='')
    image = face_recognition.load_image_file(f'{UNKNOWN_IMAGES_DIR}/{filename}')
    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    for face_encoding, face_location in zip(encoding, locations):
        results = face_recognition.compare_faces(known_faces,face_encoding, TOLERANCE)
        match = None
        if True in results:
            match = known_names[results.index(True)]
            print(f'Match Found:{match}')
            
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = [0,255,0]
            cv2.rectangle(image, top_left,bottom_right,color,FRAME_THICKNESS)


            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2]+22)
            cv2.rectangle(image, top_left,bottom_right,color,cv2.FILLED)
            cv2.putText(image,match,(face_location[3]+10,face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX,0.5,(200,200,200),FONT_THICKNESS)

    cv2.imshow(filename,image)
    cv2.waitKey(100)
   
 

