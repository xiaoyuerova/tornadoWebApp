class Father:
    a: int

    def __init__(self):
        self.a = 0

    def f_function(self):
        print('f_function work!\r')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.}


class Son(Father):
    a: int

    def __init__(self):
        self.a = 1


if __name__ == '__main__':
    p = Son()
    print(p.f_function())
    print(p.to_dict())
