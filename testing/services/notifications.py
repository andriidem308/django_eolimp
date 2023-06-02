from django.core.mail import send_mail
from django.template.loader import render_to_string

from testing.models import Student
from django_eolimp.settings import EMAIL_HOST_USER


def lecture_added_notify(lecture):
    teacher = lecture.teacher
    lecture_title = lecture.title
    group = lecture.group

    recipients = Student.objects.filter(group=group)
    recipients_email_list = [recipient.user.email for recipient in recipients]

    subject = f'New lecture "{lecture_title}"'
    message = render_to_string('messages/lecture_add.html', {'lecture_title': lecture_title, 'teacher': teacher})
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)


def problem_added_notify(problem):
    teacher = problem.teacher
    problem_title = problem.title
    group = problem.group

    recipients = Student.objects.filter(group=group)
    recipients_email_list = [recipient.user.email for recipient in recipients]

    subject = f'New problem "{problem_title}"'
    message = render_to_string('messages/problem_add.html', {'problem_title': problem_title, 'teacher': teacher})
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)
