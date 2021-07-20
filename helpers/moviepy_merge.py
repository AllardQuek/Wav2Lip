import math
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip


def resize_clip_wrt(clip1, clip2):
    """
    Return the second video resized to 1/4 the size of the first video.
    """
    w1, h1 = clip1.size
    w2, h2 = clip2.size

    desired_w = 0.25 * w1
    resize_factor = desired_w / w2
    clip2 = clip2.resize(resize_factor)
    return clip2


def merge_videos(filepath_1, filepath_2, filepath_out):
    """
    Overlay second video in the bottom right corner of the first video.
    """
    # If the video generation failed, merge fails
    if not os.path.isfile(filepath_1) or not os.path.isfile(filepath_2):
        print("Error: The filepath(s) are invalid.")
        return False

    # Merge original lesson video with Wav2Lip result video
    clip1 = VideoFileClip(fr'{filepath_1}')    # Use ./ instead of /
    clip2 = VideoFileClip(fr'{filepath_2}')

    clip2 = resize_clip_wrt(clip1, clip2)
    composite_clip = CompositeVideoClip([clip1,
                                         clip2.set_position(
                                             ("right", "bottom"))
                                         .set_start(0).crossfadein(1)])

    # Use a temp audio file if audio is not working
    # It seems overriding an existing file will result in second video not running correctly
    try:
        # final_clip.write_videofile(r'./results/result_voice.mp4')
        composite_clip.write_videofile(fr'{filepath_out}',
                                       codec='libx264',
                                       audio_codec='aac',
                                       temp_audiofile='temp-audio.m4a',
                                       remove_temp=True
                                       )
        return True
    except Exception as e:
        print(e)
        return False


# Test out merge_videos() if run from command line
if __name__ == "__main__":
    merged_videos = merge_videos("../results/result_voice.mp4",
                                 "../sample_data/lessonVid.mp4", "../results/result_lesson.mp4")
