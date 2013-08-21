from django.db import models
import datetime

class Servers(models.Model):
    server_id=models.CharField(max_length=20)
    nickname=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        server= self.server_id+ self.nickname
        return server

class AlertHistories(models.Model):
    start_time=models.CharField(max_length=20)
    end_time=models.CharField(max_length=20)
    subject=models.CharField(max_length=500)

    def __unicode__(self):
        return self.subject

class Processes(models.Model):
    uid=models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    cpu_data=models.CharField(max_length=10)
    memory_data=models.CharField(max_length=10)

    def __unicode__(self):
        process = self.uid+self.cpu_data+self.memory_data
        return process

