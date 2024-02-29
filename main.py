from datetime import datetime
import piexif
import os


def extract_date(filename):
    date_time_str = filename.split('@')[1].split('.')[0]
    date_time = datetime.strptime(date_time_str, "%d-%m-%Y_%H-%M-%S")
    return date_time.strftime("%Y:%m:%d %H:%M:%S")


def modify_date_taken(filename, new_date):
    try:
        exif_dict = piexif.load(filename)
        exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, filename)
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error modifying Date Taken metadata for {filename}: {e}")


image_directory = 'ChatExport/photos/'

for filename in os.listdir(image_directory):
    if filename.lower().endswith(('.jpg', '.jpeg')):
        image_path = os.path.join(image_directory, filename)
        new_date = extract_date(filename)
        if new_date:
            modify_date_taken(image_path, new_date)
        else:
            print(f"Invalid filename format: {filename}")
