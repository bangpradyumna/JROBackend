from django.db import models

# Create your models here.
class UploadedResearchObject(models.Model):
    oricid = models.CharField(max_length=100)
    uploadedfile = models.FileField(upload_to='ipfs')

class GithubResearchObject(models.Model):
    oricid = models.CharField(max_length=100)
    downloadedrepozip = models.FileField(upload_to='github')