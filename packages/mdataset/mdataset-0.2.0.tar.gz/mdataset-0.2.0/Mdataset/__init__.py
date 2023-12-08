from Mdataset.Audio.meta_audio import load_seamless_m4t_model
from Mdataset.Audio.meta_audio import text_to_audio
from Mdataset.Audio.meta_audio import save_audio
from Mdataset.Audio.meta_audio import generate_translated_text
from Mdataset.Audio.meta_audio import text_to_translated_text
from Mdataset.Audio.meta_audio import save_text
from Mdataset.Audio.transcription import load_model
from Mdataset.Audio.transcription import transcribe_file
from Mdataset.Audio.transcription import transcribe_folder

# Censored
from Mdataset.Censored.launch import launch_app
from Mdataset.Circuit.deep_circuit import get_with_tor
from Mdataset.Circuit.multihead_circuit import get_tor_multiprocessing

# Dark web
from Mdataset.DWeb.dsearch import run_command
from Mdataset.DWeb.dsearch import text_search   
from Mdataset.DWeb.dsearch import text_search_with_download
from Mdataset.DWeb.dsearch import image_search
from Mdataset.DWeb.dsearch import news_search
from Mdataset.DWeb.dsearch import save_news_to_csv
from Mdataset.DWeb.dsearch import answers_search

# File transfer
from Mdataset.FTransfer.Flaunch import flaunch_app

# huggingface
from Mdataset.Huggingface.face_dataset import huggingface_dataset

# Kaggle
from Mdataset.Kaggle.kaggle_load import kaggle_dataset

# Multhreading
from Mdataset.Multithread.cpu_info import get_cpu_info

# OCR
from Mdataset.Optical.displaytext import display_text
from Mdataset.Optical.pdf2text import pdf_totext

# scrapping
from Mdataset.Scrapping.chan import get_4chan
from Mdataset.Scrapping.allscrap import scrape_data
from Mdataset.Scrapping.gscholar import search_author_and_print
from Mdataset.Scrapping.gscholar import retrieve_author_details_and_print
from Mdataset.Scrapping.gscholar import retrieve_first_publication_and_print
from Mdataset.Scrapping.gscholar import print_publication_titles
from Mdataset.Scrapping.gscholar import print_citations_for_first_publication

# Synthetic
from Mdataset.Synthetic.petals_generate import generate_text

# Tabular
from Mdataset.Tabular.synload import syn_load
from Mdataset.Tabular.tab_train import train_save
from Mdataset.Tabular.tabledata import table_generate

# YouTube
from Mdataset.Youdownload.audio_downloader import ytube_tomp
from Mdataset.Youdownload.media_download import ytube_media