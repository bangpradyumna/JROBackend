from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from journal.models import UploadedResearchObject, GithubResearchObject
import ipfshttpclient
import requests
from django.core.files import File
from os.path import basename
import requests
from tempfile import TemporaryFile
from urllib.parse import urlsplit

@csrf_exempt
@api_view(['POST'])
def addGithubRepo(request):
    github_zip_url = request.data['zip_url']

    with TemporaryFile() as tf:
        r = requests.get(github_zip_url, stream=True)
        for chunk in r.iter_content(chunk_size=4096):
            tf.write(chunk)

        tf.seek(0)
        ro = GithubResearchObject.objects.create( 
            oricid=request.META['HTTP_ORICID']       
        )
        ro.downloadedrepozip.save(basename(urlsplit(github_zip_url).path), File(tf))

    try:
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
        filepath = ro.downloadedrepozip.path
        res = client.add(filepath)
        print("The hash of file is : ",res['Hash'])
        researcher = "resource:org.jro.Researcher#"+str(ro.oricid)
        rojid=ro.id
        print("\n Adding the research object to the blockchain")
        r = requests.post('http://localhost:5002/api/Add', data = { "$class": "org.jro.Add", "rojId": rojid, "node": res['Hash'], "creator": researcher })
        print(r.content)
        if r.status_code==200:
            print("\n Success")
            data={"hash": res['Hash']}
        else:
            print(r.status_code)
            data={"hash":"error"}
    except ConnectionRefusedError:
        print("Connection error, Please ensure ipfs daemon is running.")    
    return Response(data,status=200)
