import phonenumbers as pn
from phonenumbers import geocoder

phone1 = pn.parse('+393343143916')

print('Phone number location\n')
print(geocoder.description_for_number(phone1,'en'))