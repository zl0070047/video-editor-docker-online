import subprocess
import os
from moviepy.editor import VideoFileClip
import tempfile
import numpy as np
import cv2

class VideoProcessor:
    def __init__(self):
        self.video = None
        self.current_frame = None
        self.fps = 0
        self.duration = 0
        self.total_frames = 0
        self.temp_dir = tempfile.mkdtemp()
        self.frames = []
    
    def open_video(self, file_path):
        """打开视频文件"""
        try:
            self.video = VideoFileClip(file_path)
            self.fps = self.video.fps
            self.duration = self.video.duration
            self.total_frames = int(self.duration * self.fps)
            return True
        except Exception as e:
            print(f"Error opening video: {str(e)}")
            return False
    
    def get_frame(self, time):
        """获取指定时间的帧"""
        if not self.video:
            return None
        try:
            frame = self.video.get_frame(time)
            return frame
        except Exception as e:
            print(f"Error getting frame: {str(e)}")
            return None
    
    def get_duration(self):
        """获取视频时长"""
        return self.duration if self.video else 0
    
    def get_fps(self):
        """获取视频帧率"""
        return self.fps if self.video else 0
    
    def get_total_frames(self):
        """获取总帧数"""
        return self.total_frames if self.video else 0
    
    def resize_frame(self, frame, size):
        """Resize a frame to the specified size."""
        try:
            return cv2.resize(frame, size)
        except Exception as e:
            print(f"Error resizing frame: {str(e)}")
            return frame
    
    def export_video(self, output_path, start_time, end_time):
        """导出视频片段"""
        if not self.video:
            return False
        try:
            clip = self.video.subclip(start_time, end_time)
            clip.write_videofile(output_path)
            clip.close()
            return True
        except Exception as e:
            print(f"Error exporting video: {str(e)}")
            return False
    
    def create_gif(self, output_path, start_time=None, end_time=None,
                  resolution=None, fps=15, colors=256):
        """Create a GIF from the video."""
        if not self.video:
            raise ValueError("No video loaded")
        
        # Create a copy of the video clip
        video = self.video
        
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
        if not self.video:
            return None
        
        return {
            'duration': self.duration,
            'size': self.video.size,
            'fps': self.fps
        }
    
    def cleanup(self):
        """Clean up temporary files and close video."""
        if self.video:
            self.video.close()
            self.video = None 