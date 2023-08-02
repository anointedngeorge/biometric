from dashboard.urls.auth import auth_pattern
from dashboard.urls.courses import course_pattern
from dashboard.urls.lecturer import lecturer_pattern
from dashboard.urls.subjects import subject_pattern
from dashboard.urls.departments import department_pattern
from dashboard.urls.level import level_pattern
from dashboard.urls.students import student_pattern
from dashboard.urls.attendance import attendance_pattern

app_name = 'dashboard'
urlpatterns = []

# extend each patterns
urlpatterns.extend(auth_pattern)
urlpatterns.extend(course_pattern)
urlpatterns.extend(lecturer_pattern)
urlpatterns.extend(subject_pattern)
urlpatterns.extend(department_pattern)
urlpatterns.extend(level_pattern)
urlpatterns.extend(student_pattern)
urlpatterns.extend(attendance_pattern)