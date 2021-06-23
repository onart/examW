from django.db import models

# Create your models here.
class Answers(models.Model):
    uip=models.CharField(max_length=20)
    q=models.IntegerField()
    a=models.TextField()

    def __str__(self):
        return '문제 {0} | IP {1} | 답안 {2}'.format(self.q, self.uip, self.a)
