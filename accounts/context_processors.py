from notifications.models import Notification
from .models import UserProfile


def profile_picture(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

    return {'profile_picture_url': user_profile.profile_picture.url if user_profile else '/path/to/default/image.jpg'}


def notification_count(request):
    if request.user.is_authenticated:
        notification_count = Notification.objects.filter(recipient=request.user, unread=True).count()
    else:
        notification_count = 0
    return {'notification_count': notification_count}


from notifications.models import Notification


def unread_notifications(request):
    unread_notifications = None
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(recipient=request.user, unread=True)
    return {'unread_notifications': unread_notifications}
