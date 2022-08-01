# Written by Alexander Zhu
import os
import pandas as pd
######################### PROCESSING FUNCTIONS #################################

def processFilesInDir(dirName, processingFunc, 
  createDir=True, moveNewFiles=False, splitFiles=False, splitSize=50,
  deleteProcessed=False, deleteNewFiles=False,
  processedFolderName='processed', newFilesFolderName='new_files'):
  ### Change suffix based on the type of file being processed
  suffix = '.csv'

  # Get the path for the directory with dirName
  dirPath = getDirectoryPath(dirName, createDir)
  if (dirPath == None):
    print("--> No directory found. Ending program.")
    return
  else:
    print("Directory found! \n")

  # If the folder is empty, prints a warning
  folderContents = os.listdir(dirPath)
  if (len(folderContents) == 0):
    print(f"--> The '{dirName}' folder is empty. Please add '{suffix}' files into this folder for processing.")
    return
  
  if (deleteProcessed or deleteNewFiles):
    print(f"*** ATTENTION! Running program with deleteProcessed={deleteProcessed} and deleteNewFiles={deleteNewFiles}. Files will be deleted! ***\n")
    cont = input("Continue (y/n)? ").lower()
    if (cont == 'n'):
      return

  # Loop through all files
  for fileName in os.listdir(dirPath):
    filePath = os.path.join(dirPath, fileName)
    # only process files
    if (os.path.isfile(filePath)):
      if (fileName.endswith(suffix)):
        print(f'Processing {fileName}...')
        processFile(fileName, filePath, processingFunc)
        storeFile(fileName, filePath, dirPath, processedFolderName, createDir=createDir, deleteProcessed=deleteProcessed)
        # If there are NEW files that are written and moveNewFiles=True, move them.
        if (moveNewFiles):
          filePath = moveNewFile(fileName, dirPath, newFilesFolderName, createDir=createDir)
        # If files need to be split, split them
        if (splitFiles):
          splitFile(fileName, filePath, dirPath, splitSize)
        # If deleteNewFiles is enabled, delete the new file via 'filePath'
        if (deleteNewFiles and os.path.isfile(filePath)):
          os.remove(filePath)
          print(f"'{fileName}' deleted.")

        print(f"Complete!\n")

      # if file is not a .suffix file, does not process it.
      else:
        print(f"--> '{fileName}' is not a '{suffix}' file. Skipped this file in processing.\n")
  
  print("ALL FILES PROCESSED!")



# Gets the path to the directory containing all csv files, makes a new 
# directory with 'dirName' if none is found. Disable folder creation by setting
# createDir to False.
def getDirectoryPath(dirName, createDir=True):
  dirPath = os.path.join(os.getcwd(), dirName)
  if (dirName not in os.listdir()):
    if (createDir):
      # if no folder with target name is found, create it.
      os.mkdir(dirPath)
      print(f"--> Created a '{dirName}' folder. Please add files into this folder for processing.")
    else:
      print(f"--> No folder created (createDir=False). Please change the name of the target folder, or create a folder manually.")
      dirPath = None
  return dirPath



# Processes a file using its fileName and pathName (insert function inside)
def processFile(fileName, filePath, processingFunc):
  processingFunc(fileName, filePath)




# After a file is processed, store it in a folder called 'processed'
def storeFile(fileName, filePath, dirPath, folderName, createDir=True, deleteProcessed=False):
  # if the file is to be deleted, delete it and return from the function
  if (deleteProcessed and os.path.isfile(filePath)):
    os.remove(filePath)
    print(f"'p-{fileName}' deleted.")
    return

  folderPath = os.path.join(dirPath, folderName)
  folderExists = False
  
  # create the 'processed' folder if it does not exist
  if (folderName not in os.listdir(dirPath)):
    if (createDir):
      os.mkdir(folderPath)
      print(f"--> Created the '{folderName}' folder because the folder was not found.")
      folderExists = True
    else:
      print(f"--> '{folderName}' folder was not found. No new folders created (createDir is set to False).")
  else:
    folderExists = True

  # move the current file to the 'processed' folder if it exists.
  if (folderExists):
    os.rename(filePath, os.path.join(folderPath, 'p-' + fileName))
    print(f"Moved '{fileName}' to the '{folderName}' folder. 'p-' tag added to file name.")
  # otherwise, just add the tag to the file.
  else:
    os.rename(filePath, os.path.join(os.getcwd(), 'p-' + fileName))
    print(f"'{folderName}' folder does not exist. 'p-' tag added to file name.")



# For Studyfind Automation: moves new webscraped files into a "to_split" folder.
# This function relies on the fact that the webscraper code writes the data
# into a NEW csv file with the same file name, but creates it in the current directory.
# RETURNS the path to the new file.
def moveNewFile(fileName, dirPath, folderName, createDir=True):
  folderPath = os.path.join(dirPath, folderName)
  folderExists = False

  # create the 'to_split' directory if it does not exist
  if (folderName not in os.listdir(dirPath)):
    if (createDir):
      os.mkdir(folderPath)
      print(f"--> Created the '{folderName}' folder because the folder was not found.")
      folderExists = True
    else:
      print(f"--> '{folderName}' folder was not found. No new folders created (createDir is set to False).")
  else:
    folderExists = True
  
  # move the new file into the 'to_split' folder. make sure the file exists.
  if (folderExists):
    newFilePath = os.path.join(os.getcwd(), fileName)
    if (os.path.isfile(newFilePath)):
      newPath = os.path.join(folderPath, fileName)
      os.rename(newFilePath, newPath)
      print(f"Moved the new version of '{fileName}' to the '{folderName}' folder.")
      return newPath
    else:
      print(f"--> '{fileName}' is not a file in the current folder.")



# Splits a .csv file into files of a maximum size
# This function has NO createDir parameter, as folders MUST be created.
def splitFile(fileName, filePath, dirPath, splitSize, folderName="split_files"):
  parentFolderPath = os.path.join(dirPath, folderName)

  # create the 'to_split' directory if it does not exist
  if (folderName not in os.listdir(dirPath)):
    os.mkdir(parentFolderPath)
    print(f"--> Created the '{folderName}' folder because the folder was not found.")
  
  # creates a folder with the same name as the file to hold the split files.
  childFolderName = str(fileName.split('.')[0])
  childFolderPath = os.path.join(parentFolderPath, childFolderName)
  os.mkdir(childFolderPath)
  print(f"--> Created the '{childFolderName}' folder to store the split files.")
  
  # splits the files
  data = pd.read_csv(filePath)
  data.rename(columns={'Contact Name':'Name'})
  total = len(data)
  splits = (total//splitSize + 1) if (total % splitSize != 0) else (total//splitSize)
  for i in range(splits):
    # gets a data frame of size 'size' and converts it into a csv file.
    dFrame = data[splitSize*i:splitSize*(i+1)]
    dFrame.to_csv(os.path.join(childFolderPath, f"{i}_{fileName}"), index=False)
  print(f"{splits} split files added to the '{childFolderName}' folder.")
