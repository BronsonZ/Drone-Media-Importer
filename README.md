# Drone-Media-Importer
Simple Python script to import the photos and videos from my DJI Mini 3 Pro drone. 

Source and destination folders can be changed easily to accomodate unique setups:
- "src_dir": set to the DCIM folder of your SD card, likely only need to change the drive letter
- "dest_dir": set to the destination folder, where the files will be copied to

Files are imported with the following structures
- Photos: ../Year/Month/Day/Photos
- Videos: ../Year/Month/Day/Videos
- Panoramas: ../Year/Month/Day/Panoramas
- Hyperlapses: ../Year/Month/Day/Hyperlapses

File names are not changed, though that could be something I add later
