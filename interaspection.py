# print(issubclass.__doc__)

class Shape:
    pass

class Circle(Shape):
    
    def __init__(self, radius):
        self.radius =  radius

circle = Circle(10)
print(issubclass(Circle, Shape))