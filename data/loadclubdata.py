import csv
import sqlite3

connect = sqlite3.connect("project.db")
cursor = connect.cursor()

file = open('Clubs.csv')
csvreader = csv.reader(file)

header = []
header = next(csvreader)

for row in csvreader:
    club_name = row[1]
    
    # Cut the first part of the image path if it's leftover from web scraping
    cut_path = "harvard/2022/"
    cut_path2 = "images/"
    if cut_path in row[2]:
        logo_path = row[2].split(cut_path)[1]
    elif cut_path2 in row[2]:
        logo_path = row[2].split(cut_path2)[1]
    # Some image paths don't need to be trimmed
    else:
        logo_path = row[2]
    # LOAD DATA
    cursor.execute("INSERT INTO clubs (name, logo) VALUES (?, ?)", [club_name, logo_path])
# CLEAR DATA
#cursor.execute("DROP TABLE clubs")
#cursor.execute("CREATE TABLE clubs (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, logo TEXT NOT NULL)")

connect.commit()