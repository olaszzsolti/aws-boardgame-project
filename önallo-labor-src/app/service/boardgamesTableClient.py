import boto3
import json
import logging
from collections import defaultdict

# létrehozza DynamoDB client-et boto3 segítségével.
client = boto3.client('dynamodb')

def getAllBoardgames():

    # az összes Boardgames megkapjuk DynamoDB-ből
    response = client.scan(
        TableName='BoardgamesTable'
    )

    logging.info(response["Items"])

 
    # végigpörgeti a visszaadott boargameket, és hozzáadja azok attribútumait egy új dicthez,
    # amely megfelel a frontend által várt JSON-válaszszerkezetnek.
    boardgamesList = defaultdict(list)
    for item in response["Items"]:
        boardgame = {}
        boardgame["boardgamesId"] = item["BoardgamesId"]["S"]
        boardgame["name"] = item["Name"]["S"]
        boardgame["childadult"] = item["ChildAdult"]["S"]
        boardgame["gamelength"] = item["GameLength"]["S"]
        boardgame["type"] = item["Type"]["S"]
        boardgame["thumbImageUri"] = item["ThumbImageUri"]["S"]
        boardgameList["boardgames"].append(boardgame)

    # convertálja a listát JSON-ba
    return json.dumps(boardgameList)

def queryBoardgames(queryParam):

    logging.info(json.dumps(queryParam))

    # Használja a DynamoDB API-lekérdezést a kiválasztott szűrőértékekkel megegyező
    # boardgamesek lekéréséhez a táblából.
    response = client.query(
        TableName='BoardgamesTable',
        IndexName=queryParam['filter']+'Index',
        KeyConditions={
            queryParam['filter']: {
                'AttributeValueList': [
                    {
                        'S': queryParam['value']
                    }
                ],
                'ComparisonOperator': "EQ"
            }
        }
    )

    boardgameList = defaultdict(list)
    for item in response["Items"]:
        boardgame = {}
        boardgame["boardgamesId"] = item["BoardgamesId"]["S"]
        boardgame["name"] = item["Name"]["S"]
        boardgame["childadult"] = item["ChildAdult"]["S"]
        boardgame["gamelength"] = item["GameLength"]["S"]
        boardgame["type"] = item["Type"]["S"]
        boardgame["thumbImageUri"] = item["ThumbImageUri"]["S"]
        boardgameList["boardgames"].append(boardgame)

    return json.dumps(boardgameList)

# Egyedi boardgamesId nek megfelelő boardgame-t adja vissza
def getBoardgame(boardgamesId):

 
    # DynamoDB API GetItem függvényét használja,
    # mely egy itemet ad vissza a táblából
    response = client.get_item(
        TableName='BoardgamesTable',
        Key={
            'BoardgamesId': {
                'S': boardgamesId
            }
        }
    )

    item = response["Item"]

    boardgame = {}
    boardgame["boardgamesId"] = item["BoardgamesId"]["S"]
    boardgame["name"] = item["Name"]["S"]
    boardgame["year"] = int(item["Year"]["N"])
    boardgame["childadult"] = item["ChildAdult"]["S"]
    boardgame["gamelength"] = item["GameLength"]["S"]   
    boardgame["type"] = item["Type"]["S"]
    boardgame["description"] = item["Description"]["S"]
    boardgame["thumbImageUri"] = item["ThumbImageUri"]["S"]
    boardgame["profileImageUri"] = item["ProfileImageUri"]["S"]
    boardgame["likes"] = item["Likes"]["N"]

    return json.dumps(boardgame)


# növeli a like értékélt 1-el
def likeBoardgame(boardgamesId):

   
    # DynamoDb API UpdateItem függvényt használja, a like számláló növeléséhez.
    response = client.update_item(
        TableName='BoardgamesTable',
        Key={
            'BoardgamesId': {
                'S': boardgamesId
            }
        },
        UpdateExpression="SET Likes = Likes + :n",
        ExpressionAttributeValues={':n': {'N': '1'}}
    )

    response = {}
    response["Update"] = "Success";

    return json.dumps(response)
