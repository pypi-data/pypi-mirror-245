from pytube import YouTube
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment

def load_urls(input_file):
    if input_file.endswith('.txt'):
        with open(input_file, 'r') as file:
            return file.read().splitlines()
    else:
        return [input_file]

def download_and_convert_to_mp3(video_url, output_folder, overall_tqdm_bar, check_deleted):
    yt = YouTube(video_url)
    video_stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
    overall_tqdm_bar.update(1)
    video_path = os.path.join(output_folder, video_stream.title + '.mp4')
    video_stream.download(output_folder, filename=video_stream.title + '.mp4')
    audio = AudioSegment.from_file(video_path, format='mp4')
    audio_path = os.path.join(output_folder, video_stream.title + '.mp3')
    audio.export(audio_path, format='mp3')
    os.remove(video_path)

    # Check if the video file is deleted, if not, remove it
    check_deleted(video_path)

def check_and_remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def check_and_remove_remaining_videos(output_folder):
    video_files = [f for f in os.listdir(output_folder) if f.endswith('.mp4')]
    for video_file in video_files:
        video_path = os.path.join(output_folder, video_file)
        check_and_remove_file(video_path)

def ytube_tomp(input_source, output_folder='output/'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_urls = load_urls(input_source)

    def check_deleted(video_path):
        check_and_remove_file(video_path)

    with tqdm(total=len(video_urls), desc="Downloading audio", unit=" audio", position=0, leave=True) as overall_tqdm_bar:
        def process_url(video_url):
            download_and_convert_to_mp3(video_url, output_folder, overall_tqdm_bar, check_deleted)

        with ThreadPoolExecutor() as executor:
            list(executor.map(process_url, video_urls))

    # Check and remove any remaining video files
    check_and_remove_remaining_videos(output_folder)

# ytube_tomp('/content/cam-text.txt', output_folder="/content/final_mp")
