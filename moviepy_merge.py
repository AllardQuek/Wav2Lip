import os
from moviepy.editor import VideoFileClip, CompositeVideoClip
from email_aws import send_email 


def merge_videos():
    wav2lip_result_path = "./results/result_voice.mp4"
    lesson_path = "./sample_data/lessonVid.mp4"

    # If the video generation failed, merge fails
    if not os.path.isfile(wav2lip_result_path) or not os.path.isfile(lesson_path):
        return False

    # Merge original lesson video with Wav2Lip result video
    clip1 = VideoFileClip(r'./sample_data/lessonVid.mp4')    # Use ./ instead of /
    clip2 = VideoFileClip(r'./results/result_voice.mp4')

    w1,h1 = clip1.size
    w2,h2 = clip2.size

    # Resize Wav2Lip result video to 1/4 the size of the original lesson video
    desired_w = 0.25 * w1
    resize_factor = desired_w / w2
    clip2 = clip2.resize(resize_factor)
    w_final,h_final = clip2.size
    print(w_final,h_final)

    composite_clip = CompositeVideoClip([clip1,
                                         clip2.set_position(("right","bottom"))
                                              .set_start(0).crossfadein(1)])

    # Use a temp audio file if audio is not working
    # It seems overriding an existing file will result in second video not running correctly
    try:
        # final_clip.write_videofile(r'./results/result_voice.mp4')
        composite_clip.write_videofile(r'./results/result_lesson.mp4', 
                            codec='libx264', 
                            audio_codec='aac', 
                            temp_audiofile='temp-audio.m4a', 
                            remove_temp=True
                            )
        print("VIDEOS MERGED")
        return True
    except Exception as e:
        print(e)
        return False

# Test out merge_videos() if run from command line
if __name__ == "__main__":
    merged_videos = merge_videos()
    send_email(is_lesson=True) if merged_videos else send_email(error=True)
    print("DONE")