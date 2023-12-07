
class Test:

    @staticmethod
    def add_one(number):
        return Test.__add_one(number)

    @staticmethod
    def __add_one(number):
        # INF219v23
        x = 1
        y = 2
        return number + 1
