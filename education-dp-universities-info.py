#!/usr/bin/env python
import json
from database import MongoDatabase
from duckduckpy import query
from bson import json_util

class DbTouple(object):
    def __init__(self, universityname,text, url):
        self.universityname = universityname
        self.text = text
        self.url = url
        
    def __str__(self):
        return (self.text, self.url)

class universities_infos(object):
    # DB Collection name set which will be created
    db_cm = MongoDatabase().db["education-dp-universities-info"]

    def __init__(self):
         pass  

    def import_content_universities_info(q):    
        try:       
            r = query(q)           
            # Set university Name as a query Value
            universityname=q
            # Assigned Array
            db_touples = []            
            for data in r.related_topics: 
                try:               
                    datatouple = DbTouple(universityname,data.text, data.first_url)                
                    db_touples.append(datatouple)
                except AttributeError:                    
                    for indobj in data.topics:               
                        db_touples.append(DbTouple(universityname,indobj.text, indobj.first_url))
            
            # Converting Object to Json       
            json_string = json.dumps([ob.__dict__ for ob in db_touples])
            # Loads Json Data using json_util
            data_json = json_util.loads(json_string)
            #print(data_json)            
            # Drop/Clean Collection from MongoDB
            universities_infos.db_cm.drop() 
            # Inserting into MongoDB using Batch
            universities_infos.db_cm.insert_many(data_json)
            # Database Disconnection 
            MongoDatabase().client.close()            
        except IOError:
            print("Error: can\'t find file or read data")        
        else:
            print("Written content in the MongoDB successfully")
    def test_list_documents():
        
        # number of documents in the collection
        myurls = universities_infos.db_cm.count_documents({})
        print("The number of documents in collection : ", myurls) 
        
        UniversitywisecollectionData = universities_infos.db_cm.aggregate(
            [
                # First Stage: group by
                {"$group" : 
                     {
                         "_id" : "$universityname",  
                         "UniversityWiseCount" : { "$sum": 1 }
                     }
                 },
                # 2nd Stage: sorting
                 {
                     "$sort":{"_id":1}
                 }
               ]
            )
       
        for datalist in UniversitywisecollectionData:            
            print(datalist)
        
if __name__ == "__main__": 
    q="harvard"
    universities_infos.import_content_universities_info(q)
    universities_infos.test_list_documents()  