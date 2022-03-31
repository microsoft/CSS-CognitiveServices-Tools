from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import pandas as pd

def createKBUsingSearch(endpoint, key, index_name):

    #basic validation check
    validateEndpointKey(endpoint, key, index_name)

    credential = AzureKeyCredential(key)
    client = SearchClient(endpoint=endpoint,
                      index_name=index_name,
                      credential=credential)
    
    results = client.search(search_text="*", include_total_count=True)

    KBDataFrame = pd.DataFrame(columns=['KbId','Questions','Answer','Source','Metadata','SuggestedQuestions','IsContextOnly','Prompts','QnaId'])
    
    try:
        tempDict = {}
        print ('Total questions found:', results.get_count())
        kbLen = len(index_name)
        print("Fetching Rows...")
        for result in results:
            
            #check the question status
            # if it is deleted then we don't need to consider this question
            if 'changeStatus' in result:
                if result["changeStatus"] == "Delete":
                    continue

            tempDict["Questions"] = result["questions"]
            tempDict["Answer"] = result["answer"]
            tempDict["Source"] = result["source"]
            tempDict["IsContextOnly"] = result["isContextOnly"]
            tempDict["SuggestedQuestions"] = []
            tempDict["Prompts"] = result["prompts"]

            keyName = sorted(result.keys())

            #if Kb is published then kbId won't be present
            #storing KbId in df to split excel sheet based on different values
            if "kbId" in keyName:
                tempDict["QnaId"] = result["id"]
                tempDict["KbId"] = result["kbId"]
            else:
                tempDict["QnaId"] = result["id"][kbLen:]
                tempDict["KbId"] = index_name
            
            # diff in metadata in v5.0 and 4.0
            # in 4.0 metadata values are seperate keys and starts with metadata_ whereas in 5.0 it is a object and has nested properties
            metaData = ""

            for metaDataKeys in keyName:
                if "metadata_" in metaDataKeys:
                    if result[metaDataKeys] != None:
                        metaData += metaDataKeys[9:] +":"+result[metaDataKeys] + "|"
                elif "metadata" in metaDataKeys:
                    if result[metaDataKeys] != None:
                        metaDataKeys5 =  result[metaDataKeys].keys()
                        for otherMetaDataKeys in metaDataKeys5:
                            if result[metaDataKeys][otherMetaDataKeys] != None:
                                metaData += otherMetaDataKeys +":"+result[metaDataKeys][otherMetaDataKeys] + "|"
            if metaData != "":
                tempDict["Metadata"] = metaData[:-1]
            else:
                tempDict["Metadata"] = metaData
            
            #insert into dataframe
            KBDataFrame = KBDataFrame.append(tempDict, ignore_index=True, sort=False)
        if len(KBDataFrame.index) > 0:
            KBDataFrame = KBDataFrame.assign(Question=KBDataFrame['Questions']).explode('Question').reset_index(drop=True).drop(["Questions"], axis = 1)
            generateExcel(KBDataFrame)
        else:
            print("No rows were generated !")

    except Exception as e:
        exit(e)

def generateExcel(dataFrame):
    print("Generating excel files...")
    #reorder KB headers
    dataFrame = dataFrame.reindex(columns=['KbId','Question','Answer','Source','Metadata','SuggestedQuestions','IsContextOnly','Prompts','QnaId'])
    
    #split pandas DF based on different ID's
    KBName = dataFrame['KbId'].unique().tolist()
    for diffKB in KBName:
        DFCreate = dataFrame.loc[dataFrame['KbId']==diffKB]

        #drop KbId
        DFCreate = DFCreate.drop(['KbId'], axis=1)

        #sort by QnAId's
        DFCreate['QnaId'] = pd.to_numeric(DFCreate['QnaId'])
        DFCreate = DFCreate.sort_values(by=['QnaId'])
        DFCreate['QnaId'] = DFCreate['QnaId'].astype(str)

        #create excel sheet
        DFCreate.to_excel(diffKB+".xlsx",sheet_name='QnAs', index=False)
        print("Sheet Generated with name \t"+str(diffKB)+".xlsx")
    

def validateEndpointKey(endpoint, key, index_name):
    if ".search.windows.net" in endpoint:
        if len(key) == 32:
            if len(index_name) > 0:
                print("Basic Validation Okay")
            else:
                exit("Index Name is empty !")
        else:
            exit("Wrong Search key !")
    else:
        exit("Wrong Search Endpoint !")

def main():

    #fetch KB from Azure Search
    #provide kb name, search service endpoints and search service key
    index_name = ""
    endpoint = ""
    key = ""
    
    createKBUsingSearch(endpoint, key, index_name)

if __name__ == "__main__":
    main()