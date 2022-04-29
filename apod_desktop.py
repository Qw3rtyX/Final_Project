""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py image_dir_path [apod_date]

Parameters:
  image_dir_path = Full path of directory in which APOD image is stored
  apod_date = APOD image date (format: YYYY-MM-DD)

History:
  Date        Author          Description
  2022-04-28  Serena Hunter   Initial creation
"""
from sys import argv, exit
from datetime import datetime, date
from hashlib import sha256
from os import path
import requests
import hashlib
from PIL import Image
import glob
import nasapy
from datetime import datetime
from IPython.display import Image
import mysql
import ctypes

def main():

    # Determine the paths where files are stored
    image_dir_path = get_image_dir_path()
    db_path = path.join(image_dir_path, 'apod_images.db')

    # Get the APOD date, if specified as a parameter
    apod_date = get_apod_date()

    # Create the images database if it does not already exist
    create_image_db(db_path)

    # Get info for the APOD
    apod_info_dict = get_apod_info(apod_date)
    
    # Download today's APOD
    image_url = "AMq6ZJ4JLjJ2bezsRV87VgajuVqwXm7eP0KCvE80"
    image_msg = download_apod_image(image_url)
    with open(image_msg, "rb") as f:
        bytes = f.read()
        image_sha256 = hashlib.sha256(bytes).hexdigest()
    image_size = Image.open(image_msg)
    width = image_size.width
    height = image_size.height
    Total_image_size = width, height
    image_path = get_image_path(image_url, image_dir_path)

    # Print APOD image information
    print_apod_info(image_url, image_path, Total_image_size, image_sha256)

    # Add image to cache if not already present
    if not image_already_in_db(db_path, image_sha256):
        save_image_file(image_msg, image_path)
        add_image_to_db(db_path, image_path, image_size, image_sha256)

    # Set the desktop background image to the selected APOD
    set_desktop_background_image(image_path)

def get_image_dir_path():
    """
    Validates the command line parameter that specifies the path
    in which all downloaded images are saved locally.

    :returns: Path of directory in which images are saved locally
    """
    if len(argv) >= 2:
        dir_path = argv[1]
        if path.isdir(dir_path):
            print("Images directory:", dir_path)
            return dir_path
        else:
            print('Error: Non-existent directory', dir_path)
            exit('Script execution aborted')
    else:
        print('Error: Missing path parameter.')
        exit('Script execution aborted')

def get_apod_date():
    """
    Validates the command line parameter that specifies the APOD date.
    Aborts script execution if date format is invalid.

    :returns: APOD date as a string in 'YYYY-MM-DD' format
    """    
    if len(argv) >= 3:
        # Date parameter has been provided, so get it
        apod_date = argv[2]

        # Validate the date parameter format
        try:
            datetime.strptime(apod_date, '%Y-%m-%d')
        except ValueError:
            print('Error: Incorrect date format; Should be YYYY-MM-DD')
            exit('Script execution aborted')
    else:
        # No date parameter has been provided, so use today's date
        apod_date = date.today().isoformat()
    
    print("APOD date:", apod_date)
    return apod_date

def get_image_path(image_url, dir_path):
    """
    Determines the path at which an image downloaded from
    a specified URL is saved locally.

    :param image_url: URL of image
    :param dir_path: Path of directory in which image is saved locally
    :returns: Path at which image is saved locally
    """
    image_url = []
    for dir_path in glob.glob('C:\Users\seren\Desktop\Scripting Applications\Final_Project'):
        im=Image.open(dir_path)
        image_url.append(im)
    return dir_path

def get_apod_info(date):
    """
    Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    :param date: APOD date formatted as YYYY-MM-DD
    :returns: Dictionary of APOD info
    """    
    #Initialize Nasa class by creating an object:

    k = "AMq6ZJ4JLjJ2bezsRV87VgajuVqwXm7eP0KCvE80"
    nasa = nasapy.Nasa(key = k)

    #Get today's date in YYYY-MM-DD format:
    date = datetime.today().strftime('%Y-%m-%d')

    #Get the image data:
    apod = nasa.picture_of_the_day(date=date, hd=True)
    return {"date" : "apod"}

def print_apod_info(image_url, image_path, image_size, image_sha256):
    """
    Prints information about the APOD

    :param image_url: URL of image
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """    
    print(image_url, image_path, image_size, image_sha256)
    return None

def download_apod_image(image_url):
    """
    Downloads an image from a specified URL.

    :param image_url: URL of image
    :returns: Response message that contains image data
    """
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    return "img_data"

def save_image_file(image_msg, image_path):
    """
    Extracts an image file from an HTTP response message
    and saves the image file to disk.

    :param image_msg: HTTP response message
    :param image_path: Path to save image file
    :returns: None
    """
    image_msg = "img_data"
    response = requests.get(image_msg)
    image_path = "C:\Users\seren\Desktop\Scripting Applications\Final_Project"
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
    return None

def create_image_db(db_path):
    """
    Creates an image database if it doesn't already exist.

    :param db_path: Path of .db file
    :returns: None
    """
    # Convert binary data to proper format and write it on Hard Disk
    with open(get_image_path, 'wb') as db_path:
        db_path.write(Image)
    return None

def add_image_to_db(db_path, image_path, image_size, image_sha256):
    """
    Adds a specified APOD image to the DB.

    :param db_path: Path of .db file
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """
    #establish the connection
    connection = mysql.connector.connect(
        user='root', password='password', host='localhost', database='Final_Project_DB'
    )

    #Creating cursor object using cursor() method
    cursor = connection.cursor()

    #Dropping Nasa table if already exists.
    cursor.execute("DROP TABLE IF EXISTS NASA")

    sql_fetch_blob_query = """SELECT * from Final_Project_DB where Image = %s"""

    cursor.execute(sql_fetch_blob_query, (Image,))
    record = cursor.fetchall()
    for row in record:
        create_image_db(Image, db_path)
        create_image_db(Image, image_path)
        create_image_db(Image, image_size)
        create_image_db(Image, image_sha256)
    cursor.execute(record)
    return None

def image_already_in_db(db_path, image_sha256):
    """
    Determines whether the image in a response message is already present
    in the DB by comparing its SHA-256 to those in the DB.

    :param db_path: Path of .db file
    :param image_sha256: SHA-256 of image
    :returns: True if image is already in DB; False otherwise
    """ 
    db_path = "C:\Users\seren\Desktop\Scripting Applications\Final_Project\Final_Project_DB.sql"
    image_sha256 = image_sha256
    {
        using (SqlCommand cmd = new SqlCommand("SELECT COUNT(0) FROM Final_Project_DB WHERE ImageHash = @ImageHash", connection))
        {
            connection.Open();
            int imagecount = (int)cmd.ExecuteScalar();
            result = imagecount == 0;
            connection.Close();
        }
    }

    return(result);
}

def set_desktop_background_image(image_path):
    """
    Changes the desktop wallpaper to a specific image.

    :param image_path: Path of image file
    :returns: None
    """
    path = "C:\Users\seren\Desktop\Scripting Applications\Final_Project\Final_Project_DB.sql"
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path , 0)
    return None

main()