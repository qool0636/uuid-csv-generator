import PyInstaller.__main__
import os

# 確保在正確的目錄
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PyInstaller.__main__.run([
    'uuid_csv_downloader.py',
    '--onefile',
    '--name=UUID_CSV_Downloader',
    '--add-data=README.md:.',
    '--clean',
    '--noconfirm'
]) 