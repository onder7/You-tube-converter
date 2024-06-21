
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pytube import YouTube
import configparser

# Config dosyasını yükle
config = configparser.ConfigParser()
config.read('config.ini')

def save_config(path):
    config['Settings']['output_path'] = path
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def load_config():
    return config['Settings']['output_path']

def download_youtube_video(url, output_path, progress_bar):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=output_path)

        # İndirme sırasında ilerleme çubuğunu güncelle
    total_size = video.filesize
    bytes_received = 0
    while bytes_received < total_size:
        bytes_received = os.path.getsize(out_file)
        progress = min(int(bytes_received / total_size * 100), 100)
        progress_bar['value'] = progress
        progress_bar.update()
    return out_file

def convert_to_mp3(input_file, output_file):
    os.system(f'ffmpeg -i "{input_file}" -vn -ab 128k -ar 44100 -y "{output_file}"')
    os.remove(input_file)

def start_download():

    

    url = url_entry.get()
    output_path = load_config()
    
    if not url or not output_path:
        messagebox.showerror("Hata", "Lütfen geçerli bir URL ve çıkış dizini girin.")
        return
    
    try:
        # İlerleme çubuğu oluştur
        progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
        progress_bar.grid(row=2, column=0, columnspan=2, pady=10)
        
        temp_video_path = download_youtube_video(url, output_path, progress_bar)
        mp3_output_path = os.path.join(output_path, os.path.splitext(os.path.basename(temp_video_path))[0] + '.mp3')
        convert_to_mp3(temp_video_path, mp3_output_path)
        messagebox.showinfo("Başarılı", f"MP3 dosyası şu dizine kaydedildi: {mp3_output_path}")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
    finally:
        # İlerleme çubuğunu kaldır
        progress_bar.destroy()








def open_settings():
    def save_settings():
        new_path = filedialog.askdirectory()
        if new_path:
            save_config(new_path)
            settings_window.destroy()
    
    settings_window = tk.Toplevel(root)
    settings_window.title("Ayarlar")
    
    tk.Label(settings_window, text="Çıkış Dizini:").pack(pady=10)
    current_path = load_config()
    tk.Label(settings_window, text=current_path).pack(pady=10)
    tk.Button(settings_window, text="Dizini Değiştir", command=save_settings).pack(pady=20)

# GUI oluşturma
root = tk.Tk()
root.title("YouTube'dan MP3'e Dönüştürücü")

tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

download_button = tk.Button(root, text="İndir ve Dönüştür", command=start_download)
download_button.grid(row=1, column=0, columnspan=2, pady=20)

settings_button = tk.Button(root, text="Ayarlar", command=open_settings)
settings_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()