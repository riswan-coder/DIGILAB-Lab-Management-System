from django.db import models
from django.utils import timezone

class register(models.Model):
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    phone=models.CharField(max_length=120)
    password=models.CharField(max_length=120)
    status=models.CharField(max_length=120)
    reg_no=models.CharField(max_length=120)


class assignment_tbl(models.Model):
    user_id=models.CharField(max_length=150)
    date=models.CharField(max_length=150)
    report=models.CharField(max_length=120)
   
    reg_no=models.CharField(max_length=120)






class login_tbl(models.Model):
    status=models.CharField(max_length=150)
    time=models.CharField(max_length=150)
    date=models.CharField(max_length=120)
    attendence=models.CharField(max_length=120)
    system_no=models.CharField(max_length=120)
    user_id=models.CharField(max_length=120)


class Attendance(models.Model):
    user = models.ForeignKey('register', on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    system_no = models.CharField(max_length=50)
    status = models.CharField(max_length=10, default='present')  # Defaulting status to 'present'

    def __str__(self):
        return f"{self.user.email} - {self.login_time}"
   


class Logout_tbl(models.Model):
    status = models.CharField(max_length=150)
    time = models.CharField(max_length=150)  # or TimeField if time component only
    date = models.DateField()  # Add date field
    system_no = models.CharField(max_length=120)
    user_id = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.user_id} - {self.date} - {self.time} - {self.status} - {self.date}"
