import karelia
import sys
import time
import pprint

hambanner = karelia.bot("HamBanner", "xkcd")

hambanner.stock_responses["short_help"] = "I respond to spam."
hambanner.stock_responses[
    "long_help"
] = "I respond to spam. Specifically, when users are percieved to sending repeated low-quality messages in a short window, I warn. Direct criticism to @PouncySilverkitten and the cabal."

hambanner.connect()
message_lengths = {}

minimum_unpenalised_length = 30
warning_threshold = 300
time_step = 15
dec_multiplier = 0.85

warning_cooldown = 120
most_recent_warnings = {}

last_dec_time = time.time()
backoff = 1

while True:
    try:
        while True:
            backoff = 1 
            message = hambanner.parse()
            if message.type == "send-event":
                if message.data.sender.id not in message_lengths:
                    message_lengths[message.data.sender.id] = 0
                message_lengths[
                    message.data.sender.id
                ] += minimum_unpenalised_length - len(message.data.content)

                if message_lengths[message.data.sender.id] > warning_threshold:
                    if message.data.sender.id not in most_recent_warnings:
                        most_recent_warnings[message.data.sender.id] = 0
                    if most_recent_warnings[message.data.sender.id] < time.time() - warning_cooldown:
                        hambanner.reply("You're sending lots of short messages. Please consider consolidating them into fewer, longer ones.")
                        message_lengths[user_id] = warning_threshold
                        most_recent_warnings[message.data.sender.id] = time.time()
                        with open('count.txt', 'r') as f:
                            count = int(f.read())
                        with open('count.txt', 'w') as f:
                            f.write(str(count + 1))

            if time.time() > last_dec_time + time_step:
                for user_id in message_lengths:
                    message_lengths[user_id] *= dec_multiplier
                last_dec_time = time.time()
    except SystemExit:
        sys.exit(0)
    finally:
        hambanner.logger.log(3, "")
        time.sleep(backoff)
        hambanner.connect()
        backoff *= 2
