import os
import whisper
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def load_model(model_path="small"):
    return whisper.load_model(model_path)

def transcribe_file(model, input_file_path, output_folder_path):
    result = model.transcribe(input_file_path)

    filename = os.path.basename(input_file_path)
    txt_filename = os.path.splitext(filename)[0] + ".txt"
    output_file_path = os.path.join(output_folder_path, txt_filename)

    with open(output_file_path, 'w') as file:
        file.write(result["text"])

    return f"Transcription for {filename} saved to {output_file_path}"

def transcribe_folder(input_folder_path, output_folder_name, model_path="small", num_threads=None):
    # Create the output folder
    output_folder_path = os.path.join(output_folder_name)
    os.makedirs(output_folder_path, exist_ok=True)

    # Load the model
    model = load_model(model_path)

    # Get the list of files to process
    files_to_process = [os.path.join(input_folder_path, filename) for filename in os.listdir(input_folder_path) if filename.endswith(".mp3")]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(tqdm(executor.map(lambda file: transcribe_file(model, file, output_folder_path), files_to_process), total=len(files_to_process), desc="Transcribe", unit=" audio", position=0, leave=True))

    print(f"Transcription completed. Text files saved to {output_folder_path}")

