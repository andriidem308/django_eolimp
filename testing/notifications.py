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
    recipients_email_list = ['nikiforovsh@gmail.com', 'andriidem308@gmail.com']

    subject = f'New lecture "{lecture_title}"'
    message = render_to_string('messages/lecture_add.html', {'lecture_title': lecture_title, 'teacher': teacher})
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)


def problem_added_notify(problem):
    teacher = problem.teacher
    problem_title = problem.title
    group = problem.group

    recipients = Student.objects.filter(group=group)
    recipients_email_list = [recipient.user.email for recipient in recipients]
    recipients_email_list = ['nikiforovsh@gmail.com', 'andriidem308@gmail.com']

    subject = f'New problem "{problem_title}"'
    message = render_to_string('messages/problem_add.html', {'problem_title': problem_title, 'teacher': teacher})
    send_mail(subject, '', EMAIL_HOST_USER, recipients_email_list, html_message=message)


'''
def test_added_notify(test):
    subject = f'New test "{test_title}"'
    message = f'Hi Student!\nYou receive new test "{test_title}" from your teacher {teacher.user.first_name} {teacher.user.last_name}.\n\n\n' \
              f'We understand that you possess an insatiable thirst for knowledge and an unwavering dedication to your education. This task has been meticulously crafted to captivate your imagination, challenge your intellect, and provide a platform for your ideas to flourish.\n\n' \
              f'To access the details of the task, simply log in to your student portal and navigate to the course page. There, you'll find the task waiting eagerly for your brilliant touch. Prepare to immerse yourself in a world of discovery, innovation, and limitless possibilities. \n\n' \
              f'Remember, greatness lies within you, and this task is your canvas to unleash your potential. Don't be afraid to think outside the box, explore uncharted territories, and embrace your unique perspective. We believe in your ability to rise above challenges and inspire those around you.\n\n' \
              f'Should you have any questions, require guidance, or need support along the way, our dedicated team is always here to assist you. Reach out to us at alphadjeolimp@gmail.com, and we'll be thrilled to provide the assistance you need.\n\n' \
              f'Now, without further ado, it's time to embark on this thrilling quest! Prepare to amaze yourself and the world with your talent, dedication, and unwavering spirit. We can't wait to witness the incredible results you're about to achieve!\n\n' \
              f'Wishing you boundless inspiration, remarkable accomplishments, and an unforgettable journey.'
'''
#
# def send_notification_email(subject, message, recipient_list):
#     send_mail(subject, message, 'your-email@gmail.com', recipient_list, fail_silently=False)
