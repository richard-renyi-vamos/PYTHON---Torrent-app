import libtorrent as lt
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread

class TorrentDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Torrent Downloader")

        # Torrent file selection
        self.torrent_file_label = tk.Label(root, text="Torrent File:")
        self.torrent_file_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.torrent_file_entry = tk.Entry(root, width=50)
        self.torrent_file_entry.grid(row=0, column=1, padx=10, pady=5)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_torrent_file)
        self.browse_button.grid(row=0, column=2, padx=10, pady=5)

        # Save path selection
        self.save_path_label = tk.Label(root, text="Save Path:")
        self.save_path_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.save_path_entry = tk.Entry(root, width=50)
        self.save_path_entry.grid(row=1, column=1, padx=10, pady=5)

        self.save_browse_button = tk.Button(root, text="Browse", command=self.browse_save_path)
        self.save_browse_button.grid(row=1, column=2, padx=10, pady=5)

        # Download button
        self.download_button = tk.Button(root, text="Download", command=self.start_download)
        self.download_button.grid(row=2, column=1, padx=10, pady=20)

        # Progress display
        self.progress_label = tk.Label(root, text="Progress: 0.00%", anchor="w")
        self.progress_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        self.speed_label = tk.Label(root, text="Speed: 0.00 KB/s", anchor="w")
        self.speed_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="w")

    def browse_torrent_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Torrent Files", "*.torrent")])
        if file_path:
            self.torrent_file_entry.delete(0, tk.END)
            self.torrent_file_entry.insert(0, file_path)

    def browse_save_path(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.save_path_entry.delete(0, tk.END)
            self.save_path_entry.insert(0, directory_path)

    def start_download(self):
        torrent_file_path = self.torrent_file_entry.get()
        save_path = self.save_path_entry.get()

        if not torrent_file_path or not save_path:
            messagebox.showwarning("Input Error", "Please select a torrent file and a save path.")
            return

        self.download_button.config(state=tk.DISABLED)
        download_thread = Thread(target=self.download_torrent, args=(torrent_file_path, save_path))
        download_thread.start()

    def download_torrent(self, torrent_file_path, save_path):
        ses = lt.session()
        params = {
            'save_path': save_path,
            'storage_mode': lt.storage_mode_t(2)  # Sparse allocation
        }
        handle = ses.add_torrent({'ti': lt.torrent_info(torrent_file_path), 'params': params})

        while not handle.is_seed():
            s = handle.status()
            progress = s.progress * 100
            speed = s.download_rate / 1000

            self.progress_label.config(text=f"Progress: {progress:.2f}%")
            self.speed_label.config(text=f"Speed: {speed:.2f} KB/s")
            self.root.update_idletasks()

        messagebox.showinfo("Download Complete", f"{handle.name()} has been downloaded successfully.")
        self.download_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = TorrentDownloader(root)
    root.mainloop()
