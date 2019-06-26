"""
Написать декоратор instances_counter, который применяется к любому классу
и добавляет ему 2 метода:
get_created_instances - возвращает количество созданых экземпляров класса
reset_instances_counter - сбросить счетчик экземпляров,
возвращает значение до сброса
Имя декоратора и методов не менять

Ниже пример использования
"""


def instances_counter(cls):
    """Some code"""
    print(cls)
    cls.__counter = 0
    # cls_new = cls.__new__

    def __new(cls, *args, **kwargs):
        cls.__counter += 1
        return super(cls, cls).__new__(cls, *args, **kwargs)
        # return cls_new_(cls, *args, **kwargs)

    @classmethod
    def __get_created_instances(cls=cls):
        return cls.__counter

    @classmethod
    def __reset_instances_counter(cls=cls):
        res = cls.__counter
        cls.__counter = 0
        return res

    cls.__new__ = __new
    cls.get_created_instances = __get_created_instances
    cls.reset_instances_counter = __reset_instances_counter
    return cls


@instances_counter
class User:
    pass


if __name__ == '__main__':

    print(User.get_created_instances())  # 0
    user, user_2, _ = User(), User(), User()
    print(user.get_created_instances())
    print(user_2.get_created_instances())  # 3
    user.reset_instances_counter()  # 3
    print(User.get_created_instances())
