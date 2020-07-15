import requests


def get_model(path):
    r = requests.get("http://ec2-34-254-248-190.eu-west-1.compute.amazonaws.com:80/model/current")
    print(r.status_code)
    if r.status_code == 200:
        open(path, 'wb').write(r.content)

get_model('model2.tflite')