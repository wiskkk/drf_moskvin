from rest_framework.routers import DefaultRouter

from .views import AnswerViewSet, TicketViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='user')
router.register(r'answers', AnswerViewSet, basename='answer')
router.register(r'tickets', TicketViewSet, basename='ticket')
urlpatterns = router.urls
