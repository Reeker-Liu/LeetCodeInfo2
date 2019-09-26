from users.models import User

def add_user(name, id, email, version, ac):
    User.objects.create(name=name, id=id, email=email, version=version, yesterday=ac, today=ac, latest=ac)
    return

def update_user_latest(id, latest):
    return

def update_user(id, latest):
    return

def remove_user(id):
    return

def clear_all():
    return

def get_single(id):
    user = User.objects.get(id)
    return user

def get_all():
    return User.objects.all()


if __name__ == '__main__':
    print(1)
    add_user('reeker', 'huaji', '934422900@qq.com', 0, 157)
    add_user('spring', 'we98', '1231312@qq.com', 0, 99)
    print(get_all())
