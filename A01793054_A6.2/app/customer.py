'''
Customer class
'''


class Customer:
    '''
    Customer class
    '''

    name = ''
    id = None

    def __init__(self, customer_id: int = None, name: str = ''):
        self.name = name
        self.id = customer_id

    def set_name(self, name: str):
        '''
        Sets the name of the customer
        '''
        self.name = name
        return self

    def get_name(self) -> str:
        '''
        Gets the name of the customer
        '''
        return self.name

    def set_id(self, customer_id: int):
        '''
        Sets the name of the customer
        '''
        self.id = customer_id
        return self

    def get_id(self) -> int | None:
        '''
        Gets the name of the customer
        '''
        return self.id
