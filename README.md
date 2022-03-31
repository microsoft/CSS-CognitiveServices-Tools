This tool would let you create a Knowledge base using your Cognitive Search service, in case you have accidentally deleted your QnAMaker or Language service resource.
After running this tool, your KB’s data will be stored in excel files which can be used to restore your KBs using the Import KB option.

Steps:
1.	Clone/Download this repo. 
2.	Make sure you have python installed on your system or install it from this URL https://www.python.org/downloads/.
3.	Open the CMD console inside the same folder which has the requirement.txt file in it.
4.	Run this command on the console:
pip install -r requirements.txt
5.	Open index.py file in edit mode using any code Editor.
6.	Go to def main() function and update these values:
index_name = "" -> Copy the index_name from Azure Cognitive Search Overview page. There will be an indexes tab option in the middle windowpane.
endpoint = “” -> Get this endpoint value from Azure Cognitive Search Overview page. There will be a Url value similar to this: https://<custom_name>.search.windows.net
key = “” -> Get this Key value from Azure Cognitive Search Keys option. Copy any one of the keys and paste it into the code.
7.	From the CMD console run python index.py
8.	After the program finishes, you will see a few Excel Files which will have your KB data.
9.	You can use these Excel files to recreate your KB in new/existing resources using the Import KB option as outlined in the document: 
https://docs.microsoft.com/en-us/azure/cognitive-services/qnamaker/tutorials/export-knowledge-base#import-a-knowledge-base


*Note: TSV and XLS files, from exported knowledge bases, can only be used by importing the files from the Settings page in the QnA Maker portal. They can't be used as data sources during knowledge base creation or from the + Add file or + Add URL feature on the Settings page.

When you import the Knowledge base through these TSV and XLS files, the QnA pairs get added to the editorial source and not the sources from which the QnAs were extracted in the exported Knowledge Base.
