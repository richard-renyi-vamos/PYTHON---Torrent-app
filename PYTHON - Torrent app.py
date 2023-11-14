import libtorrent as lt

def download_torrent(torrent_file_path, save_path):
    ses = lt.session()
    params = {
        'save_path': save_path,
        'storage_mode': lt.storage_mode_t(2)  # Storage mode 2 for sparse allocation
    }
    handle = ses.add_torrent({'ti': lt.torrent_info(torrent_file_path), 'params': params})

    print(f"Downloading {handle.name()} to {save_path}")
    while not handle.is_seed():
        s = handle.status()
        print(f"\rProgress: {s.progress * 100:.2f}%  Speed: {s.download_rate / 1000:.2f} KB/s", end="")

if __name__ == "__main__":
    torrent_file_path = 'path/to/your/torrent_file.torrent'
    save_path = 'path/to/your/save_directory'
    download_torrent(torrent_file_path, save_path)
