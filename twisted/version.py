class Version:
    def __init__(self, major=0, minor=0, micro=0):
        self.major = major
        self.minor = minor
        self.micro = micro

    def short(self):
        return f"{self.major}.{self.minor}.{self.micro}"


version = Version()
major = version.major
minor = version.minor
micro = version.micro
