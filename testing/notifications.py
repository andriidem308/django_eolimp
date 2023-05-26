from django.core.mail import send_mail

from testing.models import Student
from django_eolimp.settings import EMAIL_HOST_USER


def lecture_added_notify(lecture):
    teacher = lecture.teacher
    lecture_title = lecture.title
    group = lecture.group

    recipients = Student.objects.filter(group=group)
    recipients_email_list = [recipient.user.email for recipient in recipients]
    recipients_email_list = ['nikiforovsh@gmail.com', 'andriidem308@gmail.com']

    subject = f'New lecture'
    message = f'Teacher {teacher.user} added a lecture {lecture_title}'

    send_mail(subject, message, EMAIL_HOST_USER, recipients_email_list)

    print(recipients_email_list)



#
# def send_notification_email(subject, message, recipient_list):
#     send_mail(subject, message, 'your-email@gmail.com', recipient_list, fail_silently=False)