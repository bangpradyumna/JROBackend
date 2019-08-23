from django.urls import include, path
from journal.views.ipfs import addfile
from journal.views.github import addgithubrepo

urlpatterns = [ 
    path('ipfs/addfile/', addfile.addFile, name='Add File'),
    path('github/addrepo/', addgithubrepo.addGithubRepo, name='Add Github Repo'),
]