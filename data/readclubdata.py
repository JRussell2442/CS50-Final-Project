import sqlite3
from PIL import Image
import os

connect = sqlite3.connect("project.db")
cursor = connect.cursor()

clubs = cursor.execute("SELECT name FROM clubs")
images = cursor.execute("SELECT logo FROM clubs")
print(images.fetchone()[0])


