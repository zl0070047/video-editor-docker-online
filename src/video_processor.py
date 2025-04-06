import subprocess
import os
from moviepy.editor import VideoFileClip
import tempfile
import numpy as np
import cv2

class VideoProcessor:
    def __init__(self):
        self.current_video = None
        self.temp_dir = tempfile.mkdtemp()
        self.frames = []
    
    def import_video(self, file_path):
        """Import a video file and validate its size."""
        if not os.path.exists(file_path):
            raise FileNotFoundError("Video file not found")
        
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
        if file_size > 100:
            raise ValueError("Video file size exceeds 100MB limit")
        
        self.current_video = VideoFileClip(file_path)
        return self.current_video
    
    def get_frame(self, frame_number):
        """Get a specific frame from the video."""
        if not self.current_video:
            return None
            
        try:
            time = frame_number / self.current_video.fps
            if time > self.current_video.duration:
                return None
                
            frame = self.current_video.get_frame(time)
            return frame  # MoviePy already returns RGB format
        except Exception as e:
            print(f"Error getting frame: {str(e)}")
            return None
    
    def resize_frame(self, frame, size):
        """Resize a frame to the specified size."""
        try:
            return cv2.resize(frame, size)
        except Exception as e:
            print(f"Error resizing frame: {str(e)}")
            return frame
    
    def export_video(self, output_path, start_time=None, end_time=None, 
                    format="mp4", resolution=None, fps=None):
        """Export video with specified parameters."""
        if not self.current_video:
            raise ValueError("No video loaded")
        
        # Create a copy of the video clip
        video = self.current_video
        
        # Apply time range if specified
        if start_time is not None or end_time is not None:
            start = start_time if start_time is not None else 0
            end = end_time if end_time is not None else video.duration
            video = video.subclip(start, end)
        
        # Apply resolution if specified
        if resolution:
            if resolution == "720p":
                video = video.resize(height=720)
            elif resolution == "480p":
                video = video.resize(height=480)
        
        # Apply FPS if specified
        if fps:
            video = video.set_fps(int(fps))
        
        # Export the video
        video.write_videofile(output_path, codec='libx264')
        video.close()
    
    def create_gif(self, output_path, start_time=None, end_time=None,
                  resolution=None, fps=15, colors=256):
        """Create a GIF from the video."""
        if not self.current_video:
            raise ValueError("No video loaded")
        
        # Create a copy of the video clip
        video = self.current_video
        
        # Apply time range if specified
        if start_time is not None or end_time is not None:
            start = start_time if start_time is not None else 0
            end = end_time if end_time is not None else video.duration
            video = video.subclip(start, end)
        
        # Apply resolution if specified
        if resolution:
            if resolution == "720p":
                video = video.resize(height=720)
            elif resolution == "480p":
                video = video.resize(height=480)
        
        # Set FPS
        video = video.set_fps(fps)
        
        # Export as GIF
        video.write_gif(output_path, program='ffmpeg', opt='optimizeplus', 
                       fuzz=10, colors=colors)
        video.close()
    
    def get_video_info(self):
        """Get information about the current video."""
        if not self.current_video:
            return None
        
        return {
            'duration': self.current_video.duration,
            'size': self.current_video.size,
            'fps': self.current_video.fps
        }
    
    def cleanup(self):
        """Clean up temporary files and close video."""
        if self.current_video:
            self.current_video.close()
            self.current_video = None 