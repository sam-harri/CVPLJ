import os
import pytube.exceptions
from pytube import YouTube
from moviepy.editor import VideoFileClip
from tqdm import tqdm

class YoutubeClip:
    """
    A class to download, process, and save clips from YouTube videos.

    Parameters
    ----------
    url : str
        The URL of the YouTube video.
    start_time : float or None, optional
        The start time in seconds from where the clip should begin.
    end_time : float or None, optional
        The end time in seconds at which the clip should end.
    framerate : int or None, optional
        The framerate (frames per second) to which the video should be adjusted.
    path : str, optional
        The directory path where the video will be saved. Defaults to 'videos/'.

    Attributes
    ----------
    video_name : str
        The name of the downloaded video file, set after downloading the video.

    Methods
    -------
    download_video():
        Downloads the video from YouTube.
    trim_and_adjust_framerate():
        Trims the video between start_time and end_time and adjusts its framerate.
    _process_video():
        Processes the video by downloading and trimming as specified.
    """
    def __init__(self, url, start_time=None, end_time=None, framerate=None, path='videos/'):
        self.url = url
        self.start_time = start_time
        self.end_time = end_time
        self.framerate = framerate
        self.path = path
        self.video_name = None
        self.pbar = None  # Initialize pbar here
        self._process_video()

    def show_progress_bar(self, stream, chunk, bytes_remaining):
        """Update progress bar during download."""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        self.pbar.update(percentage_of_completion - self.pbar.n)

    def download_video(self):
        """Downloads the video from YouTube with a progress bar."""
        try:
            yt = YouTube(self.url, on_progress_callback=self.show_progress_bar)
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            self.video_name = video.default_filename.replace(' ', '-')
            self.pbar = tqdm(total=100, desc="Downloading", unit="%")
            video.download(output_path=self.path, filename=self.video_name)
            self.pbar.close()
        except Exception as e:
            if self.pbar:
                self.pbar.close()
            raise RuntimeError(f"Failed to download video: {e}")

    def trim_and_adjust_framerate(self):
        """Trims the video between start_time and end_time and adjusts its framerate."""
        input_path = os.path.join(self.path, self.video_name)
        output_filename = f"{self.video_name}-{self.start_time or 'start'}-{self.end_time or 'end'}.mp4"
        output_path = os.path.join(self.path, output_filename)

        video_clip = VideoFileClip(input_path)
        if self.start_time is not None or self.end_time is not None:
            video_clip = video_clip.subclip(self.start_time, self.end_time)
        if self.framerate:
            video_clip = video_clip.set_fps(self.framerate)
        video_clip.write_videofile(output_path, codec='libx264')
        video_clip.close()
        os.remove(input_path)

    def _process_video(self):
        self.download_video()
        self.trim_and_adjust_framerate()