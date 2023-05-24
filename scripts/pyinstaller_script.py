import os
import sys
import PyInstaller.__main__
import pkg_resources

package_location = pkg_resources.get_distribution('customtkinter').location
customtkinter_path = os.path.join(package_location, 'customtkinter')
customtkinter_path = os.path.normpath(customtkinter_path)

if sys.platform == 'win32':
    add_data_customtkinter = f"{customtkinter_path};customtkinter"
    add_data_custom_theme = "custom_theme.json;."
else:
    add_data_customtkinter = f"{customtkinter_path}:customtkinter"
    add_data_custom_theme = "custom_theme.json:."

args = [
    "--onedir",
    "--add-data", add_data_customtkinter,
    "--add-data", add_data_custom_theme,
    "--windowed",
    "--name", "mp-rtt-ocr",
    "main.py"
]

PyInstaller.__main__.run(args)
