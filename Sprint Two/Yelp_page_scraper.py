import requests

def html_grab(url):
    keyword = "No Pool Table"
    req = requests.get(url)
    #print(keyword in req.text)

#False attributes 
    Pool_table = "No Pool Table" not in req.text
    Outdoor_seating = "No Outdoor Seating" not in req.text
    Wheelchair_access = "Not Wheelchair Accessible" not in req.text
#True attributes
    Free_wifi = "Free Wi-Fi" in req.text
    Full_bar = "Full Bar" in req.text
    Masks_required = "Masks required" in req.text
    Masks_required = "Masks required" in req.text

    print("Gathering Amenities...")

    Amenities_dictionary = {
        "Free_wifi" : Free_wifi,
        "Full_bar" : Full_bar,
        "Masks_required" : Masks_required,
        "Pool_table" : Pool_table,
        "Outdoor_seating" : Outdoor_seating,
        "Wheelchair_access" : Wheelchair_access,
    }

    return Amenities_dictionary


def main():
    print("\nStart")


if __name__ == "__main__":
    main()
