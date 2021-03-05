from accounts.models import User
from contents.models import Content


def get_user_contents(target_username):
    user = User.objects.get(username=target_username)
    contents = Content.objects.filter(user=user)

    return {'contents': contents}
