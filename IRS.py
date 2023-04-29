#=====================#
#======Imports========#
import mysql.connector
import tkinter as tk
from tkinter import *
from tkinter import ttk
import cv2
import numpy as np
import face_recognition as fr
import os
from datetime import *
#=====================#
#=Database Connection=#
mydb=mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Crushedspirit",
    database="project"
)

mycursor=mydb.cursor()

def retrive(ID):
    sql_statment="select * from students where CNIC='{0}';"
    mycursor.execute(sql_statment.format(str(ID)))
    myresult=mycursor.fetchone()
    return myresult



win = Tk()




path = "C:\Users\Hp\Downloads\out"
images = []
names = []
myList = os.listdir(path)
print(myList)

# find the name of the person from image name and add images to a list

for imgNames in myList:
    curImg = cv2.imread(f"{path}/{imgNames}")
    images.append(curImg)
    names.append(os.path.splitext(imgNames)[0])


def get(faceLoc):
    y1, x2, y2, x1 = faceLoc
    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

def findEncodings(images):
    encodedlist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodedlist.append(encode)
    return encodedlist
encodeListKnown = findEncodings(images)



print("Encoding Complete")

cap = cv2.VideoCapture(0)

# open video capture and detect a face, find and compare its encodings by the distance, and if the distance is within the min range, show recognition
faceDis=[1,2,3]
matches=[1,2,3]
while True:
    _, webcam = cap.read()
    cv2.imshow('webcam',webcam)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    for i in range(0,3):
        imgResized = cv2.resize(webcam, (0, 0), None, 0.25, 0.25)
        imgResized = cv2.cvtColor(imgResized, cv2.COLOR_BGR2RGB)

        faceCurFrame = fr.face_locations(imgResized)
        encodeFaceCurFrame = fr.face_encodings(imgResized, faceCurFrame)
        for encodeFace, faceLoc in zip(encodeFaceCurFrame, faceCurFrame):
            matches = fr.compare_faces(encodeListKnown, encodeFace)
            faceDis = fr.face_distance(encodeListKnown, encodeFace)

        # argmin returns the indices of the minimum values along axis

        matchIndex = np.argmin(faceDis)


        # checks for match; if match found, shows name from the image name, and the face match percentage


        if matches[matchIndex]:
            name = names[matchIndex]
            name.format(int)
            res=retrive(name)
            # =====================#
            # =========GUI=========#


            #
            # frn=Frame(win)
            # frn.pack(side=tk.LEFT,padx=20)
            #
            # tv=ttk.Treeview(frn,columns=(1,2,3,4,5,6),height="5")
            # tv.pack()
            #
            # tv.heading(2,text="ID")
            # tv.heading(3, text="Name")
            # tv.heading(4, text="Phone No.")
            # tv.heading(5, text="Address")
            # tv.heading(6, text="Class")
            #
            #
            # win.title("Student Data")
            # win.geometry("800x400")
            # win.resizable(False, False)
            # # win.after()
            # win.mainloop()

            print(res)
            # y1, x2, y2, x1 = faceLoc
            # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            # cv2.rectangle(webcam, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.rectangle(webcam, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            # cv2.putText(webcam,name,(x1 + 6, y2 - 6),cv2.FONT_HERSHEY_COMPLEX,1,(255, 255, 255),1,)

        # face_match_percentage = (1 - faceDis) * 100
        # for i, face_distance in enumerate(faceDis):
        #     print("The test image has a distance of {:.2} from known image {} ".format(face_distance, i))
        #     print("- comparing with a tolerance of 0.6 {}".format(face_distance < 0.6))
        #     print("Face Match Percentage = ", np.round(face_match_percentage, 4))  # upto 4 decimal places
cap.release()
cv2.destroyAllWindows()
