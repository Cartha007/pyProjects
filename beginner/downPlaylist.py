from pytube import YouTube, Playlist
from tqdm import tqdm # Need to install tqdm with pip or pip3

# Playlist url
playlist_url = input("Enter playlist URL: ")

# Playlist object
playlist = Playlist(playlist_url)

# Get total number of videos in the playlist
total_videos = len(playlist.video_urls)

for video_url in tqdm(playlist.video_urls, desc="Downloading videos", unit='video'):
    # Youtube object for the video
    video = YouTube(video_url)
    
    # Download the video in highest resolution
    video.streams.get_highest_resolution().download()
    
    # Update the progress
    tqdm.write(f'Downloaded: {video.title}')

# When all videos have been downloaded
print("All videos have been downloaded!")