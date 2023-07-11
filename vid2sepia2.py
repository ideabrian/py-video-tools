from moviepy.editor import VideoFileClip
import cv2
import numpy as np
import os

def extract_frames(video_path, frames_dir):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        raise Exception("Could not open video")

    # Read until video is completed
    frame_number = 0
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Save each frame as an image
            cv2.imwrite(os.path.join(frames_dir, f"frame_{frame_number:04d}.jpg"), frame)
            frame_number += 1
        else:
            break

    # Release the video capture object
    cap.release()

    return frame_number

def apply_sepia(frames_dir, frame_number):
    # Define the sepia effect transformation matrix
    sepia_kernel = np.array([[0.272, 0.534, 0.131],
                            [0.349, 0.686, 0.168],
                            [0.393, 0.769, 0.189]])

    # Apply sepia effect to each frame
    for i in range(frame_number):
        frame_path = os.path.join(frames_dir, f"frame_{i:04d}.jpg")
        
        # Read the frame
        frame = cv2.imread(frame_path)
        
        # Apply the sepia kernel
        sepia_frame = cv2.transform(frame, sepia_kernel)
        
        # Write the modified frame back to the file
        cv2.imwrite(frame_path, sepia_frame)

def assemble_video(frames_dir, frame_number, video_path, output_video_path):
    # Get the frame rate of the original video
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    # Read the first frame to get the frame dimensions
    first_frame_path = os.path.join(frames_dir, "frame_0000.jpg")
    first_frame = cv2.imread(first_frame_path)

    # Define the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    video_writer = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (first_frame.shape[1], first_frame.shape[0]))

    # Write each frame to the video
    for i in range(frame_number):
        frame_path = os.path.join(frames_dir, f"frame_{i:04d}.jpg")
        
        # Read the frame
        frame = cv2.imread(frame_path)
        
        # Write the frame to the video
        video_writer.write(frame)

    # Release the video writer
    video_writer.release()

import subprocess

def process_video(video_path, frames_dir, output_video_path):
    # Extract frames
    frame_number = extract_frames(video_path, frames_dir)
    # Apply sepia effect
    apply_sepia(frames_dir, frame_number)
    # Assemble video without audio
    assemble_video(frames_dir, frame_number, video_path, output_video_path)

    # Prepare the final output path
    final_output_path = output_video_path.replace('.mp4', '_final.mp4')

    # Use ffmpeg to copy the audio from the original video to the new video
    command = f"ffmpeg -i {video_path} -i {output_video_path} -c:v copy -c:a aac -map 0:a:0 -map 1:v:0 {final_output_path}"
    subprocess.run(command, shell=True, check=True)

    return final_output_path

#final_video = process_video(video_path, frames_dir, output_video_path)

#def process_video(video_path, frames_dir, output_video_path):
#    # Extract frames
#    frame_number = extract_frames(video_path, frames_dir)
#    # Apply sepia effect
#    apply_sepia(frames_dir, frame_number)
#    # Assemble video without audio
#    assemble_video(frames_dir, frame_number, video_path, output_video_path)

#    # Extract audio from original video
#    clip = VideoFileClip(video_path)
#    audio = clip.audio

#    # Load the transformed video
#    new_clip = VideoFileClip(output_video_path)

#    # Set the audio of the new clip to the original audio
#    new_clip = new_clip.set_audio(audio)

# # Write the output to a new file, preserving the original transformed video
#    final_output_path = output_video_path.replace('.mp4', '_final.mp4')
#    new_clip.write_videofile(final_output_path, codec='libx264', audio_codec='aac')

    #return final_output_path

def test_video_processing():
    video_path = "./test-videos/test2.mp4"
    frames_dir = "./frames"
    output_video_path = "./sepia-videos/test2.sepia.mp4"

    # Make sure the frames directory exists
    os.makedirs(frames_dir, exist_ok=True)

    process_video(video_path, frames_dir, output_video_path)
    
    assert os.path.isfile(output_video_path), "Output video file was not created"

test_video_processing()
