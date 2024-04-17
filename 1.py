# """
# -*- coding: utf-8 -*-
# @Time : 2024/2/23 11:27
# """
# import os
# import fitz  # PyMuPDF
# from PIL import Image
#
# def pdf_to_jpg(pdf_path, jpg_folder):
#     # Open the PDF
#     pdf_document = fitz.open(pdf_path)
#
#     # Iterate through each page
#     for page_number in range(len(pdf_document)):
#         # Get the page
#         page = pdf_document[page_number]
#
#         # Convert the page to an image
#         pix = page.get_pixmap()
#         img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#
#         # Save the image as JPG
#         jpg_path = os.path.join(jpg_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{page_number + 1}.jpg")
#         img.save(jpg_path)
#
#     # Close the PDF
#     pdf_document.close()
#
# def batch_convert_pdf_to_jpg(pdf_folder, jpg_folder):
#     # Ensure output folder exists
#     os.makedirs(jpg_folder, exist_ok=True)
#
#     # Iterate through PDF files in the folder
#     for filename in os.listdir(pdf_folder):
#         if filename.endswith('.pdf'):
#             pdf_path = os.path.join(pdf_folder, filename)
#             pdf_to_jpg(pdf_path, jpg_folder)
#
# # Example usage
# pdf_folder = r"D:\测试文件\巴雷410426198601297515"
# jpg_folder = r"C:\Users\9000\Desktop\新建文件夹 (4)"
# batch_convert_pdf_to_jpg(pdf_folder, jpg_folder)


import math

# a = (2000-1811.18)/2
# print(a".2f")

number = 998.769
rounded_number = math.floor(number * 100) / 100
print(rounded_number)