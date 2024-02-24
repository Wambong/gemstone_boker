
from .models import UserProfile

def profile_picture(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

    return {'profile_picture_url': user_profile.profile_picture.url if user_profile else '/path/to/default/image.jpg'}
