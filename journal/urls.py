from django.urls import include, path
from journal.views.ipfs import addfile

urlpatterns = [ 
    path('ipfs/addfile/', addfile.addFile, name='AddFile'),
]