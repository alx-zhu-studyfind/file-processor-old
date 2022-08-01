# Written by Alexander Zhu
from webscraperFunc import runWebscraper
from fileProcessor_lib import *


### Processes all csv files in the directory named 'dirName'
  # dirName: the folder name where the files to be processed are stored.
  # processingFunc: the function used to process the files.
    # function must take 2 parameters: fileName and filePath
### Optional parameters:
  # createDir: when True, creates new folders if they are not found (default: True)
    # works best when set to True
  # moveNewFiles: set to True if the processing writes a NEW file, that has to be stored
  # splitFiles: set to False by default, calls the split file function and splits the files into smaller segments.
  # splitSize: set to 50 by default, changes the size of splits if you want to split the file.
  # deleteProcessed: set to False by default, if enabled, deletes files that have the 'p-' label
  # deleteNewFiles: set to False by default, if enabled, deletes new files created from processing
  # processedFolderName: the name of the folder created for processed files
  # newFilesFolderName: set the folder name where the NEW files will be stored.

# processFilesInDir(dirName, processingFunc, 
  # createDir=True, moveNewFiles=False, splitFiles=False, splitSize=50,
  # deleteProcessed=False, deleteNewFiles=False,
  # processedFolderName='processed', newFilesFolderName='new_files')

processFilesInDir('TEST_data_sheets', runWebscraper, 
    moveNewFiles=True, newFilesFolderName="to_split",
    splitFiles=True, splitSize=5)

# deleteProcessed=True, deleteNewFiles=True



