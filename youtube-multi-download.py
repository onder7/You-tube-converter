//bir metin dosyasındaki YouTube URL'lerini okuyup videoları indirir ve MP3 formatına dönüştürür.
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from yt_dlp import YoutubeDL

def download_video(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def process_videos(file_path, output_path):
    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    progress_bar['maximum'] = len(urls)
    for idx, url in enumerate(urls, start=1):
        try:
            download_video(url, output_path)
            progress_bar['value'] = idx
            progress_bar.update()
        except Exception as e:
            messagebox.showerror("Hata", f"URL işlenirken bir hata oluştu: {url}\n{e}")

    messagebox.showinfo("Başarılı", "Tüm videolar başarıyla indirildi ve MP3'e dönüştürüldü.")

def start_processing():
    file_path = filedialog.askopenfilename(title="URL listesi seç", filetypes=[("Text files", "*.txt")])
    if not file_path:
        return
    output_path = filedialog.askdirectory(title="Çıkış dizinini seç")
    if not output_path:
        return
    process_videos(file_path, output_path)

# GUI oluşturma
root = tk.Tk()
root.title("YouTube to MP3 Converter")

start_button = tk.Button(root, text="Başlat", command=start_processing)
start_button.grid(row=0, column=0, padx=20, pady=20)

progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(row=1, column=0, padx=20, pady=20)

root.mainloop()
