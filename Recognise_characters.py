import pickle
import numpy
import os
import scipy.special
import os, sys

#A Python Script That Loads the Neural Network's Memory from the pickle file and Recognises the Characters
#The characters are stored as Datasets in the Form of CSV file using the method character_segmentation (automatic_license_plate_recognition.py)

#Create a list to store networks answer
answers=[]

def recognition():


    #Loading the Trained Value of weights so that we need not train our neural Network everytime we have to use it
    input_wih = open(os.path.join(sys.path[0],"weights_wih.pkl"), 'rb')
    input_who = open(os.path.join(sys.path[0],"weights_who.pkl"), 'rb')

    wih = pickle.load(input_wih)
    who = pickle.load(input_who)

    #After saving the values of weights into 2 variables, we close the file accordingly
    input_wih.close()
    input_who.close()

    #Define an Activation Function for each Nodes. I have chosen sigmoid Function as the Activation Function
    activation_function = lambda x: scipy.special.expit(x)


    #A Function to Apply the Trained Neural Network's learning to the Characters so seperated In order to Recognise them
    def query(inputs_list):

        #convert inputs list into 2D array
        inputs= numpy.array(inputs_list, ndmin=2).T

        #Calculate signals into the Hidden Layer
        hidden_inputs= numpy.dot(wih, inputs)
        #Calculate the signals emerging from the Hidden layer
        hidden_outputs= activation_function(hidden_inputs)

        #Calculate the signal into the final output layer
        final_inputs= numpy.dot(who, hidden_outputs)

        #Calculate the signal emerging from the final output layer
        final_outputs= activation_function(final_inputs)

        return final_outputs



    #Testing the Neural Network
    answers.clear()

    #Since each Character is saved in 1 CSV file, we process all files in that directory which ends with .csv
    path= os.path.join(sys.path[0],'bike')
    files= os.listdir(path)

    for filename in files:
        if filename.endswith('.csv'):

            file_name = os.path.join(path, filename)
            characters_count=1

            #Test the Neural Network
            #Opening Test dataset CSV file from the folder where where query dataset is saved

            test_data_file= open(file_name, 'r')
            test_data_list= test_data_file.readlines()
            test_data_file.close()

            #Go through all the records in the Test dataset
            for record in test_data_list:

                # Split the record by ','
                all_values = record.split(',')

                #Scale and shift the inputs
                inputs= (numpy.asfarray(all_values[:-1])/255.0 *0.99)+0.01

                #Query the Network
                outputs= query(inputs)

                #The index of the highest value corresponds to the label
                label= numpy.argmax(outputs)

                #print("Network's Answer: ", label)

                answers.append(label)




