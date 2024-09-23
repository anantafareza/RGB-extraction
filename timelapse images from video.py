from moviepy.editor import VideoFileClip

# Define video files and parameters
video_files = {
    "0 rpm.mp4": {"start_time": 0, "end_time": 120},
    "500 rpm.mp4": {"start_time": 0, "end_time": 120},
    "1000 rpm.mp4": {"start_time": 0, "end_time": 120},
    "1500 rpm.mp4": {"start_time": 0, "end_time": 120}
}

for video_file, params in video_files.items():
    input_video_path = f'[FILE PATH]{video_file}'
    trimmed_video_path = f'[FILE PATH]{video_file.replace(".mp4", "_trimmed.mp4")}'

    # Load the video file
    clip = VideoFileClip(input_video_path).subclip(params["start_time"], params["end_time"])
    
    # Write the trimmed video to a file without resizing
    clip.write_videofile(trimmed_video_path, codec='libx265', threads=12)

    print(f"Trimmed video saved to {trimmed_video_path}")
