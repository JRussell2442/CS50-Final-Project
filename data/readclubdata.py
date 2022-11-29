import sqlite3
from PIL import Image
import os

connect = sqlite3.connect("project.db")
cursor = connect.cursor()

clubs = cursor.execute("SELECT * FROM clubs")
club1 = clubs.fetchone()
club1img = club1[2]
img = Image.open("Club Logos/"+club1img)
img.show()
print(club1[1])


