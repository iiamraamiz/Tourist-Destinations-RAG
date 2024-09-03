# Tourist-Destinations-RAG

This project is aimed to explore the reterival augmented generation technique for enhancing the accuracy and reliability of generative AI models with facts fetched from external sources. The project utilizes the data of Top-50 tourist destinations in Telagana, India which stored in the graph based Neo4j database in form of nodes and relationships, where the nodes are the places and the relationships containing the parameters such as distance and time. The user's prompt is intially fed to the LLM and a cypher query is generated based on the input, which is then used to query the graph database for retreving the information. The retreived information is again passed to the LLM to generate a accurate response based on the user's prompt and answer the question according to the rules determined by the sytem prompt.

Technologies used: Python, Neo4j Database, OpenAI API, FastAPI
