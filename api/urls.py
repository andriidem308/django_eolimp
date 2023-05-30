from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import TeacherViewSet, StudentViewSet, ProblemViewSet, SolutionsViewSet, LectureViewSet

router = routers.DefaultRouter()
router.register('teachers', TeacherViewSet)
router.register('students', StudentViewSet)
router.register('problems', ProblemViewSet)
router.register('lectures', LectureViewSet)
router.register('solutions', SolutionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
