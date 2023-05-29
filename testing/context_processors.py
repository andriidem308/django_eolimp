from testing.models import Problem, Student, Solution, Teacher


def panel_context(request):
    result = {}
    user = request.user
    if user.is_authenticated:
        if user.is_student:
            student = Student.objects.get(user=user)
            solutions = Solution.objects.filter(student=student)
            problem_list = [solution.problem.id for solution in solutions]
            problems = Problem.objects.filter(group=student.group).exclude(pk__in=problem_list).order_by('deadline')[:5]

            result = {
                'student_problems': problems,
            }
        elif user.is_teacher:
            teacher = Teacher.objects.get(user=user)
            problems = Problem.objects.filter(teacher=teacher)
            solutions = Solution.objects.filter(problem__id__in=problems).filter(checked=False).order_by('date_solved')[
                        :5]
            result = {
                'teacher_solutions': solutions,
            }

    return result
