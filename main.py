import datetime
import os
import string
import threading
import time
import sqlite3
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from config import Config
import random
import tkinter as tk
from tkinter import filedialog
from pylnk3 import Lnk
from win32con import SM_CXICON
from win32api import GetSystemMetrics
from win32ui import CreateDCFromHandle, CreateBitmap
from win32gui import ExtractIconEx, DestroyIcon, GetDC
from PIL import Image
from requestez import Session
import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np

session = Session()


def get_url_from_url_file(file_path):
    """
    Extract the URL from a .url file.

    Args:
    - file_path (str): The path to the .url file.

    Returns:
    - str: The URL extracted from the .url file.
    """
    try:
        # Read the .url file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Search for the [InternetShortcut] section and URL field
        for line in lines:
            if line.strip().startswith("URL="):
                url = line.strip()[4:]
                return url

        print(f"No URL found in {file_path}")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def search_and_download_icon(file_name, output_path):
    """
    Search the web for the file name, download an icon, and remove the background.

    Args:
    - file_name (str): The name of the file to search for.
    - output_path (str): The path to save the icon images.

    Returns:
    - None
    """
    file_name = file_name.split(".")[0]
    original_path = output_path.replace(".png", ".original.png")
    try:
        if not os.path.exists(original_path):
            # Search for the file name and get the search results
            search_url = f"https://www.google.com/search?q=transparent+{file_name}+icon&tbm=isch"
            response = requests.get(search_url)
            response.raise_for_status()

            # Parse the search results using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')

            # Get the URL of the first image (assuming it's the icon)
            icon_url = img_tags[1]['src']  # Index 0 is usually the Google logo

            # Download the icon image
            icon_data = requests.get(icon_url).content

            # Save the original icon image

            with open(original_path, 'wb') as icon_file:
                icon_file.write(icon_data)

        # os.system(f"convert {original_path} -transparent white {output_path}")
        os.system(f"convert {original_path} -fuzz 43% -transparent white {output_path}")
        _session_manager.add_log(f"Original icon saved to {original_path}")
        _session_manager.add_log(f"Processed icon saved to {output_path}")
    except Exception as e:
        _session_manager.add_log(f"Error downloading and processing icon: {e}")


def download_favicon(website_url, image_path):
    protocol, _, domain, _ = (website_url + "/").split("/", 3)
    resp = requests.get(f"{protocol}//{domain}/favicon.ico", allow_redirects=False)
    try:
        resp.raise_for_status()
        if resp.content:
            with open(image_path, "wb") as f:
                f.write(resp.content)
        else:
            raise Exception("No data in file")
    except Exception as e:
        _session_manager.add_log(str(e))
        search_and_download_icon(domain, image_path)


def extract_icon_from_steam(app_id, image_path):
    """
    Fetch the icon of a Steam game using the Steam Web API.

    Args:
    - app_id (str): The AppID of the game.

    Returns:
    - Image object: The game icon image.
    """
    #       header: `https://cdn.akamai.steamstatic.com/steam/apps/${appID}/header.jpg
    #       background: `https://cdn.akamai.steamstatic.com/steam/apps/${appID}/page_bg_generated_v6b.jpg
    #       portrait: `https://cdn.akamai.steamstatic.com/steam/apps/${appID}/library_600x900.jpg
    orignal_portait_image_path = image_path.replace(".png", ".orignal.png")
    if not os.path.exists(orignal_portait_image_path):
        with open(orignal_portait_image_path, "wb") as f:
            f.write(session.get(f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/library_600x900.jpg",
                                text=False).content)
    crop_image(orignal_portait_image_path, image_path)


def crop_image(image_path, output_path):
    """
    Crop an image by removing 150 pixels from the top and 150 pixels from the bottom.

    Args:
    - image_path (str): The path to the input image file.
    - output_path (str): The path to save the cropped image.

    Returns:
    - None
    """
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Get image dimensions
            width, height = img.size

            # Crop the image
            cropped_img = img.crop((0, 70, width, height - 70))

            # Save the cropped image
            cropped_img.save(output_path)
            print(f"Cropped image saved to {output_path}")
    except Exception as e:
        print(f"Error cropping image: {e}")


def extract_icon_from_lnk(lnk_path, output_path):
    # Read the .lnk file
    with open(lnk_path, "rb") as file:

        # Parse the .lnk file
        lnk = Lnk(file)
        # Get the icon path from the .lnk file
        icon_path = lnk.icon
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if icon_path:
            if icon_path.endswith(".exe"):
                extract_icon(icon_path, output_path)
            else:
                # Extract the icon from the .lnk file
                with open(icon_path, "rb") as icon_file:
                    icon_data = icon_file.read()

                # Write the icon data to an image file
                with open(output_path, "wb") as output_file:
                    output_file.write(icon_data)
        else:
            _session_manager.add_log(f"No icon found in the .lnk file for {lnk_path}.")
            search_and_download_icon(lnk_path.split("/")[-1], output_path)


def extract_icon(exe, icon_path: str):
    if not os.path.exists(icon_path):
        ico_x = GetSystemMetrics(SM_CXICON)

        try:
            large, small = ExtractIconEx(exe, 0)
        except Exception as e:
            _session_manager.add_log(str(e))
            return ""

        if not len(large):
            return ""

        if len(small):
            DestroyIcon(small[0])
        hdc = CreateDCFromHandle(GetDC(0))
        h_bmp = CreateBitmap()
        h_bmp.CreateCompatibleBitmap(hdc, ico_x, ico_x)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(h_bmp)
        hdc.DrawIcon((0, 0), large[0])
        bmp_str = h_bmp.GetBitmapBits(True)
        img = Image.frombuffer('RGBA', (32, 32), bmp_str, 'raw', 'BGRA', 0, 1)
        img.save(icon_path)


def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(title="Select a File",
                                           filetypes=[
                                               ("Shortcuts", "*.lnk"),
                                               ("Url Launchers", "*.url"),
                                               ("Execuatable files", "*.exe"),
                                               ("All files", "*.*")]
                                           )

    if file_path:
        print(f"Selected file: {file_path}")
        return file_path
    else:
        print("No file selected.")
        return None


app = FastAPI()


class SessionManager:
    def __init__(self):
        self.logs_folder = Config.scan_logs
        os.makedirs(self.logs_folder, exist_ok=True)
        self.session_id = "nosession"
        self.logs_file = f"./log_{datetime.datetime.now().strftime('%Y-%m-%d')}_{self.session_id}.log"

    def new_session(self):
        self.session_id = self.generate_session_id()
        self.logs_file = self.logs_folder + f"log_{datetime.datetime.now().strftime('%Y-%m-%d')}_{self.session_id}.log"
        os.makedirs(os.path.dirname(self.logs_file), exist_ok=True)

    def generate_session_id(self):
        return ""
        # while True:
        #     _id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        #     for file in os.listdir(self.logs_folder):
        #         if file.endswith(_id + '.log'):
        #             break
        #     else:
        #         break
        # return _id

    def add_log(self, content: str):
        if not os.path.exists(self.logs_file):
            with open(self.logs_file, "wt") as f:
                f.write(str(datetime.datetime.now()) + ": " + content + "\n")
            return
        with open(self.logs_file, "a") as f:
            f.write(str(datetime.datetime.now()) + ": " + content + "\n")


class Database:
    """
    This project uses sqlite database.
    This class contains utility functions for db interaction.
    """

    def __init__(self, db_path, session_manager: SessionManager):
        self.session = session_manager
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            self.create_tables()
        except sqlite3.Error as e:
            self.session.add_log(f"Error connecting to database: {e}")

    def generate_display_id(self):
        _id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while self.get_items(conditions={"display_id": _id}):
            _id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return _id

    def create_tables(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS apps (
                path TEXT, 
                name TEXT,
                added_at REAL, 
                display_id TEXT,
                launch_count INTEGER,
                last_launch REAL
            )""")
            self.conn.commit()
        except sqlite3.Error as e:
            self.session.add_log(f"Error creating table: {e}")

    def insert_data(self, table_name="apps", data=None):
        if data is None:
            self.session.add_log("No data to insert. Expected data in format: {'fieldname': 'field value'}")
            return

        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(query, tuple(data.values()))
            self.conn.commit()
        except sqlite3.Error as e:
            self.session.add_log(f"Error inserting data: {e}")

    def get_items(self, table_name="apps", columns=None, conditions=None):
        try:
            if columns is None:
                columns = '*'
            else:
                columns = ', '.join(columns)

            if conditions:
                conditions_str = ' AND '.join([f"{key} = ?" for key in conditions.keys()])
                query = f"SELECT {columns} FROM {table_name} WHERE {conditions_str}"
                self.cursor.execute(query, tuple(conditions.values()))
            else:
                query = f"SELECT {columns} FROM {table_name}"
                self.cursor.execute(query)

            rows = self.cursor.fetchall()

            # Convert rows to list of dictionaries
            items = []
            for row in rows:
                item = {}
                for i, column in enumerate(self.cursor.description):
                    item[column[0]] = row[i]
                items.append(item)

            return items
        except sqlite3.Error as e:
            self.session.add_log(f"Error retrieving data: {e}")

    def delete_data(self, table_name="apps", conditions=None):
        if conditions is None:
            self.session.add_log("No conditions provided for deletion.")
            return

        try:
            conditions_str = ' AND '.join([f"{key} = ?" for key in conditions.keys()])
            query = f"DELETE FROM {table_name} WHERE {conditions_str}"
            self.cursor.execute(query, tuple(conditions.values()))
            self.conn.commit()
        except sqlite3.Error as e:
            self.session.add_log(f"Error deleting data: {e}")

    def update_data(self, table_name="apps", data=None, conditions=None):
        if data is None or conditions is None:
            self.session.add_log("Expected data and conditions to update.")
            return

        try:
            set_str = ', '.join([f"{key} = ?" for key in data.keys()])
            conditions_str = ' AND '.join([f"{key} = ?" for key in conditions.keys()])
            query = f"UPDATE {table_name} SET {set_str} WHERE {conditions_str}"
            self.cursor.execute(query, list(data.values()) + list(conditions.values()))
            self.conn.commit()
        except sqlite3.Error as e:
            self.session.add_log(f"Error updating data: {e}")

    def close_connection(self):
        try:
            if self.conn:
                self.conn.close()
        except sqlite3.Error as e:
            self.session.add_log(f"Error closing database connection: {e}")


class AppManager:
    def __init__(self, session_manager: SessionManager):
        """
        Creates required files and folders.
        """
        self.db = Database(Config.apps_database, session_manager)
        self.session = session_manager

    def add_app(self, path="", name=""):
        """
        Adds the path to a sqlite db for displaying in the future.
        :return:
        """
        if not path:
            path = open_file_dialog()
        if not path:
            return "No file selected"
        display_id = self.db.generate_display_id()
        if not name:
            name = path.replace("\\", "/").split("/")[-1].split(".")[0]
        self.db.insert_data(data={
            "path": path,
            "name": name,
            "added_at": time.time(),
            "display_id": display_id,
            "launch_count": 0,
            "last_launch": 0,
        })
        self.session.add_log("Added New app with name: %s\npath: %s\ndisplay id: %s" % (name, path, display_id))
        return "Success"

    def app_list(self):
        """
        Fetches app list for displaying on browser.
        :return:
        """
        data = self.db.get_items(columns=["name", "display_id", "launch_count"], conditions={})
        return data

    def launch(self, display_id):
        """
        Attempts to launch the app selected in the browser.
        :return:
        """
        db = Database(Config.apps_database, _session_manager)
        app_data = db.get_items(conditions={"display_id": display_id})
        if app_data:
            app_path = app_data[0]["path"]
            command = f"\"{app_path}\""
            os.system(command)
            self.session.add_log(f"Launching app at path: {app_path}")
        db.close_connection()

    def find(self, text):
        """
        Finds app from app list containing the text in its name.
        :return:
        """
        return [item for item in self.app_list() if text.lower() in item["name"].lower()]

    def show_in_folder(self, display_id):
        """
        This function opens the folder in which the file is located (Works like Show in Folder).
        :return:
        """
        app_data = self.db.get_items(conditions={"display_id": display_id})
        if app_data:
            app_path = app_data[0]["path"]
            folder_path = os.path.dirname(app_path)
            self.session.add_log(f"Opening folder: {folder_path}")
            os.system(f"start {folder_path}")

    def remove_app(self, display_id):
        """
        Removes app from app list.
        :return:
        """
        self.db.delete_data(conditions={
            "display_id": display_id
        })

    def update_app_name(self, display_id, new_name):
        """
        Updates the name of the app.
        :return:
        """
        self.db.update_data(
            table_name="apps",
            data={"name": new_name},
            conditions={"display_id": display_id}
        )

    def return_file_icon(self, display_id):
        """
        Retrives and sends the file icon
        :return:
        """
        app_data = self.db.get_items(conditions={"display_id": display_id})
        if app_data:
            app_path = app_data[0]["path"]
            image_path = "./StormLand/images/" + display_id + ".png"
            if not os.path.exists(image_path):
                if app_path.startswith("start http"):
                    download_favicon(app_path.replace("start ", "", 1), image_path)
                elif app_path.endswith(".lnk"):
                    extract_icon_from_lnk(app_path, image_path)
                elif app_path.endswith(".url"):
                    app_path = get_url_from_url_file(app_path)
                    if app_path.startswith("steam:"):
                        extract_icon_from_steam(app_path.split("/")[-1], image_path)
                    else:
                        print(app_path)
                else:
                    extract_icon(app_path, image_path)
            if os.path.exists(image_path):
                return FileResponse(image_path)
            return FileResponse("./assets/image/256.png")


_session_manager = SessionManager()
_session_manager.new_session()
_app_manager = AppManager(_session_manager)


@app.get("/apps")
async def retrive_apps_list():
    apps = _app_manager.app_list()
    apps2 = {"favourites": [], "app_list": apps}
    resp = JSONResponse(apps2)
    resp.headers["access-control-allow-origin"] = "*"
    return resp


@app.get("/apps/add")
async def add_app():
    status = _app_manager.add_app()
    resp = JSONResponse({"status": status})
    resp.headers["access-control-allow-origin"] = "*"
    return resp


@app.get("/apps/addsite")
async def add_site(name: str, url: str):
    status = _app_manager.add_app(name=name, path="start " + url.replace(" ", "%20"))
    resp = JSONResponse({"status": status})
    resp.headers["access-control-allow-origin"] = "*"
    return resp


@app.get("/apps/image/{display_id}")
async def send_image(display_id: str):
    return _app_manager.return_file_icon(display_id)


@app.get("/apps/launch/{display_id}")
async def launch_app(display_id: str):
    # _app_manager.launch(display_id)
    threading.Thread(target=_app_manager.launch, args=(display_id,)).start()
    resp = JSONResponse({"status": "success"})
    resp.headers["access-control-allow-origin"] = "*"
    return resp


@app.get("/apps/update/{display_id}")
async def update_app(display_id: str, new_name: str):
    _app_manager.update_app_name(display_id, new_name)
    resp = JSONResponse({"status": "success"})
    resp.headers["access-control-allow-origin"] = "*"
    return resp


@app.post("/apps/update/{display_id}")
async def update_app(display_id: str, new_image: UploadFile):
    with open(f"./StormLand/images/{display_id}.png", "wb") as f:
        f.write(await new_image.read())
    resp = JSONResponse({"status": "success"})
    resp.headers["access-control-allow-origin"] = "*"
    return resp


@app.get("/apps/remove/{display_id}")
async def delete_app(display_id: str):
    _app_manager.remove_app(display_id)
    resp = JSONResponse({"status": "success"})
    resp.headers["access-control-allow-origin"] = "*"
    return resp


@app.get("/assets/{path:path}")
async def return_asset(path: str):
    return FileResponse(f"./assets/{path}")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5092)
    _app_manager.db.close_connection()
