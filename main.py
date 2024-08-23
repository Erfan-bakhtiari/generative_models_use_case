from crawler_module import crawl
import requests
import json
from langchain_openai import ChatOpenAI


target_url = "https://klu.ai/llm-leaderboard"
# target_selector = "body > div > div > main > div > div > div:nth-child(1) > div:nth-child(7) > div > div > table"
target_selector = ["body > div > div > main > div > div > div:nth-child(1) > div:nth-child(3) > div.mt-4 > table"
                       ,"body > div > div > main > div > div > div:nth-child(1) > div:nth-child(7) > div > div > table"]
target_labels = ["useCase", "price"]
model_api_key=""
model_base_url=""
model="gpt-4o-mini-2024-07-18"
target_result_container = {}
file_path = 'data.json'

crawl(target_url, target_selector,target_labels, target_result_container)



prompt=f"""
Below are the contents of 2 table elements from an html page that shows data about generative models.
The first table
###
{target_result_container["useCase"]}
###

The second table
###
{target_result_container["price"]}
###

By analyzing the above code, give the json output in the following format
"model": "model name",
"case": "best use case"
, "price":"price (just mention number"
Take the name of all the models from the second table
Take the price data from the second table (just mention the number and don't give a text description)
Take the case data from the first table (if the best use case model was not mentioned in the first table, put the text "unknow")
attention! just back json (not description) So that I can use the output that you give without change in the continuation of the program."""


llm = ChatOpenAI(
    model=model,
    base_url=model_base_url, 
    api_key=model_api_key
)

message_recived=llm.invoke(prompt)
json_data=message_recived.to_json()
json_string = json_data['kwargs']['content']
json_string = json_string.strip('```json')
data = json.loads(json_string)
with open(file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)



# print(message_recived)



# print(json_data)


# with open(file_path, 'w') as json_file:
#     json.dump(json_data, json_file, indent=4)
