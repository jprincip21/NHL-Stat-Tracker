import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

import requests
import cairosvg
from io import BytesIO

from PIL import Image

def get_image_light_dark(base_path):
    """Function to open images"""
    return ctk.CTkImage(light_image=Image.open(base_path + "light.png"),
                        dark_image=Image.open(base_path + "dark.png"),
                        size=(50, 50))

def get_image_default(base_path):
    """Function to open images"""
    return ctk.CTkImage(light_image=Image.open(base_path),
                        dark_image=Image.open(base_path),
                        size=(50, 50))

def get_team_logo(svg_url, size=(50,50)):
    response = requests.get(svg_url)

    if response.status_code != 200:
        print("Failed to load logo.")
        return None
    
    png_bytes = cairosvg.svg2png(bytestring=response.content, output_width=size[0], output_height=size[1])

    return ctk.CTkImage(light_image=Image.open(BytesIO(png_bytes)),
                        dark_image=Image.open(BytesIO(png_bytes)),
                        size=(28, 28))