import os
import shutil
import subprocess
import zipfile

def download_kaggle_dataset(api_file_path, dataset_link, folder_path=None):
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

# kaggle_json_path = 'kaggle.json'
# dataset_link = 'https://www.kaggle.com/datasets/samnikolas/eeg-dataset'

# download_kaggle_dataset(kaggle_json_path, dataset_link)
