import Driver 

def unit_tests():

    #Test one:
    print("Beginning Test One")
    amenities_list_1 = [True,True,True,True,True,True]
    Driver.store_bars_and_attributes("New Brunswick NJ",1610,"Coolness","True",amenities_list_1)

    #Test Two
    print("Beginning Test Two")
    Driver.store_bars_and_attributes("New Brunswick NJ",1610,"Safety","True",amenities_list_1)

    #Test Three
    print("Beginning Test Three")
    Driver.store_bars_and_attributes("Detroit Michigan",5000,"Coolness","True",amenities_list_1)
    
    #Test Four
    print("Beginning Test Four")
    Driver.store_bars_and_attributes("Detroit Michigan",5000,"Safety","True",amenities_list_1)

    #Test Five
    print("Beginning Test Five")
    Driver.store_bars_and_attributes("Los Angelees CA",1610,"Coolness","True",[True,True,False,True,False,True])
    
    #Test Six
    print("Beginning Test Six")
    Driver.store_bars_and_attributes("Los Angelees CA",1610,"Safety","True",[False,True,True,True,True,True])


def component_tests():
   #Test one:
    print("Beginning Test One")
    amenities_list_1 = [True,True,True,True,True,True]
    Driver.store_bars_and_attributes("Jersey City NJ",40000,"Coolness","True",amenities_list_1)

    #Test Two
    print("Beginning Test Two")
    Driver.store_bars_and_attributes("London UK",15000,"Safety","False",amenities_list_1)

    #Test Three
    print("Beginning Test Three")
    Driver.store_bars_and_attributes("Detroit Michigan",5000,"Safety","True",[False,True,True,True,True,True])
    
    #Test Four
    print("Beginning Test Four")
    Driver.store_bars_and_attributes("Los Angeles CA",1610,"Coolness","False",amenities_list_1)

    #Test Five
    print("Beginning Test Five")
    Driver.store_bars_and_attributes("Moscow Russia",100000,"Safety","False",amenities_list_1)
    
def system_tests():
    print("Beginning Test One")
    amenities_list_1 = [True,True,True,True,True,True]
    Driver.store_bars_and_attributes("Jersey City NJ",40000,"Coolness","True",amenities_list_1)

    #Test Two
    print("Beginning Test Two")
    Driver.store_bars_and_attributes("London UK",2000,"Coolness","False",amenities_list_1)

    #Test Three
    print("Beginning Test Three")
    Driver.access_API("San Francisco CA",15000)
    
    #Test Four
    print("Beginning Test Four")
    Driver.access_API("Detroit Michigan",5000)

def main():
    print("Begin Tests...")
    #unit_tests()
    #component_tests()
    system_tests()
if __name__ == "__main__":
    main()