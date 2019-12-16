##### aimldl > documents > web_videos > bash_scripts > README.md
* Rev.1: 2019-12-16 (Mon)
* Draft: 2019-12-12 (Thu)

### README.md
This directory has several utility programs to process web videos.

This directory is supposed to be a subset of "aimldl > computing_environments > bash > scripts". Only relevant scripts are selectively copied to this directory for convenience.

#### TODO
##### 2019-12-12 (Thu)
Write a Bash script that renames missing file names in order.
I deleted IMG_8927-500-60.PNG and IMG_8922-500_60.PNG.
So I have renamed all the file names from IMG_8928-500-60.PNG
  because it makes things easier eventually. That is,

> IMG_8928-500-60.PNG -> IMG_8927-500-60.PNG
IMG_8929-500-60.PNG -> IMG_8928-500-60.PNG
  ...

Let's automate this.


##### On the iPhone,
Step 1. Screencapture the screens.
Step 2. Move all the images to Google Drive's _temp directory.
        _temp contains nothing but the screencaptured images.
        Google Drive is used as a temporary storage to move the images to a computer.
##### On a computer,
Step 3. Download all the images.
        Google Drive zips the image files into a single archived file.
Step 4. Uncompress the zip file and move all the image files to the input directory.
Step 5. cd to directory where this script exists.
Step 6. TODO: Run a script to organize the file names.
The file names up to IMG_9100.PNG have consecutive numbers. Some files are deleted after capturing the screens. The numbers in the file names are changed so that all the file names have consecutive numbers.
<img src="images/all_image_files.png">
Step 7. Run iphone2web. Comment the line with the eval command to test the commands and uncomment the line to actually run it.
Step 8.

##### Example
```bash
  ~/aimldl/documents/web_videos/bash_scripts$ ./iphone2web
  convert input/IMG_9095.PNG -resize 500 -quality 60 output/IMG_9095.PNG
  convert input/IMG_9096.PNG -resize 500 -quality 60 output/IMG_9096.PNG
    ...
  convert input/IMG_9110.PNG -resize 500 -quality 60 output/IMG_9110.PNG
  <img src='images/IMG_9095.PNG'>
  <img src='images/IMG_9096.PNG'>
    ...
  <img src='images/IMG_9110.PNG'>

  ~/aimldl/documents/web_videos/bash_scripts$
```
23.1MB -> 1.9MB

change_file_names is not necessary. So delete it after taking out some necessary parts.
