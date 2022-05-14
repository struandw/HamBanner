import karelia
import pprint


blorbo = karelia.bot("Present", "xkcd")

blorbo.stock_responses["short_help"] = "eeby deeby"
blorbo.stock_responses[
    "long_help"
] = "blorbo from my shows"

blorbo.connect()
present = {}

while True:
    message = blorbo.parse()
    try:
        if not message.data.sender.id.startswith("bot:"):
            if message.type == "join-event":
                print(message.data.name + " joined")
                present[message.data.name] = True
            elif message.type == "part-event":
                print(message.data.name + " left")
                present[message.data.name] = False
            elif message.type == "send-event":
                present[message.data.sender.name] = True
                if message.data.content.lower == "!present":
                    present_list = []
                    for user in present:
                        if present[user]:
                            present_list.append(user)
                    blorbo.reply("\n".join(sorted(present_list)))
            elif message.type == "nick-event":
                present[message.packet["data"]["from"]] = False
                present[message.data.to] = True
    except AttributeError:
        pass