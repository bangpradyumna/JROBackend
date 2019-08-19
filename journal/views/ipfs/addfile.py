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
    # print("Printing Request dictionary")
    # print(request.data)
    # print("Printing File")
    # print(file_obj.read())
    # file_stored = File(file_obj)
    ro = UploadedResearchObject.objects.create( # Need to change the oricid value
        oricid="123",
        uploadedfile=file_obj
    )

    try:
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
        # filename = input("Enter the filename stored in current directory (with extension)")
        filepath = ro.uploadedfile.path
        res = client.add(filepath)
        print("The hash of file is : ",res['Hash'])
        # rid = input("\nEnter the Researcher ID")
        # researcher = "resource:org.jro.Researcher#"+str(rid)
        # rojid = input("\nEnter the Research object ID")
        # print("\n Adding the research object to the blockchain")
        # r = requests.post('http://localhost:3000/api/Add', data = { "$class": "org.jro.Add", "rojId": rojid, "node": res['Hash'], "creator": researcher })
        # if r.status_code==200:
            # print("\n Success")
    except ConnectionRefusedError:
        print("Connection error, Please ensure ipfs daemon is running.")    
    return Response(status=200)