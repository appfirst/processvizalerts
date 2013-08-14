from django.db import models

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
        alert= self.start_time+"to"+self.end_time +"for" +self.subject
        return alert

class Processes(models.Model):
    uid=models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        process = self.uid+"to"+self.end_time
        return process

    def __datetime__(self):
        return self.created_at
