from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from utils import places, llm, graph
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

app = FastAPI()

history_sessions = {}
class ChatMessage(BaseModel):
    prompt: str
    session_id: str

@app.post("/chat")
def get_response(request: Request, data: ChatMessage):
    prompt = data.prompt
    if(data.session_id in history_sessions):
        history = history_sessions[data.session_id]
    else:
        history_sessions[data.session_id] = []
        history = []
    cypher_prompt = '''
Given a query about places and distances between them, generate the appropriate Cypher query to retreive a place or a distance relationship between two places in a Neo4j database. 
The relationship is non-directed.

Instructions:
If the user is asking an Itenary retreive all the relationships from the Neo4j database.
If the user is asking for distance and/or time between any two locations then retreive node and the relationship between the locations.
Return only the cypher query and nothing else. No other text or explanation is required. If no cypher query is needed then return FALSE
Always Extract the duration and distance of the relationship.
Always return relevant value in the cypher query.
Always return place variable in the cypher query.
The locations in Neo4j database are {context}
The realtionship is in the following format: Place -> [:DISTANCE] -> Place
Consider the following sample:
(:Place [name: "Charminar, Hyderabad", description: "A historic monument and mosque built in 1591, the Charminar is the most iconic symbol of Hyderabad. It is surrounded by bustling markets, offering a vibrant cultural experience.", location: "Char Kaman, Ghansi Bazaar, Hyderabad, Telangana 500002"])-[:DISTANCE [duration: "36 mins", distance: "11.3 km"]]->(:Place [name: "Golconda Fort, Hyderabad", description: "A massive fort known for its grand architecture and acoustics, Golconda Fort offers a glimpse into the grandeur of the Qutb Shahi dynasty. The fort is also famous for its evening sound and light show.", location: "Khair Complex, Ibrahim Bagh, Hyderabad, Telangana 500008"])
'''
    generate_cipher_template = ChatPromptTemplate.from_messages([
        ("system", cypher_prompt),
        MessagesPlaceholder("history"),
        ("human", "{input}")
    ])
    cypher_response = llm.invoke(generate_cipher_template.format_messages(
        input = prompt,
        history = history,
        context = places
    )).content.strip().strip('```')

    if(cypher_response.startswith("cypher")):
        cypher_response = cypher_response[6:]

    print(cypher_response)
    if(cypher_response == "FALSE"):
        neo4jdata = 'None'
    else:
        neo4jdata = graph.query(cypher_response)

    print(neo4jdata)
    
    general_prompt = '''
Based on the context answer the question of the user.

cypher query: 
{cypher_response}

retreived data:
{neo4jdata}

use the retrived data extracted using the cypher query from Neo4j database to answer the user query.

If there is no retreived data from the Neo4j database indicate that the data is not available.

If the origin and the destination place is same indicate that both the places are the same.
'''
    general_prompt_template = ChatPromptTemplate.from_messages([
        ("system", general_prompt),
        MessagesPlaceholder("history"),
        ("human", "{input}")
    ])
    general_response = llm.invoke(general_prompt_template.format_messages(
        input = prompt,
        history = history,
        cypher_response = cypher_response, 
        neo4jdata = neo4jdata
    )).content.strip()

    history_sessions[data.session_id].append(("human",prompt))
    history_sessions[data.session_id].append(("ai",general_response))
    
    return general_response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)