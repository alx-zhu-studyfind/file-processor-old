# Written by Alexander Zhu
import os

# Gets the path to the directory containing all csv files
def getDirectoryPath(dirName):
  currPath = os.getcwd()
  dirPath = os.path.join(currPath, dirName)
  if (dirName not in os.listdir(currPath)):
    # if no folder with target name is found, create it.
    os.mkdir(dirPath)
    print(f"--> Created a '{dirName}' folder. Please add csv files into this folder for processing.")
  return dirPath



# Processes all csv files in the directory at 'path'
def processCSVFilesInDir(dirName):
  # Get the path for the directory with dirName
  dirPath = getDirectoryPath(dirName)
  if (dirPath == None):
    print("--> No directory found.")
    return

  # If the folder is empty, prints a warning
  folderContents = os.listdir(dirPath)
  if (len(folderContents) == 0):
    print(f"--> The '{dirName}' folder is empty. Please add csv files into this folder for processing.")
    return
  
  # Loop through all files
  for fileName in os.listdir(dirPath):
    filePath = os.path.join(dirPath, fileName)
    # only process files
    if (os.path.isfile(filePath)):
      if (fileName.endswith('.csv')):
        print(f'Processing {fileName}...', end='')
        processCSVFile(fileName, filePath)
        storeCSVFile(fileName, filePath, dirPath)
        print(f"Complete! \nMoved {fileName} to the 'processed' folder.\n")
      # if file is not a .csv file, does not process it.
      else:
        print(f"--> '{fileName}' is not a csv file. Skipped this file in processing.\n")
  
  print("ALL FILES PROCESSED!")




# Processes a csv file using its fileName and pathName
def processCSVFile(fileName, filePath):
  pass




# After a csv file is processed, store it in a folder called 'processed'
def storeCSVFile(fileName, filePath, dirPath):
  folderName = 'processed'
  processedPath = os.path.join(dirPath, folderName)
  
  # create the 'processed' folder if it does not exist
  if (folderName not in os.listdir(dirPath)):
    os.mkdir(processedPath)
    print(f"Created the {folderName} directory because the folder was not found...", end='')

  # move the current file to the 'processed' directory.
  os.rename(filePath, os.path.join(processedPath, fileName))

processCSVFilesInDir('data_sheets')