async def is_admin(user):
    return user.role.name == 'ADMIN'


async def is_owner(user):
    return user.role.name == 'OWNER'


async def is_user(user):
    return user.role.name == 'USER'


async def is_registered(user):
    return user.role.name == 'REGISTERED'


async def is_owner_admin(user):
    return user.role.name in ['OWNER', 'ADMIN']


async def is_owner_admin_user(user):
    return user.role.name in ['OWNER', 'ADMIN', 'USER']
