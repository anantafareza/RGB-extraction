from moviepy.editor import VideoFileClip

# Define video files and parameters
video_files = {
    "0 rpm.mp4": {"start_time": 2.5, "end_time": 127.5},
    "500 rpm.mp4": {"start_time": 9.5, "end_time": 134.5},
    "1000 rpm.mp4": {"start_time": 2, "end_time": 127},
    "1500 rpm.mp4": {"start_time": 4, "end_time": 129}
}

for video_file, params in video_files.items():
    input_video_path = f'E:\\pH gradient\\{video_file}'
    trimmed_video_path = f'E:\\pH gradient\\{video_file.replace(".mp4", "_trimmed.mp4")}'

    # Load the video file
    clip = VideoFileClip(input_video_path).subclip(params["start_time"], params["end_time"])
    
    # Write the trimmed video to a file without resizing
    clip.write_videofile(trimmed_video_path, codec='libx265', threads=12)

    print(f"Trimmed video saved to {trimmed_video_path}")
