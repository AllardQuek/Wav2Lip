"""
Take in some text provided by the user and return an audio file of the speech.
Example for Chinese text.
"""


import boto3

# Credentials can be configured using "aws configure"
polly_client = boto3.Session(region_name='ap-southeast-1').client('polly')
translate = boto3.client(service_name='translate',
                         region_name='ap-south-1')

text = "Hello world. What's your name?"

# Translate text to Chinese
result = translate.translate_text(Text=text,
                                  SourceLanguageCode="en",
                                  TargetLanguageCode="zh")
print('TranslatedText: ' + result.get('TranslatedText'))
print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))

# Convert text to speech
response = polly_client.synthesize_speech(VoiceId='Zhiyu',
                                          OutputFormat='mp3',
                                          LanguageCode="cmn-CN",
                                          Text=result.get('TranslatedText'),
                                          #   Text='你好， 你叫什么名字',
                                          #   Text='This is a sample text to be synthesized.',
                                          Engine='standard')

# Save audio output to file
with open('speech.mp3', 'wb') as file:
    file.write(response['AudioStream'].read())
