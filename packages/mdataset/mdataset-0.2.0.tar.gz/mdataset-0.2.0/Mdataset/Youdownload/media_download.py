from pytube import YouTube
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor

def load_urls(input_file):
    if input_file.endswith('.txt'):
        with open(input_file, 'r') as file:
            return file.read().splitlines()
    else:
        return [input_file]

def download_video(video_url, output_folder, overall_tqdm_bar):
    yt = YouTube(video_url)
    video_stream = yt.streams.filter(file_extension='mp4', progressive=True).first()

    # Manually updating overall tqdm progress
    overall_tqdm_bar.update(1)

    video_stream.download(output_folder, filename=video_stream.title + '.mp4')

def ytube_media(input_source, output_folder='output/'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_urls = load_urls(input_source)

    with tqdm(total=len(video_urls), desc="Downloading videos", unit=" video") as overall_tqdm_bar:
        def process_url(video_url):
            download_video(video_url, output_folder, overall_tqdm_bar)

        with ThreadPoolExecutor() as executor:
            list(executor.map(process_url, video_urls))

# ytube_media('/content/cam-text.txt', output_folder="/content/High")