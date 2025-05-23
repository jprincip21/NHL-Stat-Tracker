import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

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