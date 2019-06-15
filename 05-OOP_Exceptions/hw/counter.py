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
    counter = 0
    orig_init = cls.__init__

    def __add_count(self, *args, **kwargs):
        nonlocal counter
        counter += 1
        return orig_init(self, *args, **kwargs)

    def __get_created_instances(self=None):
        return counter

    def __reset_instances_counter(self=None):
        nonlocal counter
        res = counter
        counter = 0
        return res

    cls.__init__ = __add_count
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
    print(user.get_created_instances())
