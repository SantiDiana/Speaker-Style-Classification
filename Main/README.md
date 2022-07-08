# Speaker Style Classification
This project implements an algorithm called Speaker Style Classification. It is a speech and singing voice discriminator, and it is based in this [Reference Paper](https://www.isca-speech.org/archive_v0/IberSPEECH_2018/pdfs/IberS18_O4-4_Sarasola.pdf)
This project was created within the framework of the Final Degree Project of the Universitat Politècnica de València in collaboration with Voicemod by Santiago Diana Sánchez with the help of Clara Luzón Álvarez.

# Description
The speech and singing voice discriminator is a complex algorithm that contains several parts and it is based in 2 parameters derived from musical note classification and fundamental frequency calculation. The dynamics are:
1. Implementation of a GMM based Voice Activity Detector. 
2. F0 extraction of the voiced segments.
3. Implementation of a Note Detection Algorithm, which detects if a voiced segment contains musical notes due to complying with certain conditions. 
4. Implementation of both parameters calculation scripts: NotePercentage and FramePercentage. 
5. Implementation of a SVM (Support Vector Machine) to create de Decision Function that discriminates between silence, speech and singing voice. 

Every part of the algorithm has been trained and tested with two different datasets. For the training, [Bertso Dataset](https://drive.google.com/drive/folders/17OyEclSBwmxJMEjnFbB67iY5Q5UzTiaF) has been used. It has been manually labelled by Santiago Diana Sánchez. Then, for testing, [NUS Sung and Spoken Lyrics](https://drive.google.com/drive/folders/1HX25GDzPfp1bhFWhYrZIk-oY3A0Q_wgp) has been used and also manually labelled. The training and testing of the Voice Activity Detector, Support Vector Machine and final main script have been done with this two datasets.


![Diagram](img/diagram.png)


# Installation and run of the project
For using this project, the only thing you must do is cloning this Repository in your local and install the dependencies. No datasets must be downloaded because the training parameters are already saved.

# How to run the project
The way of running the project is very easy. Once you have the present repository cloned, you must put the audio file in the "audio" folder, and you must run the main.py script.
You will get as response a vector called decision_vector, which is a vector that contains 0s,1s and 2s.

0 means silence, 1 means speech and 2 means singing voice. The decision is made by applying a frame window of 10ms, so each element of the decision_vector corresponds to a 10ms frame of the input audio file. Once you have that vector, is up to you what to do with it. 

# Explanation of the different modules
First of all, VAD.py contains the Voice Activity Detector. Then, evaluate_pitch.py, pitch_extractor.py and extractors folder contain the way to extract the f0 of every frame of the input audio file. Then, NoteDetection.py implements the Note Detection Algorithm over the f0 signal. NumberFramesPercentage.py and NotePercentage.py contain both calculations of the parameters that are used in order the make the final decision. Finally, SVM.py contains the decision function.

Parameters_silence_VAD.sav and Parameters_voice_VAD.sav contain the Voice Activity Detector parameters once trained with Bertso Dataset. finalized_model.sav contains SVM training once trained with Bertso Dataset. 

And finally main.py, which calls every other script and gives us as result the decision_vector.

Auxiliar folder contains both scripts and folders which were used all around the project to test, get metrics and charts about the project, but they are not used in the normal
functioning of the algorithm. 