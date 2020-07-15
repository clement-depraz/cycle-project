from flask import Flask, request, send_file
import sys
import boto3
import tempfile
import io
app = Flask(__name__)

@app.route('/ping')
def index():
    return 'OK'

@app.route('/model/current', methods=['GET'])
def get_model():
    print('Fetching latest model', file=sys.stderr)
    s3 = boto3.client('s3')
    print('Downloading model from s3', file=sys.stderr)
    response = s3.get_object(Bucket='project-cycle', Key='models/latest/model.tflite')
    print('Sending back model', file=sys.stderr)
    return send_file(io.BytesIO(response['Body'].read()), attachment_filename='model.tflite', mimetype='application/octet-stream', as_attachment=True)

# https://flask.palletsprojects.com/en/1.1.x/quickstart/#file-uploads
@app.route('/image/new', methods=['POST'])
def upload_image():
    print('Receiving image', file=sys.stderr)
    f = request.files['image']
    print('Filename is ', f.filename, file=sys.stderr)
    cat = request.args.get("category")
    f.save('/var/www/html/images/' + f.filename)
    print('Image saved', file=sys.stderr)
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file('/var/www/html/images/' + f.filename, 'project-cycle', 'dataset/new/{}/{}'.format(cat, f.filename))
        print('Image uploaded to S3', file=sys.stderr)
    except Exception as e:
        print('Error uploading file to S3', e, file=sys.stderr)
    return 'Image uploaded'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    