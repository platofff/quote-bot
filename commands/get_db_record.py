from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
from db.connect import collection
from typing import Optional
import json
import bson.json_util
bp = Blueprint()

config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/бд <item> <ite>', '/БД <item> <ite>', '/бд <item>', '/БД <item>'], description = 'get db record')

Record = Command()

@bp.on.message(text = Record.hdl())
async def list(m: Message, item: Optional[int] = None, ite: Optional[str] = None):
    data = config_load(config)
    admins = data["admins"]
    if (m.from_id in admins):
        cursor = collection.find({})
        quotes = []
        for i in cursor:
            quotes.append(i)
        try:
            item = int(item)
            if (isinstance(item, int)):
                def parse_json(data):
                    return json.loads(bson.json_util.dumps(data, ensure_ascii=False).encode('utf8'))
                if (ite != None):
                    obj = parse_json(quotes[item][ite])
                else:
                    obj = parse_json(quotes[item])
                a = str(json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False)).replace('    ', 'ᅠ')
                print(str(json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False)))
                await Record.ans_up(a, m)
        except Exception as e:
            await Record.ans_up(e, m)
    
    