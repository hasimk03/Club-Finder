#class will hold a bar object, where each  object contains:
    #The name of the bar
    #A safety value
    #A coolness value
import math
class Bar:
    def __init__(self,bar_name,index,coolness,safety, Amenities_dict, user_inputs):
        self.name = bar_name
        self.index = index
        self.coolness = coolness
        self.safety = safety
        self.Amenities_dict = Amenities_dict
        self.user_inputs = user_inputs

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index

    def get_coolness(self):
        return self.coolness
    
    def set_coolness(self,prev_val):
        #algorithim: 0.6(prev coolness value) + 0.4((Bar_amenities U User_inputs) / 5)

        #determining the intersection of amenities
        intersection_val = 0
        amenities = self.get_Amenities_dict()
        user_in = self.get_user_inputs()

        if (amenities["Free_wifi"] == user_in["Free_wifi"]):   
            intersection_val += 1
        if (amenities["Full_bar"] == user_in["Full_bar"]==True):   
            intersection_val += 1        
        if (amenities["Pool_table"] == user_in["Pool_table"]==True):   
            intersection_val += 1
        if (amenities["Outdoor_seating"] == user_in["Outdoor_seating"]==True):   
            intersection_val += 1
        if (amenities["Wheelchair_access"] == user_in["Wheelchair_access"]):   
            intersection_val += 1

        self.coolness = math.ceil((0.6*prev_val) + (40*(intersection_val/4.5)))                #algorithim = 0.6(prev) + 0.4(intersection/4.44)

    def get_safety(self):
        return self.safety

    def set_safety(self,prev):
        #Algo: 0.65(prev) + 35(if masks)
        amenities = self.get_Amenities_dict()
        user_in = self.get_user_inputs()
        mask = 0

        if (amenities["Masks_required"] == user_in["Masks_required"]):              #masks are required
            mask = 35                                                               #add 35 to safety score

        self.safety = 0.75*prev + mask

    def set_Amenities_dict(self,dictionary):
        self.Amenities_dict = dictionary

    def get_Amenities_dict(self):
        return self.Amenities_dict

    def set_user_inputs(self, in_dict):
        self.user_inputs = in_dict
    
    def get_user_inputs(self):
        return self.user_inputs


def main():
    print("Start")


if __name__ == "__main__":
    main()