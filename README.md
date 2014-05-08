Disease Treatment Detection in Patents
======================================

Model Used: CRF
API: Mallet [http://mallet.cs.umass.edu]

Data Set: 
---------
Patent Dataset from Patci: http://abel.lis.illinois.edu/cgi-bin/patci/patci.pl
In this code we have just added a sample of the dataset in the file: `matched_patents_final_xl_edit.txt`

Code Dependencies:
-------------------
 * Python 2.7
 * NLTK
 * MALLET
 * Flask [For Web Tool]

File Descriptions:
------------------
 * `NervousDiseases_clean.txt` - Mesh Terms related to Nervous System Diseases
 * `compunds.txt` - TREATEMENT terms based on Regex
 * `genFeatures.py` - Generate features for all the data in the training set. Store in the folder `train_data`
 * `train_all.sh` - Train the model
 * `test_all.sh` - Predict from the model
 * `accuracy.py` - Determine the accuracy, precision, recall and F1 score from the predictions

How to run:
-----------
 * Run `python genFeatures.sh`
 * Run `./train_all.sh` - Model trained and saved in `drug_disease` file
 * Run `./test_all.sh test_set.txt out_pred_5000.txt`
 * Run `python accuracy.py` - Generated all the accuracy statistics.
 * Run `data_statistics.sh` - Generates all the data statistics.

Web Tool:
---------

 * The code for the web tool is in the folder `website`. 
 * In order to run the code you need to put your abstracts for user `sneha` and `shubh` in the respective name folders.
 * The web tool runs using Flask library for python.

Contributors:
------------
 * Sneha Agarwal - sagarwa8@illinois.edu
 * Shubhanshu Mishra - smishra8@illinois.edu

