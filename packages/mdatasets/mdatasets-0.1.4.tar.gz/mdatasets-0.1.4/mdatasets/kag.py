import os
import shutil
import subprocess
import zipfile

def kaggle_dataset(api_file_path, dataset_link, folder_path=None):
    """
    Download and extract a Kaggle dataset using the Kaggle API.

    Parameters:
    - api_file_path (str): The path to the Kaggle API key file (kaggle.json).
    - dataset_link (str): The Kaggle dataset link (e.g., 'https://www.kaggle.com/datasets/username/datasetname').
    - folder_path (str, optional): The local path to store the downloaded dataset. If None, the current working directory is used.

    Prints:
    - Success messages for each step (download, unzip, remove downloaded zip file) if successful.
    - Error message if any step fails.

    Example:
    >>> kaggle_json_path = 'kaggle.json'
    >>> dataset_link = 'https://www.kaggle.com/datasets/samnikolas/eeg-dataset'
    >>> download_kaggle_dataset(kaggle_json_path, dataset_link)
    Dataset downloaded successfully!
    Dataset unzipped successfully!
    Downloaded zip file removed.
    """

    home_dir = os.path.expanduser("~")
    destination_dir = os.path.join(home_dir, '.kaggle')
    os.makedirs(destination_dir, exist_ok=True)
    shutil.copy(api_file_path, destination_dir)
    
    dataset_identifier = dataset_link.replace("https://www.kaggle.com/datasets/", "")
    
    if folder_path is None:
        dataset_storage_path = os.getcwd()
    else:
        dataset_storage_path = folder_path
    
    try:
        subprocess.run(['kaggle', 'datasets', 'download', '-d', dataset_identifier, '-p', dataset_storage_path], check=True)
        print("Dataset downloaded successfully!")

        zip_filename = f"{dataset_identifier.split('/')[-1]}.zip"
        downloaded_zip_file = os.path.join(dataset_storage_path, zip_filename)
        
        with zipfile.ZipFile(downloaded_zip_file, 'r') as zip_ref:
            zip_ref.extractall(dataset_storage_path)
        print("Dataset unzipped successfully!")

        os.remove(downloaded_zip_file)
        print("Downloaded zip file removed.")
    except subprocess.CalledProcessError:
        print("Error occurred while downloading the dataset.")
