#!/usr/bin/env python
import os
import glob
import pandas as pd
import json
from database import MongoDatabase

class yearly_data(object):
    # DB Collection name set which will be created
    db_cm = MongoDatabase().db["education-dp-yearly-data"]

    def __init__(self):
         pass         
     
    def import_content_yearly_data(filepath):
    
        try:                       
            # Define relative path to folder containing the text files            
            filenames = glob.glob(os.path.join(filepath ,"*.txt")) 
            datayears=[]
            files = []
            for filename in filenames:
                #print(filename)                
                if "2018" in filename:
                   # print("Year:2018")
                    files = pd.read_csv(filename, delimiter='\t' ) 
                    files['year']='2018'                    
                if "2019" in filename:
                    #print("Year:2019")
                    files = pd.read_csv(filename, delimiter='\t' ) 
                    files['year']='2019'                     
                if "2020" in filename:
                     #print("Year:2020")
                     files = pd.read_csv(filename, delimiter='\t' ) 
                     files['year']='2020'  
                #Years Data Append to one array      
                datayears.append(files)
                
            #print(datayears) 
            
            # Concatenate dataframe list and set all values as a string
            data = pd.concat(datayears).astype('str') 
            # Remove the Default indexation and NaN value replace with null 
            data.to_string(index=False)
            data.dropna(inplace = True)
            #print(data)
            # Converted pandas data to json format for inserting to MongoDB
            data_json = json.loads(data.to_json(orient='records'))
            #print (data_json)
            # Drop/Clean Collection from MongoDB
            yearly_data.db_cm.drop() 
            # Inserting into MongoDB using Batch
            yearly_data.db_cm.insert_many(data_json)
            # Database Disconnection 
            MongoDatabase().client.close()
        # Exception
        except IOError:
            print("Error: can\'t find file or read data")
        else:
            print("Written content in the MongoDB successfully")
    
   
    
    def test_list_documents():
        
        # number of documents in the collection
        mydoc = yearly_data.db_cm.count_documents({})
        print("The number of documents in collection : ", mydoc) 
        
        YearwisecollectionData = yearly_data.db_cm.aggregate(
            [
                # First Stage: group by
                {"$group" : 
                     {
                         "_id" : "$year",  
                         "YearWiseCount" : { "$sum": 1 }
                     }
                 },
                # 2nd Stage: sorting
                 {
                     "$sort":{"_id":1}
                 }
               ]
            )
       
        for datalist in YearwisecollectionData:            
            print(datalist)
    
    
if __name__ == "__main__":
  filepath = 'C:\python_practice\education-dp-exercise-simplified'  #pass csv file path
  yearly_data.import_content_yearly_data(filepath)
  yearly_data.test_list_documents()
 