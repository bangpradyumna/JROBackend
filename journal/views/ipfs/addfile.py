from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from django.core.files import File
from journal.models import UploadedResearchObject
import ipfshttpclient
import requests

@csrf_exempt
@api_view(['POST'])
@parser_classes([FileUploadParser])
def addFile(request):
    file_obj = request.data['file']
    print(request.META)
    ro = UploadedResearchObject.objects.create( 
        oricid=request.META['HTTP_oricid'],
        uploadedfile=file_obj
    )

    try:
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
        filepath = ro.uploadedfile.path
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
