class Person_Libs():
    def __init__(self, id=0, UserName=None, email=None, phone=None, address=None):
        self.aid=id
        self.UserName=UserName
        self.email=email
        self.phone=phone
        self.address=address


    def getid(self):
        return self.aid

    def getUserName(self):
        return self.UserName

    def getEmail(self):
        return self.email

    def getPhone(self):
        return self.phone

    def getAddress(self):
        return self.address


    def setid(self, id):
        self.id=id

    def setUserName(self, UserName):
        self.UserName=UserName


    def setEmail(self, email):
        self.email=email

    def setPhone(self, phone):
        self.mobile=phone

    def setAddress(self, address):
        self.address=address



    def __str__(self):
        return ('{},{},{},{},{},{}'.format(self.id, self.UserName, self.email, self.phone, self.address))