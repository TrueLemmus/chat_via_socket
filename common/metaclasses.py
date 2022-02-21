import dis

class ClientVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        self.methods = ClientVerifier.get_methods(clsdict)
        self.attrs = ClientVerifier.get_attributes(clsdict)
        ClientVerifier.validate_methods(self.methods)       
        ClientVerifier.validate_attributes(self.attrs)
        super().__init__(clsname, bases, clsdict)
        
    
    @staticmethod      
    def get_methods(clsdict):
        methods = []
        for func in clsdict:
            # Пробуем
            try:
                ret = dis.get_instructions(clsdict[func])
                # Если не функция то ловим исключение
            except TypeError:
                pass
            else:
                # Раз функция разбираем код, получая используемые методы.
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        return methods
    
    
    @staticmethod
    def get_attributes(clsdict):
        attrs = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                # Раз функция разбираем код, получая используемые атрибуты.
                for i in ret:
                    if i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            # заполняем список атрибутами, использующимися в функциях класса
                            attrs.append(i.argval)
        return attrs
    
    
    @staticmethod    
    def validate_methods(methods):
        # Если обнаружено использование недопустимого метода accept, listen, socket бросаем исключение:
        for command in ('accept', 'listen'):
            if command in methods:
                raise TypeError('В классе обнаружено использование запрещённого метода')
        # Вызов get_message или send_message из utils считаем корректным использованием сокетов
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
    
    
    @staticmethod
    def validate_attributes(attrs):
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')


class ServerMaker(type):
    def __init__(self, clsname, bases, clsdict):
        self.methods = ServerMaker.get_methods(clsdict)
        self.attrs = ServerMaker.get_attributes(clsdict)
        ServerMaker.validate_methods(self.methods)       
        ServerMaker.validate_attributes(self.attrs)
        super().__init__(clsname, bases, clsdict)
        
    
    @staticmethod      
    def get_methods(clsdict):
        methods = []
        for func in clsdict:
            # Пробуем
            try:
                ret = dis.get_instructions(clsdict[func])
                # Если не функция то ловим исключение
            except TypeError:
                pass
            else:
                # Раз функция разбираем код, получая используемые методы.
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        return methods
    
    
    @staticmethod
    def get_attributes(clsdict):
        attrs = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                # Раз функция разбираем код, получая используемые атрибуты.
                for i in ret:
                    if i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            # заполняем список атрибутами, использующимися в функциях класса
                            attrs.append(i.argval)
        return attrs
    
    
    @staticmethod    
    def validate_methods(methods):
        if 'connect' in methods:
            raise TypeError('Использование метода connect недопустимо в серверном классе')
    
    
    @staticmethod
    def validate_attributes(attrs):
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')