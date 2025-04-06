import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                           QSlider, QComboBox, QFrame, QSpinBox)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QIcon, QPalette, QColor, QFont, QPixmap, QImage
from video_processor import VideoProcessor

class VideoEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Editor")
        self.setMinimumSize(1200, 800)
        
        # Initialize video processor
        self.video_processor = VideoProcessor()
        
        # Initialize video playback variables
        self.current_frame = 0
        self.is_playing = False
        self.playback_timer = QTimer()
        self.playback_timer.timeout.connect(self.update_frame)
        
        # Set up the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Create the sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Create the main content area
        content_area = self.create_content_area()
        main_layout.addWidget(content_area, stretch=1)
        
        # Apply the skeuomorphic style
        self.apply_skeuomorphic_style()
    
    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setMinimumWidth(250)
        sidebar.setMaximumWidth(250)
        
        layout = QVBoxLayout(sidebar)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Import button
        import_btn = QPushButton("Import Video")
        import_btn.setObjectName("importButton")
        import_btn.clicked.connect(self.import_video)
        layout.addWidget(import_btn)
        
        # Trim settings
        trim_label = QLabel("Trim Settings")
        trim_label.setObjectName("sectionLabel")
        layout.addWidget(trim_label)
        
        # Start time
        start_layout = QHBoxLayout()
        start_label = QLabel("Start:")
        self.start_time = QSpinBox()
        self.start_time.setMinimum(0)
        self.start_time.setSuffix(" s")
        self.start_time.valueChanged.connect(self.start_time_changed)
        start_layout.addWidget(start_label)
        start_layout.addWidget(self.start_time)
        set_start_btn = QPushButton("Set")
        set_start_btn.clicked.connect(self.set_start_time)
        set_start_btn.setFixedWidth(50)
        start_layout.addWidget(set_start_btn)
        layout.addLayout(start_layout)
        
        # End time
        end_layout = QHBoxLayout()
        end_label = QLabel("End:")
        self.end_time = QSpinBox()
        self.end_time.setMinimum(0)
        self.end_time.setSuffix(" s")
        self.end_time.valueChanged.connect(self.end_time_changed)
        end_layout.addWidget(end_label)
        end_layout.addWidget(self.end_time)
        set_end_btn = QPushButton("Set")
        set_end_btn.clicked.connect(self.set_end_time)
        set_end_btn.setFixedWidth(50)
        end_layout.addWidget(set_end_btn)
        layout.addLayout(end_layout)
        
        # Export options
        export_label = QLabel("Export Options")
        export_label.setObjectName("sectionLabel")
        layout.addWidget(export_label)
        
        # Format selection
        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP4", "MOV", "AVI", "GIF"])
        layout.addWidget(self.format_combo)
        
        # Resolution selection
        self.res_combo = QComboBox()
        self.res_combo.addItems(["Original", "720p", "480p", "Custom"])
        layout.addWidget(self.res_combo)
        
        # Frame rate selection
        self.fps_combo = QComboBox()
        self.fps_combo.addItems(["Original", "30", "24", "15"])
        layout.addWidget(self.fps_combo)
        
        # Export button
        export_btn = QPushButton("Export")
        export_btn.setObjectName("exportButton")
        export_btn.clicked.connect(self.export_video)
        layout.addWidget(export_btn)
        
        layout.addStretch()
        
        return sidebar
    
    def create_content_area(self):
        content = QFrame()
        content.setObjectName("contentArea")
        
        layout = QVBoxLayout(content)
        
        # Video preview area
        self.preview = QLabel("Video Preview")
        self.preview.setObjectName("previewArea")
        self.preview.setMinimumHeight(400)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.preview)
        
        # Timeline area
        timeline_container = QFrame()
        timeline_container.setObjectName("timeline")
        timeline_container.setMinimumHeight(100)
        timeline_layout = QVBoxLayout(timeline_container)
        
        # Timeline slider
        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.timeline_slider.setObjectName("timelineSlider")
        self.timeline_slider.setTracking(True)  # Enable live tracking
        self.timeline_slider.sliderPressed.connect(self.slider_pressed)
        self.timeline_slider.sliderReleased.connect(self.slider_released)
        self.timeline_slider.valueChanged.connect(self.timeline_value_changed)
        timeline_layout.addWidget(self.timeline_slider)
        
        # Time labels
        time_labels = QHBoxLayout()
        self.current_time_label = QLabel("00:00")
        self.total_time_label = QLabel("00:00")
        time_labels.addWidget(self.current_time_label)
        time_labels.addStretch()
        time_labels.addWidget(self.total_time_label)
        timeline_layout.addLayout(time_labels)
        
        layout.addWidget(timeline_container)
        
        # Control buttons
        controls = QHBoxLayout()
        
        self.play_btn = QPushButton("Play")
        self.play_btn.setObjectName("controlButton")
        self.play_btn.clicked.connect(self.toggle_playback)
        controls.addWidget(self.play_btn)
        
        layout.addLayout(controls)
        
        return content
    
    def slider_pressed(self):
        if self.is_playing:
            self.toggle_playback()
    
    def slider_released(self):
        self.update_frame()
    
    def start_time_changed(self, value):
        if value >= self.end_time.value():
            self.start_time.setValue(self.end_time.value() - 1)
    
    def end_time_changed(self, value):
        if value <= self.start_time.value():
            self.end_time.setValue(self.start_time.value() + 1)
    
    def set_start_time(self):
        if not self.video_processor.current_video:
            return
        current_time = int(self.current_frame / self.video_processor.current_video.fps)
        self.start_time.setValue(current_time)
    
    def set_end_time(self):
        if not self.video_processor.current_video:
            return
        current_time = int(self.current_frame / self.video_processor.current_video.fps)
        self.end_time.setValue(current_time)
    
    def import_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.mov *.avi);;All Files (*)"
        )
        
        if file_path:
            try:
                self.video_processor.import_video(file_path)
                video_info = self.video_processor.get_video_info()
                
                # Update timeline
                duration = round(video_info['duration'])  # Round to nearest integer
                self.timeline_slider.setMinimum(0)
                self.timeline_slider.setMaximum(int(duration * video_info['fps']))
                
                # Update time settings
                self.start_time.setMaximum(duration)
                self.end_time.setMaximum(duration)
                self.end_time.setValue(duration)
                
                # Update time labels
                self.total_time_label.setText(f"{duration//60:02d}:{duration%60:02d}")
                
                # Start preview
                self.current_frame = 0
                self.update_frame()
                
            except Exception as e:
                self.preview.setText(f"Error: {str(e)}")
    
    def timeline_value_changed(self, value):
        if not self.video_processor.current_video:
            return
            
        video_info = self.video_processor.get_video_info()
        current_time = value / video_info['fps']
        self.current_time_label.setText(f"{int(current_time)//60:02d}:{int(current_time)%60:02d}")
        
        if not self.is_playing:
            self.current_frame = value
            self.update_frame()
    
    def toggle_playback(self):
        if not self.video_processor.current_video:
            return
            
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_btn.setText("Pause")
            self.playback_timer.start(1000 // 30)  # 30 fps preview
        else:
            self.play_btn.setText("Play")
            self.playback_timer.stop()
    
    def update_frame(self):
        if not self.video_processor.current_video:
            return
            
        try:
            frame = self.video_processor.get_frame(self.current_frame)
            if frame is not None:
                height, width = frame.shape[:2]
                scale = min(self.preview.width() / width, self.preview.height() / height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                
                frame = self.video_processor.resize_frame(frame, (new_width, new_height))
                image = QImage(frame.data, frame.shape[1], frame.shape[0], 
                             frame.shape[1] * 3, QImage.Format.Format_RGB888)  # Changed to RGB888
                pixmap = QPixmap.fromImage(image)
                self.preview.setPixmap(pixmap)
                
                if self.is_playing:
                    self.current_frame += 1
                    self.timeline_slider.setValue(self.current_frame)
                    
                    # Loop playback
                    if self.current_frame >= self.timeline_slider.maximum():
                        self.current_frame = 0
                        self.timeline_slider.setValue(0)
                        
        except Exception as e:
            print(f"Error updating frame: {str(e)}")
    
    def export_video(self):
        if not self.video_processor.current_video:
            self.preview.setText("Please import a video first")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Video",
            "",
            f"{self.format_combo.currentText()} Files (*.{self.format_combo.currentText().lower()})"
        )
        
        if file_path:
            try:
                format = self.format_combo.currentText().lower()
                resolution = self.res_combo.currentText()
                fps = self.fps_combo.currentText()
                
                start_time = self.start_time.value()
                end_time = self.end_time.value()
                
                if format == "gif":
                    self.video_processor.create_gif(
                        file_path,
                        start_time=start_time,
                        end_time=end_time,
                        resolution=resolution if resolution != "Original" else None,
                        fps=int(fps) if fps != "Original" else 15
                    )
                else:
                    self.video_processor.export_video(
                        file_path,
                        start_time=start_time,
                        end_time=end_time,
                        format=format,
                        resolution=resolution if resolution != "Original" else None,
                        fps=int(fps) if fps != "Original" else None
                    )
                
                self.preview.setText(f"Video exported successfully: {os.path.basename(file_path)}")
            except Exception as e:
                self.preview.setText(f"Error: {str(e)}")
    
    def apply_skeuomorphic_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #e0e0e0;
            }
            
            #sidebar {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 10px;
                border: 1px solid #c0c0c0;
            }
            
            #contentArea {
                background-color: #f0f0f0;
                border-radius: 10px;
                border: 1px solid #c0c0c0;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #f0f0f0, stop:1 #d0d0d0);
                border: 1px solid #a0a0a0;
                border-radius: 5px;
                padding: 8px;
                min-width: 50px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #ffffff, stop:1 #e0e0e0);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #d0d0d0, stop:1 #f0f0f0);
            }
            
            #importButton, #exportButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                border: 1px solid #2a5a8c;
                min-width: 100px;
            }
            
            #importButton:hover, #exportButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #5aa0f2, stop:1 #458acd);
            }
            
            #previewArea {
                background-color: #000000;
                border-radius: 5px;
                color: white;
            }
            
            #timeline {
                background-color: #ffffff;
                border-radius: 5px;
                border: 1px solid #c0c0c0;
                padding: 10px;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
            }

            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #4a90e2, stop:1 #357abd);
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
            
            QComboBox {
                background: white;
                border: 1px solid #a0a0a0;
                border-radius: 3px;
                padding: 5px;
            }
            
            QSpinBox {
                background: white;
                border: 1px solid #a0a0a0;
                border-radius: 3px;
                padding: 5px;
            }
            
            #sectionLabel {
                font-weight: bold;
                color: #333333;
                margin-top: 10px;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoEditor()
    window.show()
    sys.exit(app.exec()) 