# Pedestrian-Attributes-Annotation-Tool

# Requirements:

* Python3

* Tkinter

* Pillow

# Setup for linux(ununtu):

* sudo apt install python3-pip

* sudo apt-get install python3-tk

* pip3 install Pillow

# Setup for Windows

* Python3 
1.Download windows compatible python3 exe file from here: https://www.python.org/downloads/
2.Run the Python Installer once downloaded. 
3.Select Install Now – the recommended installation options.



4.The next dialog will prompt you to select whether to Disable path length limit. No need to do it though it will allow Python to bypass the 260-character MAX_PATH limit. Effectively, it will enable Python to use long path names.
5.Open cmd and type: **python**. It should open python compiler in cmd if every thing installed correctly. Exit the terminal using **exit()** command.

* Tkinter
6. Install pillow using : **pip install Pillow**

# How to use this tool?

1. Execute run.py 
2. There should be folder named **Images** where all the images should be store which you need to label
3. Once annotatoion window pops up, click on load. It will directly upload images in the **Images** folder one by one.
4. Annotate images with labels in the dropdown provided.
5. Once you annotate the images click on next. It will automatically then save the labels for that particular image.
6. You can go back to any image and re-annotate them and click on next to update.
7. If you quit the run.py in between. You can load the images in the same manner as mentioned in step2, after which you can just go to the required image either by hitting next      till you arrive at that image (while doing so you will see that the images you annotated are already saved). Secondly, you can directly mention image number in got to image        option.

# Warning : In the same directory there will be folder named Labels where all the annotations will be saved. Never delete that.
