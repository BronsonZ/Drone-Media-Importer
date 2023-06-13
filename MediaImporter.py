import os
import shutil
import datetime

src_dir = "H:\\DCIM"
dest_dir = "E:\\Dropbox\\Drone Imports"

summary_array = []

def is_image(file_path):
    img_extensions = ('.jpg', '.JPG', '.jpeg', '.JPEG', '.dng', '.DNG')
    return file_path.endswith(img_extensions)

def is_video(file_path):
    video_extensions = ('.mp4', '.MP4', '.mov', '.MOV', '.srt', '.SRT')
    return file_path.endswith(video_extensions)

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
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

def import_photos_and_videos():
    copied_files = 0
    media_src_dir = os.path.join(src_dir, "100MEDIA")
    num_files = len(os.listdir(media_src_dir))
    print("Importing Photos/Videos: " + str(num_files) + " files")
    for file in os.listdir(media_src_dir):
        src_file_path = os.path.join(media_src_dir, file)

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
            print("File " + dest_file_path + " already exists, skipping")
            continue

        if not make_dir(os.path.dirname(dest_file_path)):
            continue

        print("#" + str(copied_files+1) + "/" + str(num_files) + " Copying " + file + " to " + dest_file_path)
        
        if not copy_file(src_file_path, dest_file_path):
            continue

        print("Done copying #" + str(copied_files+1) + "/" + str(num_files) )
        copied_files += 1

    summary_array.append("MEDIA: copied " + str(copied_files) + "/" + str(num_files) + " files")
    print(summary_array[-1])

def import_panorama_or_hyperlapse(input_dir):
    src_dir_path = os.path.join(src_dir, input_dir)

    copied_dirs = 0
    num_dirs = len(os.listdir(src_dir_path))
    print("Importing: " + input_dir + " with " + str(num_dirs) + " folders")

    for sub_dir in os.listdir(src_dir_path):
        src_sub_dir_path = os.path.join(src_dir_path, sub_dir)

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
        for file in os.listdir(src_sub_dir_path):
            src_file = os.path.join(src_sub_dir_path, file)
            new_file_name = new_dir_name + " - " + file
            dest_file = os.path.join(dest_dir_path, new_file_name)

            success = True

            if os.path.exists(dest_file):
                print("File " + dest_file + " already exists, skipping")
                continue
            
            if not copy_file(src_file, dest_file):
                success = False
                continue

        if success:
            print("Fully copyied #" + str(copied_dirs+1) + "/" + str(num_dirs) )
            copied_dirs += 1

    summary_array.append(input_dir + ": fully copied " + str(copied_dirs) + "/" + str(num_dirs) + " folders")
    print(summary_array[-1])

def main():
    try:
        total_size = get_dir_size(src_dir)
        print("Total size to be coppied: " + str(round(total_size/1000000000, 1)) + "GBs")
        input("Press enter to continue, ctrl+c to exit")

        import_photos_and_videos()
        import_panorama_or_hyperlapse("PANORAMA")
        import_panorama_or_hyperlapse("HYPERLAPSE")

        print("Summary:")
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