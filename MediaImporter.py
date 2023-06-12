import os
import shutil
import datetime

src_dir = "H:\\DCIM"
dest_dir = "E:\\Dropbox\\Drone Imports"

summary_array = []

def is_image(file_path):
    img_extensions = ('.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG', '.gif', '.GIF', '.dng', '.DNG')
    return file_path.endswith(img_extensions)

def is_video(file_path):
    video_extensions = ('.mp4', '.MP4', '.mov', '.MOV', '.srt', '.SRT')
    return file_path.endswith(video_extensions)

def import_media():
    copied_files = 0
    media_src_dir = os.path.join(src_dir, "100MEDIA")
    num_files = len(os.listdir(media_src_dir))
    print("Importing Media: " + str(num_files) + " files")
    for file in os.listdir(media_src_dir):
        src_file_path = os.path.join(media_src_dir, file)

        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(src_file_path))

        year = str(creation_time.year)
        month = str(creation_time.month) + ' - ' + creation_time.strftime("%B")
        day = str(creation_time.day) + ' - ' + creation_time.strftime("%A")

        if is_image(src_file_path):
            dest_file_path = os.path.join(dest_dir, year, month, day, "Photos", file)
        elif is_video(src_file_path):
            dest_file_path = os.path.join(dest_dir, year, month, day, "Videos", file)
        else:
            print("File " + file + " is not an image or video, skipping")
            num_files -= 1
            continue

        if os.path.exists(dest_file_path):
            print("File " + dest_file_path + " already exists, skipping")
            continue

        try:
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
        except OSError as e:
            print("Error creating directory: " + str(e))
            continue

        try:
            print("#" + str(copied_files+1) + "/" + str(num_files) + " Copying " + file + " to " + dest_file_path)
            shutil.copy2(src_file_path, dest_file_path)
            print("Done copying #" + str(copied_files+1) + "/" + str(num_files) )
            copied_files += 1
        except shutil.Error as e:
            print("Error copying file: " + str(e))
            continue
    print("Finished, copied " + str(copied_files) + "/" + str(num_files) + " files")
    summary_array.append("MEDIA: copied " + str(copied_files) + "/" + str(num_files) + " files")

def import_panorama_and_hyperlapse():
    print("Importing Panoramas and Hyperlapses")
    
    for dir in os.listdir(src_dir):

        if dir != "PANORAMA" and dir != "HYPERLAPSE":
            continue

        src_dir_path = os.path.join(src_dir, dir)

        copied_dirs = 0
        num_dirs = len(os.listdir(src_dir_path))
        print("Importing: " + dir + " " + str(num_dirs) + " directories")

        for sub_dir in os.listdir(src_dir_path):
            src_sub_dir_path = os.path.join(src_dir_path, sub_dir)

            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(src_sub_dir_path))

            year = str(creation_time.year)
            month = str(creation_time.month) + ' - ' + creation_time.strftime("%B")
            day = str(creation_time.day) + ' - ' + creation_time.strftime("%A")

            if dir == "PANORAMA":
                dest_dir_path = os.path.join(dest_dir, year, month, day, "Panoramas", sub_dir)
            else:
                dest_dir_path = os.path.join(dest_dir, year, month, day, "Hyperlapses", sub_dir)

            if os.path.exists(dest_dir_path):
                print("Directory " + dest_dir_path + " already exists, skipping")
                continue

            try:
                os.makedirs(os.path.dirname(dest_dir_path), exist_ok=True)
            except OSError as e:
                print("Error creating directory: " + str(e))
                continue

            try:
                print("Copying " + sub_dir + " to " + dest_dir_path)
                shutil.copytree(src_sub_dir_path, dest_dir_path, copy_function=shutil.copy2, dirs_exist_ok=False)
                print("Done copying " + sub_dir)
                copied_dirs += 1
            except FileExistsError as e:
                print("Error copying directory: " + str(e))
                continue
            except shutil.Error as e:
                print("Error copying directory: " + str(e))
                continue
        print("Finished " + dir + ", copied " + str(copied_dirs) + "/" + str(num_dirs) + " directories")
        summary_array.append(dir + ": copied " + str(copied_dirs) + "/" + str(num_dirs) + " directories")
    print("Finished importing panoramas and hyperlapses")

try:
    import_media()
    import_panorama_and_hyperlapse()
    print("Summary:")
    for line in summary_array:
        print(line)
    input("Program finished, press enter to exit")
    exit()
except KeyboardInterrupt:
    print("User interrupted, closing program")
    input("Press enter to exit")
    exit()