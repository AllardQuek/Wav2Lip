"""
Take in some text provided by the user and return an audio file of the speech.
Example for Chinese text.
"""

import boto3

# Credentials can be configured using "aws configure"
polly_client = boto3.Session(region_name='ap-southeast-1').client('polly')

response = polly_client.synthesize_speech(VoiceId='Raveena',
                OutputFormat='mp3', 
				# LanguageCode="cmn-CN",
                # Text = '你好， 你叫什么名字',
                Text = 'This is a sample text to be synthesized.',
                Engine = 'standard')

file = open('speech.mp3', 'wb')
file.write(response['AudioStream'].read())
file.close()