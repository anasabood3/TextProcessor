
class Item():
    def __init__(self ,sender ,receiver ,phone_number ,destination ,amount):
        self.receiver = receiver
        self.sender = sender
        self.phone_number = phone_number
        self.amount = amount
        self.destination = destination
    def __iter__(self):
        values = []
        for attr, value in self.__dict__.items():
            values.append(value)
        return values
    def __str__(self):
        return "Receiver:" + str(self.receiver) +",Amount:" + str(self.amount) + ",Destination:" + str(
            self.destination)

    def __eq__(self, other):
        return self.__iter__() == other.__iter__()

