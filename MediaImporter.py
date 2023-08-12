import os
import shutil
import datetime

src_dir = str()
dest_dir = str()
temp_dir = str()

summary_array = []

def is_image(file_path):
    img_extensions = ('.jpg', '.JPG', '.jpeg', '.JPEG', '.dng', '.DNG')
    return file_path.endswith(img_extensions)

def is_video(file_path):
    video_extensions = ('.mp4', '.MP4', '.mov', '.MOV', '.srt', '.SRT')
    return file_path.endswith(video_extensions)

def get_dir_size(path):
    total = 0
    with os.scandir(path) as dir:
        for entry in dir:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def copy_file(src_file_path, dest_file_path):
    try:
        shutil.copy2(src_file_path, dest_file_path)
        return True
    except (shutil.Error, FileNotFoundError) as e:
        print("Error copying file " + src_file_path + " to " + dest_file_path + " | Error: " + str(e))
        return False
    
def make_dir(path):
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except OSError as e:
        print("Error creating directory " + path + " | Error: " + str(e))
        return False

def get_creation_time(file_path):
    creation_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    year = str(creation_time.year)
    month = str(creation_time.month) + ' - ' + creation_time.strftime("%B")
    day = str(creation_time.day) + ' - ' + creation_time.strftime("%A")
    return creation_time, year, month, day

def equal_file_size(src_file_path, dest_file_path):
    src_size = os.path.getsize(src_file_path)
    dest_size = os.path.getsize(dest_file_path)
    return src_size == dest_size

def import_photos_and_videos(input_dir):
    copied_files = 0
    media_src_dir = os.path.join(src_dir, input_dir)
    num_files = len(os.listdir(media_src_dir))
    print("Importing Photos/Videos: " + str(num_files) + " files")
    for file in os.listdir(media_src_dir):
        src_file_path = os.path.join(media_src_dir, file)

        if not os.path.isfile(src_file_path):
            print("Directory " + file + " is not a file, skipping")
            num_files -= 1
            continue

        creation_time, year, month, day = get_creation_time(src_file_path)

        date_string = creation_time.strftime("%Y-%m-%d-%H%M")
        new_file_name = date_string + " - " + file

        if is_image(src_file_path):
            dest_file_path = os.path.join(dest_dir, year, month, day, "Photos", new_file_name)
        elif is_video(src_file_path):
            dest_file_path = os.path.join(dest_dir, year, month, day, "Videos", new_file_name)
        else:
            print("File " + file + " is not an image or video, skipping")
            num_files -= 1
            continue

        if os.path.exists(dest_file_path):
            if equal_file_size(src_file_path, dest_file_path):
                print("#" + str(copied_files+1) +" File " + dest_file_path + " already exists, skipping")
                copied_files += 1
                continue
            else:
                print("#" + str(copied_files+1) +" File " + dest_file_path + " already exists, but has different size, copying anyway, saving original file to " + temp_dir)
                if not make_dir(temp_dir):
                    continue
                temp_file_path = os.path.join(temp_dir, new_file_name)
                copy_file(dest_file_path, temp_file_path)

        if not make_dir(os.path.dirname(dest_file_path)):
            continue

        print("#" + str(copied_files+1) + "/" + str(num_files) + " Copying " + file + " to " + dest_file_path)
        
        if copy_file(src_file_path, dest_file_path):
            print("Done copying #" + str(copied_files+1) + "/" + str(num_files) )
            copied_files += 1

    summary_array.append("Photos/Videos: copied " + str(copied_files) + "/" + str(num_files) + " files")
    print(summary_array[-1])

def import_panorama_or_hyperlapse(input_dir):
    src_dir_path = os.path.join(src_dir, input_dir)

    copied_dirs = 0
    num_dirs = len(os.listdir(src_dir_path))
    print("Importing: " + input_dir + " with " + str(num_dirs) + " folders")

    for sub_dir in os.listdir(src_dir_path):
        src_sub_dir_path = os.path.join(src_dir_path, sub_dir)
        
        if not os.path.isdir(src_sub_dir_path):
            print("File " + sub_dir + " is not a directory, skipping")
            num_dirs -= 1
            continue

        creation_time, year, month, day = get_creation_time(src_sub_dir_path)

        date_string = creation_time.strftime("%Y-%m-%d")
        new_dir_name = date_string + " - " + sub_dir

        if input_dir == "PANORAMA":
            dest_dir_path = os.path.join(dest_dir, year, month, day, "Panoramas", new_dir_name)
        else:
            dest_dir_path = os.path.join(dest_dir, year, month, day, "Hyperlapses", new_dir_name)
        
        if not make_dir(dest_dir_path):
            continue

        print("#" + str(copied_dirs+1) + "/" + str(num_dirs) + " Copying " + sub_dir + " to " + dest_dir_path)
        success = True
        for file in os.listdir(src_sub_dir_path):
            src_file = os.path.join(src_sub_dir_path, file)

            if not os.path.isfile(src_file):
                print( file + " is not a file, skipping")
                continue

            new_file_name = new_dir_name + " - " + file
            dest_file = os.path.join(dest_dir_path, new_file_name)

            if os.path.exists(dest_file):
                if equal_file_size(src_file, dest_file):
                    print("File " + dest_file + " already exists, skipping")
                    continue
                else:
                    print("File " + dest_file + " already exists, but has different size, copying anyway, saving original file to temp folder")
                    make_dir(temp_dir)
                    temp_file_path = os.path.join(temp_dir, new_file_name)
                    copy_file(dest_file, temp_file_path)
            
            if not copy_file(src_file, dest_file):
                success = False
                continue


        if success:
            print("Fully copyied #" + str(copied_dirs+1) + "/" + str(num_dirs) )
            copied_dirs += 1

    summary_array.append(input_dir + ": fully copied " + str(copied_dirs) + "/" + str(num_dirs) + " folders")
    print(summary_array[-1])

def call_function_with_directory(func, directory):
    if os.path.isdir(os.path.join(src_dir, directory)):
        func(directory)
    else:
        print("Directory " + directory + " does not exist or is not a directory, skipping")

def main():
    try:
        global src_dir
        global dest_dir
        global temp_dir

        src_dir_letter = input("Enter the drive letter of the source drive: ").upper()
        src_dir = src_dir_letter + ":\\DCIM"
        
        dest_dir_letter = input("Enter the drive letter of the destination drive: ").upper()
        dest_dir = dest_dir_letter + ":\\Dropbox\\Drone Imports"

        temp_dir = os.path.join(dest_dir, "TEMP")

        if not os.path.exists(src_dir) or not os.path.isdir(src_dir):
            print("Source directory " + src_dir + " does not exist or is not a directory")
            input("Press enter to exit")
            exit()
        
        total_size = get_dir_size(src_dir)
        print("Source directory: " + src_dir)
        print("Destination directory: " + dest_dir)
        print("Total size to be copied: " + str(round(total_size/1000000000, 1)) + "GB")

        valid_yes_input = "y", "Y", "yes", "Yes", "YES", ""

        do_continue = input("Do you want to continue? (Y,n) :")

        if do_continue not in valid_yes_input:
            print("Program stopped")
            exit()

        call_function_with_directory(import_photos_and_videos, "100MEDIA")
        call_function_with_directory(import_panorama_or_hyperlapse, "PANORAMA")
        call_function_with_directory(import_panorama_or_hyperlapse, "HYPERLAPSE")

        print("Summary:")
        if summary_array == []:
            print("Nothing was copied")
            input("Press enter to exit")
            exit()
        else:
            for line in summary_array:
                print(line)
        
        input("Program finished, press enter to exit")
        exit()
    except KeyboardInterrupt:
        print("User interrupted, program stopped")
        input("Press enter to exit")
        exit()

if __name__ == "__main__":
    main()