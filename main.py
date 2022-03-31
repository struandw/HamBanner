import karelia
import sys
import time

hambanner = karelia.bot("Hambanner", "xkcd")

hambanner.stock_responses["short_help"] = "I respond to spam."
hambanner.stock_responses[
    "long_help"
] = "I respond to spam. Specifically, when users are percieved to sending repeated low-quality messages in a short window, I warn. Direct criticism to @PouncySilverkitten and the cabal."

hambanner.connect()
message_lengths = {}

minimum_unpenalised_length = 40
warning_threshold = 100
time_step = 15
dec_multiplier = 0.9

last_dec_time = time.time()

while True:
    try:
        while True:
            message = hambanner.parse()
            if message.type == "send-event":
                if message.data.sender.id not in message_lengths:
                    message_lengths[message.data.sender.id] = 0
                message_lengths[
                    message.data.sender.id
                ] += minimum_unpenalised_length - len(message.data.content)

                if message_lengths[message.data.sender.id] > warning_threshold:
                    hambanner.reply("You're sending spam. Please don't do that.")

            if time.time() > last_dec_time + time_step:
                for user_id in message_lengths:
                    message_lengths[user_id] *= dec_multiplier
                last_dec_time = time.time()

    except SystemExit:
        # Catches !kill commands to the bot and ctrl+c/equivalent
        sys.exit(0)
    finally:
        time.sleep(1)
        hambanner.connect()
