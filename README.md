# Drone-Media-Importer
Simple Python script to import the photos and videos from my DJI Mini 3 Pro drone.

I am not very experienced with python so I'm sure there are plenty of improvemnets and fixes that could be made, I'm happy to take suggestions!

Source and destination folders must be changed to accommodate unique setups:

* `src_dir`: set to the DCIM folder of your SD card, likely only need to change the drive letter
* `dest_dir`: set to the destination folder, where the files will be copied to

Given the correct source and destination path, it copies each image and video with the following structure based on its creation date:

* Photos: ../Year/Month/Day/Photos
* Videos: ../Year/Month/Day/Videos
* Panoramas: ../Year/Month/Day/Panoramas
* Hyperlapses: ../Year/Month/Day/Hyperlapses

The groups of photos in panoramas and hyperlapses are kept in their corresponding folder.

All files are renamed to include the date down to the minute before the original file name, e.g. `DJI_0120.DNG` would be renamed to `2023-6-13-1310 - DJI_0120.DNG`

Panorama and hyperlapse folders are renamed to include the date and the files within the folders have that new root folder name added before their original file name.

Any file name conflicts involving an existing file are skipped to avoid any unwanted overwrites. In the future this could be improved to check if the files are actually the same or if its just that their file names happen to be equal.

I plan to update it and improve it over the next few weeks.
