'''
Dummy object for testing purposes
'''


class Dummy:
    '''
    Dummy object for testing purposes
    '''

    id = None
    name = ''
    num = None

    def __init__(self, dummy_id: int = None, name: str = None,
                 num: int = None) -> None:
        self.id = dummy_id
        self.name = name
        self.num = num

    def set_id(self, dummy_id: int):
        '''
        Sets dummy id
        '''
        self.id = dummy_id

        return self

    def get_id(self) -> int | None:
        '''
        Returns dummy id
        '''
        return self.id

    def set_name(self, dummy_name: str):
        '''
        Sets dummy name
        '''
        self.name = dummy_name

        return self

    def get_name(self) -> int | None:
        '''
        Returns dummy name
        '''
        return self.name

    def set_num(self, dummy_num: int):
        '''
        Sets dummy num
        '''
        self.num = dummy_num

        return self

    def get_num(self) -> int | None:
        '''
        Returns dummy num
        '''
        return self.num
