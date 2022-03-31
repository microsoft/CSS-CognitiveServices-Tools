# QnAMaker-createKB
This tool would let you create Knowledge base using your Cognitive Search service, in case if you have accidently deleted your QnAMaker resource.
After running this tool, your KB’s data will be stored in excel files which can be used to restore your KB using Import KB option.


Steps to run this tool:
1.	Clone/Download the repo. 
2.	Make sure you have python installed on your system.
3.	Open CMD console inside the same folder which has requirement.txt file in it.
4.	Run this command on console:
    pip install -r requirements.txt
5.	Open index.py file in edit mode using any code Editor.
6.	Go to def main() function and update these values:
    index_name = "" -> Copy the index_name from Azure Cognitive Search Overview page. There will be indexes tab option in the middle windowpane.
    endpoint = “” -> Get this endpoint value from Azure Cognitive Search Overview page. There will be a Url value similar to this:  https://<custom_name>.search.windows.net
    key = “” -> Get this Key value from Azure Cognitive Search Keys option. Copy any one of the keys and paste it in code.
7.	From CMD console run python index.py
8.	After the program finishes, you will see few Excel Files which will have your KB data.
9.	You can use these Excel file to recreate your KB in new/existing resource using Import KB option.
