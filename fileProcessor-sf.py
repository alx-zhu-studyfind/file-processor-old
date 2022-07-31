# Written by Alexander Zhu
import os
from webscraperFunc import runWebscraper

# Gets the path to the directory containing all csv files
def getDirectoryPath(dirName):
  dirPath = os.path.join(os.getcwd(), dirName)
  if (dirName not in os.listdir()):
    # if no folder with target name is found, create it.
    os.mkdir(dirPath)
    print(f"--> Created a '{dirName}' folder. Please add files into this folder for processing.")
  return dirPath



# Processes all csv files in the directory at 'path'
def processFilesInDir(dirName):
  ### Change suffix based on the type of file
  suffix = '.csv'

  # Get the path for the directory with dirName
  dirPath = getDirectoryPath(dirName)
  if (dirPath == None):
    print("--> No directory found.")
    return
  else:
    print("Directory found! \n")

  # If the folder is empty, prints a warning
  folderContents = os.listdir(dirPath)
  if (len(folderContents) == 0):
    print(f"--> The '{dirName}' folder is empty. Please add {suffix} files into this folder for processing.")
    return
  
  # Loop through all files
  for fileName in os.listdir(dirPath):
    filePath = os.path.join(dirPath, fileName)
    # only process files
    if (os.path.isfile(filePath)):
      if (fileName.endswith(suffix)):
        print(f'Processing {fileName}...')
        processFile(fileName, filePath)
        storeFile(fileName, filePath, dirPath)
        print(f"Complete! Moved {fileName} to the 'processed' folder. 'p-' tag added to file name.\n")
      # if file is not a .suffix file, does not process it.
      else:
        print(f"--> '{fileName}' is not a {suffix} file. Skipped this file in processing.\n")
  
  print("ALL FILES PROCESSED!")



# Processes a file using its fileName and pathName (insert function inside)
def processFile(fileName, filePath):
  runWebscraper(fileName, filePath)



# After a file is processed, store it in a folder called 'processed'
def storeFile(fileName, filePath, dirPath):
  ### Change the folder name of processed files
  folderName = 'processed'
  folderPath = os.path.join(dirPath, folderName)
  
  # create the 'processed' folder if it does not exist
  if (folderName not in os.listdir(dirPath)):
    os.mkdir(folderPath)
    print(f"--> Created the {folderName} directory because the folder was not found...")

  # move the current file to the 'processed' directory.
  os.rename(filePath, os.path.join(folderPath, 'p-' + fileName))

  # move new files into a "to_split" folder
  moveNewFile(fileName, dirPath)



# For Studyfind Automation: moves new webscraped files into a "to_split" folder.
# This function relies on the fact that the webscraper code writes the data
# into a NEW csv file with the same file name, but creates it in the current directory.
def moveNewFile(fileName, dirPath):
  ### Change folder name as needed
  folderName = 'to_split'
  folderPath = os.path.join(dirPath, folderName)

  # create the 'to_split' directory if it does not exist
  if (folderName not in os.listdir(dirPath)):
    os.mkdir(folderPath)
    print(f"--> Created the {folderName} directory because the folder was not found...")
  
  # move the new file into the 'to_split' folder. make sure the file exists.
  newFilePath = os.path.join(os.getcwd(), fileName)
  if (os.path.isfile(newFilePath)):
    os.rename(newFilePath, os.path.join(folderPath, fileName))
  else:
    print(f"--> {fileName} is not a file in the current directory.")




processFilesInDir('data_sheets')