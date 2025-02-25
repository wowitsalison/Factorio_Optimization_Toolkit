from bs4 import BeautifulSoup
import requests
import os

# Link to the rocket silo factorio wiki page
origin_link = "https://wiki.factorio.com/Rocket_silo"

# Include a User-Agent header to identify the client
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36" }

# Initialize material dictionary to add materials to
materials = {
    "Rocket silo" : 1
}

material_cache = {}

# Function to convert quantity string to int
def convert_quantity(quantity):
    if not quantity:
        return 0  # Return 0 if the quantity is empty or invalid
    # If k is in the quantity, multiply by 1000
    if 'k' in quantity:
        return int(quantity.replace('k', '')) * 1000
    try:
        # Try to convert the quantity directly to an integer
        return int(quantity)
    except ValueError:
        # If conversion fails, return 0 or handle accordingly
        return 0

def get_materials(material_link, headers):
    # Fetch the wiki page
    wiki_response = requests.get(material_link, headers=headers)
    try: 
        wiki_soup = BeautifulSoup(wiki_response.text, 'html.parser')
        # Find materials section
        material_links = wiki_soup.find('td', class_='infobox-vrow-value')
        # Get links from materials section
        material_links = material_links.find_all('a', href=True, title=True)

        # Get material name, link, and quantity 
        for material in material_links[1:-1]:   # Skip first and last- time and current material
            title = material['title']
            material_url = "https://wiki.factorio.com" + material['href']
            quantity = material.find_next('div', class_='factorio-icon-text').text.strip()
            quantity = convert_quantity(quantity)

            # Check if material is already in dictionary
            if title in materials:
                # If it is, increase the quantity
                materials[title] += quantity
            else:
                # If it's not, add it
                materials[title] = quantity

            #print(f"Material: {title}, Link: {material_url}, Quantity: {quantity}")

            get_materials(material_url, headers)

    except Exception as e:
        print(f"Error fetching wiki page: {e}")

if __name__ == "__main__":
    get_materials(origin_link, headers)
    print(materials)