"""
Tests related to sending emails and moviepy merge video pipeline.
Not covered:
    - craft_email without error (as need to check if file is attached)
    - send_email (as no suitable return value to check if delivery was successful)

"""

import math
import unittest
from os import path
from moviepy.editor import VideoFileClip, CompositeVideoClip
from helpers.email_aws import configure_message, craft_email, craft_error_email
from helpers.moviepy_merge import resize_clip_wrt, merge_videos


class TestHelpers(unittest.TestCase):
    def test_configure_message_correctly(self):
        sender_email = "anytutor.official@gmail.com"
        receiver_email = "cybersecma@gmail.com"
        subject = 'Test Subject'
        body = 'Test Body'
        text = configure_message(sender_email, receiver_email, subject, body)
        self.assertIn(f"From: {sender_email}", text)
        self.assertIn(f"To: {receiver_email}", text)
        self.assertIn(f"Subject: {subject}", text)
        self.assertIn(f"{body}", text)

    def test_craft_error_email_correctly(self):
        sender_email = "anytutor.official@gmail.com"
        receiver_email = "cybersecma@gmail.com"
        name = "Test Name"

        text = craft_error_email(sender_email, receiver_email, name)
        subject = "Sorry! Your video file could not be generated :("
        body = "We are unable to generate your video file"
        self.assertIn(f"From: {sender_email}", text)
        self.assertIn(f"To: {receiver_email}", text)
        self.assertIn(f"Subject: {subject}", text)
        self.assertIn(f"{body}", text)
        self.assertIn(f"{name}", text)

    def test_resize_clip_wrt_correctly(self):
        filepath_1 = "./results/result_voice.mp4"  # Relative to where you run the test
        filepath_2 = "./sample_data/lessonVid.mp4"
        clip1 = VideoFileClip(fr'{filepath_1}')    # Use ./ instead of /
        clip2 = VideoFileClip(fr'{filepath_2}')
        clip2 = resize_clip_wrt(clip1, clip2)

        clip1_w, clip1_h = clip1.size[0], clip1.size[1]
        clip2_w, clip2_h = clip2.size[0], clip2.size[1]

        # Check if resized clip's dimensions are within 5% accurate
        self.assertTrue(math.isclose(clip1_w, clip2_w * 4, rel_tol=0.05))
        self.assertTrue(math.isclose(clip1_h, clip2_h * 4, rel_tol=0.05))

    def test_merge_video_outputs_file(self):
        merged_videos = merge_videos("./results/result_voice.mp4",
                                     "./sample_data/lessonVid.mp4", "./results/result_lesson.mp4")
        self.assertTrue(merged_videos)
        self.assertTrue(path.isfile("./results/result_lesson.mp4"))


if __name__ == '__main__':
    unittest.main()
