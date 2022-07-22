import requests
import json
import YelpHelper as YelpHelp
import Bars_class as B
import Yelp_page_scraper as scrape
#import YelpHelp


#This method accessees the Yelp API with loc and rad inputs - returns dictionary of bars and relevant data
def access_API(loc,rad):
    #unique key to access API & dict 'headers' to access API via unique key 
    api_key = 'ozFbeHZhNgSDjqO2NE6dB4w0oI-UtOEy-cnVXSOlUMwuAj_MaF_1D9I3VF17a7H2j9cvJheUzNjEVgCwnZ_J9LQ7486uzuAL5p5T1FEXjJntV4oBjQoU9r-Mz70yYnYx'
    header = {                                                                 
            'Authorization': 'Bearer %s' % api_key                          
    }


    url='https://api.yelp.com/v3/businesses/search'                             #url linking to search feature

    parameters = {                                                              #constraints for Yelp search
        'term'       : 'bar',
        'location'   : loc,
        'radius'     : rad,
        'sort_by'    : 'review_count',                                           #allows for list to be sorted by popularity
        'categories' : '(pubs,All)'
    }
 
    req = requests.get(url,params=parameters,headers = header)                  #makes get request 
    if (req.status_code !=200):                                                 #print status code if error occured
        print("Status Code is",req.status_code)
        
    bar_dict = json.loads(req.text)                                      #returns text of request as dict

    try:
        bar_name_list = [""] * len(bar_dict['businesses'])                          #intialize list of bars
    except KeyError:
        print("Location or radius was not entered")
    
    for i in range(len(bar_dict['businesses'])):                                #run thru bar dict
        bar_name_list[i] = bar_dict['businesses'][i]['name']                        #store bar names in bar_name_list

        #delete certain keys for each business listed
        del bar_dict['businesses'][i]['alias']
        del bar_dict['businesses'][i]['image_url']
        del bar_dict['businesses'][i]['coordinates']
        del bar_dict['businesses'][i]['location']['address1']
        del bar_dict['businesses'][i]['location']['address2']
        del bar_dict['businesses'][i]['location']['address3']

    #print(json.dumps(bar_dict,indent=2))

    return bar_dict

def collect_constraints_from_user():
    loc = input("Where do you want to go clubbing? Enter your response in the following format: City,State\n  >>>")   #desired location
    if loc == "":
        raise Exception("Location was not entered!")
    
    rad = input("Enter search radius for {0} in meters (mile =~ 1610 meters) \n  >>>".format(loc))                                          #search radius(mi->m)
    if rad == "":
        raise Exception("Search radius was not entered!")

    Priority = input("Which is more importance to you when choosing a bar to visit, safety or coolness?\n>>>")
    more_constraints_in = input("Would you like to provide more inputs? Enter Yes or No\n>>>")   #string input
    more_constraints_in = "Yes"
    
    if (more_constraints_in == "Yes" or more_constraints == "yes"):
        more_constraints = True
    elif (more_constraints_in == "No" or more_constraints == "no"):
        more_constraints = False
    else:
        more_constraints = False

    #initialize variables
    Free_wifi = "No"; Full_bar = "No"; Masks_required = "No" 
    pool_table = "No"; outdoor_seat = "No"; wheelchair_access = "No"

    #grab amenities inputs from user
    if (more_constraints):                                                                  #if amenities are desired
        print("Amenities Offered: Answer Yes or No for the following Questions")
        input_list = [1,2,3,4,5,6] 

        input_list[0] = input("Do you want the bar to offer Free Wifi?\n>>>")   #"Yes" 
        input_list[1] = input("Do you want the bar to have a full bar?\n>>>")
        input_list[2] = input("Do you want the bar to require masks?\n>>>")
        input_list[3] = input("Do you want the bar to have a pool table?\n>>>")
        input_list[4] = input("Do you want the bar to offer a outdoor seating?\n>>>")
        input_list[5] = input("Do you want the bar to be wheelchair accessible?\n>>>")

        for z in range(len(input_list)):
            if input_list[z] == "Yes" or input_list[z] == "y" or input_list[z] == "yes":
                input_list[z] = True 
            else:
                input_list[z] = False

       
        
        store_bars_and_attributes(loc,rad,Priority,more_constraints,input_list)        #call method to onvert raw data into objects
        


#This method operates on raw bar dictionary grabed from yelp API
#Begins creating lists and dictionaries containing bar objects (and others)
#Lists/dictionaries are then sorted and organized
def store_bars_and_attributes(loc,rad,Priority,more_constraints,input_list):

    user_inputs = {
            "Free_wifi" : input_list[0],
            "Full_bar" : input_list[1],
            "Masks_required" : input_list[2],
            "Pool_table" : input_list[3],
            "Outdoor_seating" : input_list[4],
            "Wheelchair_access" : input_list[5]
        }


    bar_dict = access_API(loc,rad)          #accesses API to grab raw data

 
    last_index = len(bar_dict['businesses'])-1
    max_num_reviews = [bar_dict['businesses'][0]['name'],bar_dict['businesses'][0]['review_count']]
    min_num_reviews = [bar_dict['businesses'][last_index]['name'],bar_dict['businesses'][last_index]['review_count']]

    #create two list of bars - indicies correspond to indicies in dict
    bar_names           = [""] * len(bar_dict['businesses'])                #bar names
    bar_coolness_values = [""] * len(bar_dict['businesses'])                #bar coolness values
    bar_safety_values   = [""] * len(bar_dict['businesses'])                #bar safety values


    for i in range(last_index+1):
        #bar [parent] object
        bar1_obj = YelpHelp.bar(bar_dict['businesses'][i])
        bar_names[i]= bar1_obj.get_bar_name()

        #coolness [child] object
        bar1_obj_child1 = bar1_obj.coolness(bar_dict['businesses'][i],max_num_reviews[1])
        bar_coolness_values[i] = bar1_obj_child1.get_coolness_value()

        #safety [child] object
        bar1_obj_child2 = bar1_obj.safety(bar_dict['businesses'][i],max_num_reviews[1],min_num_reviews[1])
        bar_safety_values[i] = bar1_obj_child2.get_safety_value()

        #Amenities [child] object
        bar1_obj_child3 = bar1_obj.amenities()

    #Bar_object_one = B("",0,0)
    empty_dict = {}
    bar_list = [B.Bar("",0,0,0,empty_dict,empty_dict)] * len(bar_dict['businesses'])

    for j in range(last_index+1):
            bar_list[j] = B.Bar(bar_names[j],j,bar_coolness_values[j],bar_safety_values[j],empty_dict,empty_dict)   #create bar objects and store into list


    if (more_constraints == False):                                                       #user does not want to enter more constraints
        print("\n")
        for k in range(len(bar_list)):                                                    #run thru bar_list
            print("Bar {0}: {1}".format(k+1,bar_list[k].get_name()))                      #print bar # & name
        return                                                                            #terminate progrm
    
    #sorting the list by coolness and safety values
    bars_sorted_by_coolness = sorted(bar_list,key = lambda x: x.coolness,reverse=True)
    bars_sorted_by_safety = sorted(bar_list,key = lambda x: x.safety,reverse=True)

    #only adding amneities to 5 most likely bars for 
    if Priority == "Safety" or Priority == "safety":            
        for k in range(len(bar_list)):
            Amenities = scrape.html_grab(bar_dict['businesses'][k]['url'])
            bars_sorted_by_safety[k].set_Amenities_dict(Amenities)                          #add amenities to dict
            bars_sorted_by_safety[k].set_user_inputs(user_inputs)                           #add defined inputs
            bars_sorted_by_safety[k].set_coolness(bars_sorted_by_safety[k].get_coolness())    #update coolness
            bars_sorted_by_safety[k].set_safety(bars_sorted_by_safety[k].get_safety())        #update safety

    else:
        for k in range(len(bar_list)):
            Amenities = scrape.html_grab(bar_dict['businesses'][k]['url'])
            bars_sorted_by_coolness[k].set_Amenities_dict(Amenities)
            bars_sorted_by_coolness[k].set_user_inputs(user_inputs)                           #add defined inputs
            bars_sorted_by_coolness[k].set_coolness(bars_sorted_by_coolness[k].get_coolness())
            bars_sorted_by_coolness[k].set_safety(bars_sorted_by_coolness[k].get_coolness())

    #sorting the list with the new coolness and safety values
    bars_sorted_by_coolness = sorted(bars_sorted_by_coolness,key = lambda x: x.coolness,reverse=True)
    bars_sorted_by_safety = sorted(bars_sorted_by_safety,key = lambda x: x.safety,reverse=True)

    #call next method - print bars
    print_bars(Priority,bar_list,bars_sorted_by_coolness,bars_sorted_by_safety,bar_dict)





#This method prints all bar data - including recommendations, relevant data and list of sorted bars is desired by use
#specific format of print statements and data printed is dependent upon defined inputs
def print_bars(Priority,bar_list,bars_sorted_by_coolness,bars_sorted_by_safety,bar_dict):
    #prints out recommendation for bar 

    if (Priority == "safety" or Priority == "Safety"):                                  #if priority = safety
        print("Recommended Bar: ",bars_sorted_by_safety[0].get_name())
        index = bars_sorted_by_safety[0].get_index()
        print("   Safety Value: ",bars_sorted_by_safety[0].get_safety(), "  -> Masks are required" if bars_sorted_by_coolness[0].get_Amenities_dict()['Masks_required'] == True else "")
        print("   Coolness Value: ",bars_sorted_by_coolness[0].get_coolness())
        print("   Amenities included:")
        print("      Pool Table" if bars_sorted_by_coolness[0].get_Amenities_dict()['Pool_table'] == True else "")
        print("      Outside Seating" if bars_sorted_by_coolness[0].get_Amenities_dict()['Pool_table'] == True else "")
        print("      Full bar" if bars_sorted_by_coolness[0].get_Amenities_dict()['Full_bar'] == True else "")
        print("      Wheelchair accessible" if bars_sorted_by_coolness[0].get_Amenities_dict()['Wheelchair_access'] == True else "")
        print("      Free Wi-Fi" if bars_sorted_by_coolness[0].get_Amenities_dict()['Free_wifi'] == True else "")


    elif (Priority == "coolness" or Priority == "Coolness"):                           #program assumes priority=coolness
        print("Recommended Bar: ",bars_sorted_by_coolness[0].get_name())
        index = bars_sorted_by_coolness[0].get_index()
        print("   Coolness Value: ",bars_sorted_by_coolness[0].get_coolness())
        print("   Safety Value: ",bars_sorted_by_safety[0].get_safety(),"  -> Masks are required" if bars_sorted_by_coolness[0].get_Amenities_dict()['Masks_required'] == True else "")
        print("   Amenities included:")
        print("      Pool Table" if bars_sorted_by_safety[0].get_Amenities_dict()['Pool_table'] == True else "")
        print("      Outside Seating" if bars_sorted_by_safety[0].get_Amenities_dict()['Pool_table'] == True else "")
        print("      Full bar" if bars_sorted_by_safety[0].get_Amenities_dict()['Full_bar'] == True else "")
        print("      Wheelchair accessible" if bars_sorted_by_safety[0].get_Amenities_dict()['Wheelchair_access'] == True else "")
        print("      Free Wi-Fi" if bars_sorted_by_safety[0].get_Amenities_dict()['Free_wifi'] == True else "")

    else:
        print("Priority of coolness or safety was not entered - system shall prioritize coolness")
        print("Recommended Bar: ",bars_sorted_by_coolness[0].get_name())
        index = bars_sorted_by_coolness[0].get_index()
        print("   Coolness Value: ",bars_sorted_by_coolness[0].get_coolness())
        print("   Safety Value: ",bars_sorted_by_safety[0].get_safety(),"  -> Masks are required" if bars_sorted_by_coolness[0].get_Amenities_dict()['Masks_required'] == True else "")
        print("   Amenities included:")
        print("      Pool Table" if bars_sorted_by_coolness[0].get_Amenities_dict()['Pool_table'] == True else "")
        print("      Outside Seating" if bars_sorted_by_coolness[0].get_Amenities_dict()['Pool_table'] == True else "")
        print("      Full bar" if bars_sorted_by_coolness[0].get_Amenities_dict()['Full_bar'] == True else "")
        print("      Wheelchair accessible" if bars_sorted_by_coolness[0].get_Amenities_dict()['Wheelchair_access'] == True else "")
        print("      Free Wi-Fi" if bars_sorted_by_coolness[0].get_Amenities_dict()['Free_wifi'] == True else "")


#prints out relevant attributes for given bar recommendation
    print("   Is_Closed?: ",bar_dict['businesses'][index]['is_closed'])
    print("   Phone Number: ",bar_dict['businesses'][index]['display_phone'])
    print("   Address: ",bar_dict['businesses'][index]['location']['display_address'])
    print("   City: ",bar_dict['businesses'][index]['location']['city'])
    print("   State: ",bar_dict['businesses'][index]['location']['state'])
    print("   Price: ",bar_dict['businesses'][index]['price'])
    print("   Average Rating: ",bar_dict['businesses'][index]['rating'])


    #print_sorted_list = input("Would you like to see a list of bars sorted by {0}? Enter 'Yes' or 'No'\n>>>".format(Priority))
    #if print_sorted_list == "No": print_sorted_list = False
    
    print_sorted_list = True
#prints sorted list
    if (print_sorted_list):
        for k in range(len(bar_list)):
            print("\n-----------Bar {0}-----------".format(k+1))
            if (Priority == "Safety" or Priority== "safety"):
                print("Name: ",bars_sorted_by_safety[k].get_name())
                print("Safety value: ",bars_sorted_by_safety[k].get_safety())
                #print("   Does the Bar have a Pool Table?: ",bars_sorted_by_coolness[0].get_Amenities_dict()['Pool_table'])
                #print("   Does the Bar offer a outdoor seating?: ",bars_sorted_by_coolness[0].get_Amenities_dict['Outdoor_seating'])

            else:
                print("Name: ",bars_sorted_by_coolness[k].get_name())
                print("Coolness value: ",bars_sorted_by_coolness[k].get_coolness())



def main():
    print("\n---------------------------------------------Start-----------------------------------------------------\n")        
    #collect_constraints_from_user()

if __name__ == "__main__":
    main()