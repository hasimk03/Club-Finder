#System shall receive dictionary of bars and bar data from Raw_data_handler
#system gets referenced by prev system to create bar object and store bar attributes from dictionary keys
#This system will organize all data 
#Next system will compare data to user inputs and rank all bars then return appropriate bars recommendation

import math
class bar:                                          #superclass 
    def __init__(self,bar_data):
        self.id = bar_data['id']
        self.name = bar_data['name']
        self.is_closed = bar_data['is_closed']

        for s in bar_data['categories']:
            self.categories_list = [s]

        if 'transactions' in bar_data:             #check if key exists
            for z in bar_data['transactions']:     #grab all data in transaction list
                self.transactions_type_list = [z]  #store in transaction_type_list attribute
        
        self.location_list = [bar_data['location']['city'],bar_data['location']['state'],bar_data['location']['display_address'][0]]
        self.phone_number = bar_data['display_phone']
        if 'price' in bar_data:                 #checks if key exists before reference
            self.price = bar_data['price']      #does not always exist


    def display(self):
        #print("\n ----------Bar Class-------------:")
        print("Name: {0} \n   id: {1}\n   is_closed: {2}\n   phone number: {3}".format(self.name,self.id,self.is_closed,self.phone_number))
    
    def get_bar_name(self):
        return self.name

    class coolness:                                 
        def __init__(self,bar_data,max_value):            
            self.review_count = bar_data['review_count']
            self.average_rating = bar_data['rating']
            self.max_review_count = max_value
            #self.is_party_atmosphere = bar_data['party_scene']
            self.final_coolness_value = math.ceil(self.get_final_coolness_value(bar_data))              #final coolness value

        def get_final_coolness_value(self,bar_data):
            #Algo = 10*review_count + 4*rating  + 70*index
            return 10*(self.review_count/self.max_review_count) + 4*(self.average_rating) + 70* (self.get_coolness_index(bar_data))

        def get_coolness_index(self,bar_data):                                                          #algo to determine bars coolness
            coolness_index =0
            for s in bar_data['categories']:
               if (s['title'] == "Sports Bar" or s['title'] == "Dance Clubs" or s['title'] == "Dive Bars"):                                  #most cool
                   coolness_index = coolness_index + 3
               elif (s['title'] == "cocktailbars" or s['title'] == "tradamerican" or s['title'] == "beerbar" or s['title'] == "Music Venue" or s['title']=="pubs" or s['title'] == "Hot Dogs"):    #moderately cool - find a list of foods to replace this 
                   coolness_index = coolness_index + 2

            return (coolness_index /(3*len(bar_data['categories'])))                                     #convert to decimal (max=1)

       
        def display(self):
            #print("\n----------coolness Class----------")
            print("   Number of Reviews: {0}\n   Average Rating: {1}\n   Coolness Value: {2}".format(self.review_count,self.average_rating,self.final_coolness_value))
        
        def get_coolness_value(self):
            return self.final_coolness_value

    class safety:                                   #subclass 2
        def __init__(self,bar_data,max_review_count,min_review_count):
            self.surface_disinfection = False       #default 
            self.staff_temp_check     = False       #default
            self.max_review_count = max_review_count
            self.min_review_count = min_review_count
            self.final_safety_value = math.ceil(self.get_safety_val(bar_data))

        def get_safety_val(self,bar_data):
            #algo = 2(rating) + 30(100-coolness_index) + 60(1/review_count/min)
            cool_obj = bar(bar_data).coolness(bar_data,self.max_review_count)
            return 2*(cool_obj.average_rating) + 30*(1-cool_obj.get_coolness_index(bar_data)) + 60*(self.min_review_count/cool_obj.review_count)


        def display(self):
            #print("\n----------safety Class----------:")
            print("   Does staff disinfect surfaces? ",self.surface_disinfection)
            print("   Does staff get temp checks? ",self.staff_temp_check)
            print("   Final Safety Value: {0}".format(self.final_safety_value))

        def get_safety_value(self):
            return self.final_safety_value

    class amenities:                                #subclass 3
        def __init__(self):
            self.is_sportsbar = False
            self.offers_food  = False

        
        def display(self):
            #print("\n----------amenities class--------")
            print("   Sportsbar?: {0}\n   Offers Food?: {1}".format(self.is_sportsbar,self.offers_food))

def main():
    print("YelpHelp file")


if __name__ == "__main__":
    main()