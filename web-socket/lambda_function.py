import boto3
import time
from botocore.vendored import requests
from websocket_client import websocket


def lambda_handler(event, context):

    sm_client = boto3.client('sagemaker')
    s3_client = boto3.client("s3")
    notebook_instance_name = 'Wav2Lip-demo'
    url = sm_client.create_presigned_notebook_instance_url(NotebookInstanceName=notebook_instance_name)['AuthorizedUrl']

    url_tokens = url.split('/')
    http_proto = url_tokens[0]
    http_hn = url_tokens[2].split('?')[0].split('#')[0]

    s = requests.Session()
    r = s.get(url)
    cookies = "; ".join(key + "=" + value for key, value in s.cookies.items())

    ws = websocket.create_connection(
        "wss://{}/terminals/websocket/1".format(http_hn),
        cookie=cookies,
        host=http_hn,
        origin=http_proto + "//" + http_hn
    )
 
    # TODO: Take the input file(s) and upload to S3

    # * Once files are uploaded, run our SageMaker notebook
    ws.send("""[ "stdin", "jupyter nbconvert --execute --to notebook --inplace /home/ec2-user/SageMaker/Wav2Lip/Wav2Lip-socket.ipynb --ExecutePreprocessor.kernel_name=python3 --ExecutePreprocessor.timeout=1500\\r" ]""")

    time.sleep(1)
    ws.close()

    return "looking clean"