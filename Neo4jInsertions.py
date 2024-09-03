from neo4j import GraphDatabase
import googlemaps
from dotenv import load_dotenv
import os

#loading the environment variables from .env file
load_dotenv()
GMAPS_API_KEY = os.environ['GMAPS_API_KEY']

# Neo4j database connection
NEO4J_URI = os.environ['NEO4J_URI']
NEO4J_USER = os.environ['NEO4J_USER']
NEO4J_PASSWORD = os.environ['NEO4J_PASSWORD']

# Initialize Google Maps client
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

# List of 50 places with their locations and descriptions
places_info = [
    ("Charminar, Hyderabad", "Char Kaman, Ghansi Bazaar, Hyderabad, Telangana 500002", 
     "A historic monument and mosque built in 1591, the Charminar is the most iconic symbol of Hyderabad. It is surrounded by bustling markets, offering a vibrant cultural experience."),
    
    ("Golconda Fort, Hyderabad", "Khair Complex, Ibrahim Bagh, Hyderabad, Telangana 500008", 
     "A massive fort known for its grand architecture and acoustics, Golconda Fort offers a glimpse into the grandeur of the Qutb Shahi dynasty. The fort is also famous for its evening sound and light show."),
    
    ("Ramoji Film City, Hyderabad", "Anaspur Village, Hayathnagar Mandal, Hyderabad, Telangana 501512", 
     "The world’s largest film city, Ramoji Film City is a popular tourist attraction where visitors can explore movie sets, enjoy theme parks, and experience live shows."),
    
    ("Birla Mandir, Hyderabad", "Naubath Pahad, Khairatabad, Hyderabad, Telangana 500004", 
     "A beautiful temple made of white marble, dedicated to Lord Venkateswara. The temple offers panoramic views of Hyderabad city and is known for its serene ambiance."),
    
    ("Hussain Sagar Lake, Hyderabad", "Tank Bund Road, Hyderabad, Telangana 500004", 
     "A large man-made lake with a giant Buddha statue in the center, Hussain Sagar is a popular spot for boating and enjoying the city’s skyline, especially at sunset."),
    
    ("Warangal Fort, Warangal", "Warangal Fort Road, Warangal, Telangana 506002", 
     "A historic fort built by the Kakatiya dynasty, known for its grand stone gates and intricate carvings. It offers insights into the architectural brilliance of medieval South India."),
    
    ("Ramappa Temple, Warangal", "Palampet, Mulugu, Telangana 506345", 
     "A UNESCO World Heritage Site, the Ramappa Temple is known for its exquisite architecture and detailed stone carvings. It was built in the 13th century and is dedicated to Lord Shiva."),
    
    ("Nagarjuna Sagar Dam", "Nagarjuna Sagar, Telangana 508202", 
     "One of the largest dams in India, Nagarjuna Sagar Dam is built on the Krishna River and is a popular spot for picnics and boat rides. It is surrounded by lush greenery and offers scenic views."),
    
    ("Bhadrakali Temple, Warangal", "Near Hanamkonda, Warangal, Telangana 506001", 
     "Dedicated to Goddess Bhadrakali, this temple is one of the oldest and most significant in the region. It is located near a large lake and offers a peaceful atmosphere for devotees."),
    
    ("Yadagirigutta Temple, Yadadri", "Yadagirigutta, Yadadri Bhuvanagiri District, Telangana 508115", 
     "A famous temple dedicated to Lord Lakshmi Narasimha, Yadagirigutta is located on a hilltop and attracts thousands of devotees every day. The temple offers panoramic views of the surrounding area."),
    
    ("Medak Church, Medak", "Medak Town, Telangana 502110", 
     "The Medak Cathedral is one of the largest churches in Asia, known for its Gothic architecture and stunning stained glass windows. It is a prominent landmark in Medak."),
    
    ("Kuntala Waterfalls, Adilabad", "Neredigonda Mandal, Adilabad, Telangana 504308", 
     "The highest waterfall in Telangana, Kuntala Waterfalls is a beautiful spot surrounded by forests. It is a popular destination for nature lovers and adventure enthusiasts."),
    
    ("Ethipothala Waterfalls", "Near Nagarjuna Sagar, Telangana 508202", 
     "A stunning waterfall located on the Chandravanka River, Ethipothala Waterfalls is a popular spot for picnics and photography. The surrounding area is lush and green, offering a refreshing atmosphere."),
    
    ("Pocharam Wildlife Sanctuary", "Medak District, Telangana 502277", 
     "A wildlife sanctuary located near Medak, Pocharam is home to a variety of animals, including deer, wild boar, and migratory birds. It is an ideal spot for nature walks and bird watching."),
    
    ("Kakatiya Zoological Park, Warangal", "Enumamula Road, Warangal, Telangana 506002", 
     "A zoological park in Warangal that houses various species of animals, birds, and reptiles. It is a great spot for families and children to learn about wildlife."),
    
    ("Bhongir Fort, Bhongir", "Bhongir, Telangana 508116", 
     "A massive rock fort built on a monolithic rock, Bhongir Fort offers stunning views of the surrounding countryside and is a popular spot for trekking."),
    
    ("Surendrapuri, Yadadri", "Near Yadagirigutta, Telangana 508115", 
     "A mythological awareness center and theme park, Surendrapuri is known for its replicas of various Hindu temples and mythological scenes."),
    
    ("Pakhal Lake, Warangal", "Pakhal, Warangal, Telangana 506381", 
     "A beautiful man-made lake surrounded by lush forests, Pakhal Lake is a great spot for picnics and nature walks. The area is also home to a wildlife sanctuary."),
    
    ("Shamirpet Lake, Hyderabad", "Shamirpet, Telangana 500078", 
     "A serene lake located near Hyderabad, Shamirpet Lake is a popular spot for picnics, boating, and bird watching."),
    
    ("Qutb Shahi Tombs, Hyderabad", "Ibrahim Bagh, Hyderabad, Telangana 500008", 
     "The tombs of the Qutb Shahi rulers, these monuments are an architectural marvel, blending Persian, Pathan, and Hindu styles. They are set in a beautifully landscaped garden."),
    
    ("Chilkur Balaji Temple, Hyderabad", "Chilkur, Hyderabad, Telangana 500075", 
     "Also known as the 'Visa Balaji Temple', this temple is popular among devotees seeking visas for overseas travel. It is one of the few temples in India that does not accept any money or donations."),
    
    ("Moula Ali Dargah, Hyderabad", "Moula Ali, Hyderabad, Telangana 500040", 
     "A prominent Islamic pilgrimage site located on a hillock, offering panoramic views of Hyderabad. The dargah is dedicated to Hazrat Ali, the son-in-law of Prophet Muhammad."),
    
    ("Gundala Waterfalls, Bhadradri", "Gundala, Bhadradri Kothagudem District, Telangana 507101", 
     "A picturesque waterfall located amidst dense forests, Gundala Waterfalls is a serene spot perfect for nature lovers and picnickers."),
    
    ("Khammam Fort, Khammam", "Khammam, Telangana 507001", 
     "A historic fort built during the Kakatiya dynasty, Khammam Fort is known for its architectural grandeur and offers a panoramic view of the surrounding area."),
    
    ("Bogatha Waterfall, Mulugu", "Cheekupally, Wazeedu Mandal, Mulugu, Telangana 506343", 
     "Often referred to as the 'Niagara of Telangana', Bogatha Waterfall is a stunning natural attraction surrounded by greenery. It is a great spot for picnics and photography."),
    
    ("Bhadrachalam Temple, Bhadrachalam", "Bhadrachalam, Bhadradri Kothagudem District, Telangana 507111", 
     "A famous temple dedicated to Lord Rama, Bhadrachalam is a significant pilgrimage site, especially during the festival of Sri Rama Navami."),
    
    ("Ananthagiri Hills, Vikarabad", "Ananthagiri, Vikarabad, Telangana 501102", 
     "A popular hill station near Hyderabad, Ananthagiri Hills is known for its scenic beauty, coffee plantations, and trekking trails."),
    
    ("Basar Saraswathi Temple, Basar", "Basar, Nirmal District, Telangana 504101", 
     "One of the two famous temples dedicated to Goddess Saraswathi in India, Basar Temple is a prominent pilgrimage site and is known for the ritual of 'Aksharabhyasam' (initiation of education)."),
    
    ("Mahabubnagar Fort, Mahabubnagar", "Mahabubnagar, Telangana 509001", 
     "A historic fort that dates back to the 14th century, Mahabubnagar Fort is known for its ancient architecture and offers a glimpse into the region's history."),
    
    ("Koilkonda Fort, Mahabubnagar", "Koilkonda, Mahabubnagar District, Telangana 509371", 
     "A hill fort with stunning views of the surrounding landscape, Koilkonda Fort is a popular spot for trekking and history enthusiasts."),
    
    ("Kinnerasani Wildlife Sanctuary, Bhadradri", "Kinnerasani, Bhadradri Kothagudem District, Telangana 507113", 
     "A wildlife sanctuary located on the banks of the Kinnerasani River, it is home to a variety of wildlife, including tigers, leopards, and various bird species."),
    
    ("Eturnagaram Wildlife Sanctuary, Eturnagaram", "Eturnagaram, Mulugu District, Telangana 506165", 
     "One of the oldest wildlife sanctuaries in Telangana, Eturnagaram is known for its rich biodiversity, including elephants, deer, and various bird species."),
    
    ("Srisailam Dam", "Srisailam, Telangana 508202", 
     "A major dam built on the Krishna River, Srisailam Dam is one of the largest dams in India and a popular spot for boating and enjoying the scenic views."),
    
    ("Sri Lakshmi Narasimha Swamy Temple, Dharmapuri", "Dharmapuri, Jagtial District, Telangana 505425", 
     "An ancient temple dedicated to Lord Narasimha, this temple is known for its religious significance and attracts devotees from across the state."),
    
    ("Kadam Dam, Nirmal", "Kadam, Nirmal District, Telangana 504310", 
     "A major dam located on the Kadem River, Kadam Dam is surrounded by lush greenery and is a popular spot for picnics and nature walks."),
    
    ("Jagtial Fort, Jagtial", "Jagtial, Telangana 505327", 
     "A unique star-shaped fort built during the Mughal era, Jagtial Fort is known for its architectural brilliance and historical significance."),
    
    ("Alampur Jogulamba Temple, Alampur", "Alampur, Jogulamba Gadwal District, Telangana 509152", 
     "One of the 18 Maha Shakti Peethas, Alampur Jogulamba Temple is a significant pilgrimage site dedicated to Goddess Jogulamba."),
    
    ("Osman Sagar Lake (Gandipet Lake), Hyderabad", "Gandipet, Hyderabad, Telangana 500075", 
     "A large reservoir that serves as a major water source for Hyderabad, Osman Sagar Lake is a popular spot for picnics and boating."),
    
    ("Nizam Sagar Dam, Nizamabad", "Nizam Sagar, Nizamabad District, Telangana 503302", 
     "A large dam built across the Manjira River, Nizam Sagar Dam is a popular spot for picnics and enjoying scenic views."),
    
    ("Jurala Dam, Mahabubnagar", "Jurala, Mahabubnagar District, Telangana 509102", 
     "A major dam built on the Krishna River, Jurala Dam is a popular spot for picnics and enjoying the surrounding natural beauty."),
    
    ("Chaya Someshwara Temple, Nalgonda", "Panagal, Nalgonda District, Telangana 508004", 
     "An ancient temple known for the mysterious shadow that falls on the deity's idol at all times of the day, Chaya Someshwara Temple is a unique architectural marvel."),
    
    ("Kolanupaka Jain Temple, Kolanupaka", "Kolanupaka, Yadadri Bhuvanagiri District, Telangana 508101", 
     "A historic Jain temple known for its ancient architecture and beautiful sculptures, Kolanupaka Jain Temple is a significant pilgrimage site for the Jain community."),
    
    ("Ujwala Park, Karimnagar", "Karimnagar, Telangana 505001", 
     "A beautiful park located in Karimnagar, Ujwala Park is a popular spot for families and children, offering a peaceful environment for relaxation."),
    
    ("Sapthagiri Lotus Pond, Karimnagar", "Karimnagar, Telangana 505001", 
     "A scenic pond surrounded by greenery, Sapthagiri Lotus Pond is a popular spot for nature lovers and photographers."),
    
    ("Bheemuni Paadam Waterfalls, Warangal", "Bheemuni Paadam, Warangal, Telangana 506348", 
     "A stunning waterfall that flows through a rock resembling a giant foot, Bheemuni Paadam Waterfalls is a popular spot for picnics and enjoying the natural beauty."),
    
    ("Sathnala Dam, Adilabad", "Sathnala, Adilabad District, Telangana 504105", 
     "A major dam located on the Sathnala River, Sathnala Dam is a popular spot for picnics and enjoying the surrounding natural beauty."),
    
    ("Palair Reservoir, Khammam", "Palair, Khammam District, Telangana 507157", 
     "A large reservoir located near Khammam, Palair Reservoir is a popular spot for boating and enjoying the scenic views.")
]

# Initialize Neo4j driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def insert_place(tx, name, location, description):
    tx.run("MERGE (p:Place {name: $name, location: $location, description: $description})",
           name=name, location=location, description=description)

def insert_distance(tx, place1, place2, distance, duration):
    tx.run("MATCH (p1:Place {name: $place1}), (p2:Place {name: $place2}) "
           "MERGE (p1)-[:DISTANCE {distance: $distance, duration: $duration}]->(p2)",
           place1=place1, place2=place2, distance=distance, duration=duration)

def calculate_and_insert_distances():
    with driver.session() as session:
        # Insert all places into Neo4j
        for place, location, description in places_info:
            session.write_transaction(insert_place, place, location, description)

        # Calculate and insert distances between each pair of places
        for i in range(len(places_info)):
            for j in range(i + 1, len(places_info)):
                origin_name, origin_location, _ = places_info[i]
                dest_name, dest_location, _ = places_info[j]

                result = gmaps.distance_matrix(origins=origin_location, destinations=dest_location, mode="driving")

                if result['rows'][0]['elements'][0]['status'] == 'OK':
                    distance = result['rows'][0]['elements'][0]['distance']['text']
                    duration = result['rows'][0]['elements'][0]['duration']['text']

                    session.write_transaction(insert_distance, origin_name, dest_name, distance, duration)

if __name__ == "__main__":
    calculate_and_insert_distances()
    driver.close()