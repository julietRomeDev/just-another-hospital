from faker import Faker

fake = Faker('es_AR')
print("*" * 50)
print("Development Purposes - Generating Fake phone numbers and address")
print("*" * 50)
print()

street = fake.street_name()
height = fake.building_number()
city = "Buenos Aires"
province = "Buenos Aires"
ba_address = f"{street}, {height}, {city}, {province}"
name = fake.name()
domain = "justanotherhospital.domain"
corporative_mail = f"{name}@{domain}"
phone = fake.phone_number()

print("DATA")
print(f"direccion: {ba_address}")
print(f"email corporativo: {corporative_mail}")
print(f"ciudad:  {city}")
print(f"provincia:  {province}")
print(f"username:  {name}")
print(f"number:  {phone}")
