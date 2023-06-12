import os
import shutil
import datetime

src_dir = "H:\\DCIM\\100MEDIA"
dest_dir = "E:\\Dropbox\\Drone Imports"

def is_image(file_path):
    img_extensions = ('.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG', '.gif', '.GIF', '.dng', '.DNG')
    return file_path.endswith(img_extensions)

def is_video(file_path):
    video_extensions = ('.mp4', '.MP4', '.mov', '.MOV', '.srt', '.SRT')
    return file_path.endswith(video_extensions)

count = 0

num_files = len(os.listdir(src_dir))

try:
    for file in os.listdir(src_dir):
        src_file_path = os.path.join(src_dir, file)

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
            num_files -= 1
            continue

        os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
        
        try:
            print("#" + str(count+1) + "/" + str(num_files) + " Copying " + file + " to " + dest_file_path)
            shutil.copy2(src_file_path, dest_file_path)
            print("Done copying #" + str(count+1) + "/" + str(num_files) )
            count += 1
        except shutil.Error as e:
            print("Error copying file: " + str(e))
            num_files -= 1
            continue

    print("Finished, copied " + str(count) + "/" + str(num_files))

except KeyboardInterrupt:
    print("User interrupted, closing program, copied " + str(count) + "/" + str(num_files))
    exit()


