#system works with Yelp API and user 
    #use cmd line inputs as constraints for search business feature in Yelp API
    #System main function:
        #create objects to store each business result 
            #create attributes for each business object

    #system terminates with N results, where each result contains a set of relevant attributes (reviews,address,ect..)

    #Second system will store this data into specific classes/objects following a defined heirarchy
        #sub-system/third system ranks and organizes list by most similar to user requirements

import requests
import json
import YelpHelp
import Bar_instance as B
#import YelpHelp

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

    
    bar_name_list = [""] * len(bar_dict['businesses'])                          #intialize list of bars

    for i in range(len(bar_dict['businesses'])):                                #run thru bar dict
        bar_name_list[i] = bar_dict['businesses'][i]['name']                        #store bar names in bar_name_list

        #delete certain keys for each business listed
        del bar_dict['businesses'][i]['alias']
        del bar_dict['businesses'][i]['image_url']
        del bar_dict['businesses'][i]['coordinates']
        del bar_dict['businesses'][i]['location']['address1']
        del bar_dict['businesses'][i]['location']['address2']
        del bar_dict['businesses'][i]['location']['address3']

        #add party key for each business
        bar_dict['businesses'][i]['party_scene'] = False
        #bar_dict['businesses'][i]['party_scene'] = True

    #print(json.dumps(bar_dict,indent=2))

    return bar_dict


def main():
    print("\n---------------------------------------------Start-----------------------------------------------------\n")
    #inputs = city,search radius, coolness or safety
        #later inputs = amenities,safety regulations,business requirements

    loc = input("Where do you want to go clubbing? Enter your response in the following format: City,State\n>>>")   #desired location
    rad = input("Enter search radius for {0} in meters (mile =~ 1610 meters) \n  >".format(loc))                                          #search radius(mi->m)
    #rad = rad * 1610
    Priority = input("Which is more importance to you when choosing a bar to visit, safety or coolness?\n>>>")

    #loc = "New Brunswick, New Jersey"
    #rad = 1610
    #Priority = "Coolness"

    bar_dict = access_API(loc,rad)

#create bar object for 1st bar in dict -> destination dogs
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
    bar_list = [B.Bar("",0,0,0)] * len(bar_dict['businesses'])

    for j in range(last_index+1):
        bar_list[j] = B.Bar(bar_names[j],j,bar_coolness_values[j],bar_safety_values[j])   #create bar objects and store into list

    #sorting the list by coolness and safety values
    bars_sorted_by_coolness = sorted(bar_list,key = lambda x: x.coolness,reverse=True)
    bars_sorted_by_safety = sorted(bar_list,key = lambda x: x.safety,reverse=True)

#prints out recommendation for bar 
    if (Priority == "safety" or Priority == "Safety"):
        print("Recommended Bar: ",bars_sorted_by_safety[0].get_name())
        index = bars_sorted_by_safety[0].get_index()
        print("   Safety Value: ",bars_sorted_by_safety[0].get_safety())
        print("   Coolness Value: ",bars_sorted_by_coolness[0].get_coolness())


    elif (Priority == "coolness" or Priority == "Coolness"):
        print("Recommended Bar: ",bars_sorted_by_coolness[0].get_name())
        index = bars_sorted_by_coolness[0].get_index()
        print("   Coolness Value: ",bars_sorted_by_coolness[0].get_coolness())
        print("   Safety Value: ",bars_sorted_by_safety[0].get_safety())

#prints out relevant attributes for given bar recommendation
    print("   Is_Closed?: ",bar_dict['businesses'][index]['is_closed'])
    print("   Phone Number: ",bar_dict['businesses'][index]['display_phone'])
    print("   Address: ",bar_dict['businesses'][index]['location']['display_address'])
    print("   City: ",bar_dict['businesses'][index]['location']['city'])
    print("   State: ",bar_dict['businesses'][index]['location']['state'])
    print("   Price: ",bar_dict['businesses'][index]['price'])
    print("   Average Rating: ",bar_dict['businesses'][index]['rating'])


    print_sorted_list = input("Would you like to see a list of bars sorted by {0}? Enter 'Yes' or 'No'\n>>>".format(Priority))
    if print_sorted_list == "No": print_sorted_list = False

#prints sorted list
    if (print_sorted_list):
        for k in range(len(bar_list)):
            print("\n-----------Bar {0}-----------".format(k+1))
            if (Priority == "Safety" or Priority== "safety"):
                print("Name: ",bars_sorted_by_safety[k].get_name())
                print("Safety value: ",bars_sorted_by_safety[k].get_safety())
            else:
                print("Name: ",bars_sorted_by_coolness[k].get_name())
                print("Coolness value: ",bars_sorted_by_coolness[k].get_coolness())



if __name__ == "__main__":
    main()