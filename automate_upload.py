import os
import time
import datetime
import re
from datetime import datetime
import uploader

VIDEO_DIR = 'File directory.'
SESSION_ID = 'Your session ID'
UPLOADED_VIDEOS_FILE = 'uploaded_videos.txt'

def extract_date_from_filename(filename):
    match = re.search(r'(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})', filename)
    if match:
        year, month, day, hour, minute, second = match.groups()
        return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    return None

def get_video_files(video_dir):
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith('.mp4')]
    video_files.sort(key=lambda x: extract_date_from_filename(x))
    return video_files

def extract_date_from_filename(filename):
    date_pattern = r'(\d{4})(\d{2})(\d{2})'
    match = re.search(date_pattern, filename)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month}-{day}"
    return None

def get_uploaded_videos():
    if not os.path.exists(UPLOADED_VIDEOS_FILE):
        return set()
    with open(UPLOADED_VIDEOS_FILE, 'r') as f:
        return set(line.strip() for line in f.readlines())

def add_uploaded_video(video_name):
    with open(UPLOADED_VIDEOS_FILE, 'a') as f:
        f.write(f'{video_name}\n')

def main():
    video_files = get_video_files(VIDEO_DIR)
    uploaded_videos = get_uploaded_videos()
    
    for video_file in video_files:
        video_filename = os.path.basename(video_file)
        if video_filename in uploaded_videos:
            print(f'Skipping already uploaded video: {video_filename}')
            continue

        video_date = extract_date_from_filename(video_filename)
        if video_date is None:
            print(f'Failed to extract date from filename: {video_file}')
            continue

        video_title = f'Video from {video_date}'
        success = False
        while not success:
            print(f'Uploading video: {video_title}')
            success = uploader.uploadVideo(SESSION_ID, video_file, video_title, [])
            if success:
                print(f'Uploaded video: {video_title}')
                add_uploaded_video(video_filename)
            else:
                print(f'Failed to upload video: {video_title}')
                print("Retrying in 300 seconds.")
                time.sleep(300)  # Sleep for 3 minutes before retrying
        time.sleep(300)  # Sleep for 3 minutes between uploads


if __name__ == '__main__':
    main()