# cascade_haar_classifier
 Training cascade Haar classified step-by-step on user data

## Step 1 - Create negative and positive samples

- Positive samples - contain an object of intereset that needs to be recognized by cascade haar classifier.
- Negative samples - similar images but without objects to be recognized.

Run APP.py. Positive and Negative samples directories will autofill.
![image](https://user-images.githubusercontent.com/24581566/150626859-722a6083-35d8-4878-8e65-641d340007db.png)

Open \*.mp4 source file.
![image](https://user-images.githubusercontent.com/24581566/150626883-621c59fa-5db3-4ad2-aab5-3bacbe2cdf2e.png)

Scroll through the video file frames using Previous and Next buttons. 

- To save a Negative sample just press Save button. As a result, the current frame will be saved as \*.bmp file in /training/samples/negative/rawdata. Also, info.txt file will be created if does not exist yet in /training/samples/negative. Inside the info.txt file a new line will be added ```\rawdata\mp3filename_framecount.bmp```.
- To save a Positive sample click Add ROI (Rectangle Of Interest). In a newly opened window drag a rectangle around the object.
![image](https://user-images.githubusercontent.com/24581566/150626930-7e05b39b-650a-41ac-b162-03e52cff90fb.png)
Press Enter. In the main window a green rectangle around the object will appear.
![image](https://user-images.githubusercontent.com/24581566/150626934-7cc380de-9552-4b8b-b776-67a995af3e8d.png)
The ROI data can be removed by clicking Remove ROI.
Multiple ROI can be added from the same image.
Click Save button. As a result, the current frame will be saved as \*.bmp file in /training/samples/positive/rawdata. Also, info.txt file will be created if does not exist yet in /training/samples/positive. Inside the info.txt file a new line will be added ```\rawdata\mp3filename_framecount.bmp ROIindex ROIx ROIy ROIw ROIh```.

## Step 2 - Create vector of positive samples

Open 00_samples_creation.bat in training folder. Its content is like:
```createsamples.exe -info samples/positive/info.txt -vec vector/objectvector.vec -num 114 -w 20 -h 20
pause```
The parameters are:
- -info relative path to info.txt inside positive samples folder
- -vec relative path to output vector file
- -num number of positive samples
- -w width of object in pixels
- -h height of object in pixels

Close the 00_samples_creation.bat and run it. To run creatsample.exe following files are needed as well cv097.dll, cxcore097.dll, highgui097.dll, and libguide40.dll.
CMD should show a similar result:
![image](https://user-images.githubusercontent.com/24581566/150627011-a20000fc-d2ff-4413-8a69-9b4fe68b65ae.png)
Also objectvector.vec file will be created in vector folder.

## Step 3 - Haar training

Open 01_haar_training.bat in training folder. Its content is like:
```haartraining.exe -data cascades -vec vector/objectvector.vec -bg samples/negative/info.txt -npos 114 -nneg 78 -nstages 15 -mem 1024 -mode ALL -w 20 -h 20
pause```

-data       cascades path for storing the cascade of classifiers
-vec        path which points the location of vector file
-bg         path which points to info.txt file of negative samples
-npos       number of positive samples ≤ no. positive bmp files
-nneg       number of negative samples (patches) - has to be greater than or equal to number of positive samples
-nstages    number of intended stages for training
-mem        memory assigned in MB
-mode       check literature for more info about this parameter
-w          width of object in pixels - must be the same as in 00_samples_creation.bat
-h          height of object in pixels - must be the same as in 00_samples_creation.bat
-nonsym     use this parameter without argument if the object is not horizontally symmetrical

Close the 01_haar_training.bat and run it. To run haartraining.exe following files are needed as well cv097.dll, cxcore097.dll, highgui097.dll, and libguide40.dll.
CMD should show a similar result: