import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def find_defects(reference_image, live_cam=0):
  
    reference = cv2.imread(reference_image)

    cap = cv2.VideoCapture(live_cam)

    while True:
        
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        gray_reference = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        difference = cv2.absdiff(gray_reference, gray_frame)

        _, threshold = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imshow("Defect Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_inspection():
    reference_image_path = filedialog.askopenfilename(title="Select Reference Image", filetypes=[("Image files", "*.jpg;*.png")])
    if reference_image_path:
        find_defects(reference_image_path)

root = tk.Tk()
root.title("Defect Inspection")

inspect_button = tk.Button(root, text="Start Inspection", command=start_inspection)
inspect_button.pack(pady=20)

root.mainloop()