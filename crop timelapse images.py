import cv2
import os

def extract_and_crop_frames(video_path, output_folder, intervals, roi):
    os.makedirs(output_folder, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file at path {video_path}.")
        return []
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval_frames = [int(t * fps) for t in intervals]
    
    max_frames = int(180 * fps)
    frame_count = 0
    extracted_frames = []
    
    # Extract base filename without extension
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    
    while cap.isOpened() and frame_count <= max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count in interval_frames:
            x, y, w, h = roi
            frame_h, frame_w, _ = frame.shape
            x = min(max(x, 0), frame_w - w)
            y = min(max(y, 0), frame_h - h)
            cropped_frame = frame[y:y+h, x:x+w]
            
            denoised_frame = cv2.fastNlMeansDenoisingColored(cropped_frame, None, 1.5, 1.5, 7, 21)
            
            timestamp = frame_count / fps
            # Updated output filename
            output_path = os.path.join(output_folder, f"{base_name}_frame_{timestamp:.0f}s.png")
            cv2.imwrite(output_path, denoised_frame)
            print(f"Saved: {output_path}")  # Debug statement
            extracted_frames.append((timestamp, output_path))
        
        frame_count += 1
    
    cap.release()
    return extracted_frames

# Example usage
video_path = r'[FILE PATH]'  # Use the actual filename
output_folder = r'[FILE PATH]'

intervals = list(range(0, 61, 5)) #intervals
roi = (1371, 915, 510, 370) #region of interest

extracted_frames = extract_and_crop_frames(video_path, output_folder, intervals, roi)

for timestamp, image_path in extracted_frames:
    print(f"Saved frame at {timestamp}s: {image_path}")
