#class will hold a bar object, where each  object contains:
    #The name of the bar
    #A safety value
    #A coolness value




class Bar:
    def __init__(self,bar_name,index,coolness,safety):
        self.name = bar_name
        self.index = index
        self.coolness = coolness
        self.safety = safety

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index

    def get_coolness(self):
        return self.coolness

    def get_safety(self):
        return self.safety

def main():
    print("Start")



if __name__ == "__main__":
    main()