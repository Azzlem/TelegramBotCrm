from models.users import Users


class UserFormatter:
    model = Users

    @classmethod
    async def convert_to_add(cls, data):
        user = cls.model(
            telegram_id=data.id,
            fullname=f'{data.first_name} {data.last_name}',
            username=data.username
        )
        return user

    @classmethod
    async def convert_to_base_list(cls, users):
        message = f'Информация об инженерах:\n\n'

        for user in users:
            phone = user.phone if user.phone is not None else "нет телефона"
            message += (f"{user.fullname}\n"
                        f"Никнэйм: {user.username}\n"
                        f"Права: {user.role.name}\n"
                        f"Телефон: {phone}\n"
                        f"Зарегистрирован: {user.created_on.strftime('%Y-%m-%d')}\n\n"
                        )
        return message

