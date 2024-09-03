from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

#loading the environment variables from .env file
load_dotenv()
GMAPS_API_KEY = os.environ['GMAPS_API_KEY']

# Neo4j database connection
NEO4J_URI = os.environ['NEO4J_URI']
NEO4J_USER = os.environ['NEO4J_USER']
NEO4J_PASSWORD = os.environ['NEO4J_PASSWORD']

MODEL = os.environ['MODEL']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

graph = Neo4jGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

llm = ChatOpenAI(model=MODEL, temperature=0, api_key=OPENAI_API_KEY)

places = [
    "Charminar, Hyderabad",
    "Golconda Fort, Hyderabad",
    "Ramoji Film City, Hyderabad",
    "Birla Mandir, Hyderabad",
    "Hussain Sagar Lake, Hyderabad",
    "Warangal Fort, Warangal",
    "Ramappa Temple, Warangal",
    "Nagarjuna Sagar Dam",
    "Bhadrakali Temple, Warangal",
    "Yadagirigutta Temple, Yadadri",
    "Medak Church, Medak",
    "Kuntala Waterfalls, Adilabad",
    "Ethipothala Waterfalls",
    "Pocharam Wildlife Sanctuary",
    "Kakatiya Zoological Park, Warangal",
    "Bhongir Fort, Bhongir",
    "Surendrapuri, Yadadri",
    "Pakhal Lake, Warangal",
    "Shamirpet Lake, Hyderabad",
    "Qutb Shahi Tombs, Hyderabad",
    "Chilkur Balaji Temple, Hyderabad",
    "Moula Ali Dargah, Hyderabad",
    "Gundala Waterfalls, Bhadradri",
    "Khammam Fort, Khammam",
    "Bogatha Waterfall, Mulugu",
    "Bhadrachalam Temple, Bhadrachalam",
    "Ananthagiri Hills, Vikarabad",
    "Basar Saraswathi Temple, Basar",
    "Mahabubnagar Fort, Mahabubnagar",
    "Koilkonda Fort, Mahabubnagar",
    "Kinnerasani Wildlife Sanctuary, Bhadradri",
    "Eturnagaram Wildlife Sanctuary, Eturnagaram",
    "Srisailam Dam",
    "Sri Lakshmi Narasimha Swamy Temple, Dharmapuri",
    "Kadam Dam, Nirmal",
    "Jagtial Fort, Jagtial",
    "Alampur Jogulamba Temple, Alampur",
    "Osman Sagar Lake (Gandipet Lake), Hyderabad",
    "Nizam Sagar Dam, Nizamabad",
    "Jurala Dam, Mahabubnagar",
    "Chaya Someshwara Temple, Nalgonda",
    "Kolanupaka Jain Temple, Kolanupaka",
    "Ujwala Park, Karimnagar",
    "Sapthagiri Lotus Pond, Karimnagar",
    "Bheemuni Paadam Waterfalls, Warangal",
    "Sathnala Dam, Adilabad",
    "Palair Reservoir, Khammam"
]