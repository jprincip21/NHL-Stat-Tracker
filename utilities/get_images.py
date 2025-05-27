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
    """Function to Get team Light and Dark Logos"""
    dark_url = svg_url.replace("light.svg", "dark.svg")
    
    response_light = requests.get(svg_url)
    response_dark = requests.get(dark_url)

    if response_light.status_code != 200 or response_dark.status_code != 200:
        print("Failed to load logo.")
        return None
    
    png_bytes_light = cairosvg.svg2png(bytestring=response_light.content, output_width=size[0], output_height=size[1])
    png_bytes_dark = cairosvg.svg2png(bytestring=response_dark.content, output_width=size[0], output_height=size[1])

    return ctk.CTkImage(light_image=Image.open(BytesIO(png_bytes_light)),
                        dark_image=Image.open(BytesIO(png_bytes_dark)),
                        size=(28, 28))