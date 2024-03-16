from models.models import Users


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


class DataObject:
    def __init__(self, data):
        self._data = data

    @property
    def id(self):
        return int(self._data.get("user_id"))

    @property
    def fullname(self):
        return self._data.get("fullname")

    @property
    def phone(self):
        return int(self._data.get("phone"))

    @property
    def address(self):
        return self._data.get("address")

    @property
    def user_id(self):
        return int(self._data.get("user_id"))

    @property
    def vendor(self):
        return self._data.get("vendor")

    @property
    def model(self):
        return self._data.get("model")

    @property
    def defect(self):
        return self._data.get("defect")

    @property
    def customer_id(self):
        if self._data.get("customer_id") is None:
            return None
        return int(self._data.get("customer_id"))

    @property
    def order_id(self):
        if self._data.get("order_id") is None:
            return None
        else:
            return int(self._data.get("order_id"))

    @property
    def status(self):
        if self._data.get("status") is None:
            return None
        else:
            return self._data.get("status")
