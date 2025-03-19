import os
import json
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images

#  OCR preprocessing
def preprocess_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    return processed

def extract_text_from_image(image):
    return pytesseract.image_to_string(image, config='--psm 6')

def parse_text_to_json(ocr_text):
    students_data = {}
    lines = ocr_text.split("\n")

    for line in lines:
        parts = line.split()
        if len(parts) < 2:
            continue  

        student_id = parts[0]  
        students_data[student_id] = {
            "Mon": {"A": False, "1": False, "2": False, "3": False},
            "Tue": {"A": False, "1": False, "2": False, "3": False},
            "Wed": {"A": False, "1": False, "2": False, "3": False},
            "Thu": {"A": False, "1": False, "2": False, "3": False},
            "W": False, "B": False, "S": False, "BP": False, "TS": False
        }

        attendance_data = parts[1:]
        days = ["Mon", "Tue", "Wed", "Thu"]
        day_index = 0

        for i in range(0, len(attendance_data), 4):
            if day_index >= len(days):
                break  
            
            day = days[day_index]
            students_data[student_id][day] = {
                "A": "A" in attendance_data[i:i+4],
                "1": "1" in attendance_data[i:i+4],
                "2": "2" in attendance_data[i:i+4],
                "3": "3" in attendance_data[i:i+4]
            }
            day_index += 1

        if len(attendance_data) >= 20:
            students_data[student_id]["W"] = "W" in attendance_data[-5]
            students_data[student_id]["B"] = "B" in attendance_data[-4]
            students_data[student_id]["S"] = "S" in attendance_data[-3]
            students_data[student_id]["BP"] = "T" in attendance_data[-2]
            students_data[student_id]["TS"] = "T" in attendance_data[-1]

    return students_data

# Process Multiple PDFs and Generate JSON
def process_pdfs(pdf_folder):
    all_students_data = {}

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            images = convert_pdf_to_images(pdf_path)

            for image in images:
                processed_image = preprocess_image(image)
                ocr_text = extract_text_from_image(processed_image)
                student_data = parse_text_to_json(ocr_text)
                all_students_data.update(student_data)

    return json.dumps(all_students_data, indent=4)

pdf_folder = r"C:\task\pdf"

output_json = process_pdfs(pdf_folder)

with open("students_data.json", "w") as json_file:
    json_file.write(output_json)

print("JSON data saved successfully!")
