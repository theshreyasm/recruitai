import cv2
import os

def extract_frames(video_path = "videos/video.mp4", output_folder = "video_frames", frame_rate=2):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video file opened successfully
    if not cap.isOpened():
        print("Error: Couldn't open the video file.")
        return
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    frame_count = 0
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        
        # Check if the frame was read successfully
        if not ret:
            break
        
        # Calculate the current time in the video (in seconds)
        current_time_sec = frame_count / cap.get(cv2.CAP_PROP_FPS)
        
        # If the current time is a multiple of the frame rate, save the frame
        if current_time_sec % frame_rate == 0:
            # Construct the output file path
            output_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            
            # Save the frame as an image
            cv2.imwrite(output_path, frame)
            print(f"Saved frame {frame_count}")
        
        frame_count += 1
    
    # Release the video capture object
    cap.release()
    print("Frame extraction complete.")



