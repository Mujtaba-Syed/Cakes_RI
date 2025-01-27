from enum import Enum


class UserTypeChoice(Enum):
    ADMIN = "AD"
    CUSTOMER = "CU"
    SELLER = "SE"
    
    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)

    @classmethod
    def mappings(cls):
        return tuple((i.value, i.name.lower().replace('_', ' ')) for i in cls)


    @classmethod
    def admin_user(cls):
        return cls.ADMIN.value
    
    @classmethod
    def customer_user(cls):
        return cls.CUSTOMER.value
    
    @classmethod
    def seller_user(cls):
        return cls.SELLER.value

