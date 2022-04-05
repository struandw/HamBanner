import karelia
import sys
import time
import pprint

hambanner = karelia.bot("HamBannerTweaker", "test")

hambanner.stock_responses["short_help"] = "I respond to spam."
hambanner.stock_responses[
    "long_help"
] = "I respond to spam. Specifically, when users are percieved to sending repeated low-quality messages in a short window, I warn. Direct criticism to @PouncySilverkitten and the cabal."

hambanner.connect()
message_lengths = {}

minimum_unpenalised_length = 30
warning_threshold = 400
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

            if time.time() > last_dec_time + time_step:
                for user_id in message_lengths:
                    message_lengths[user_id] *= dec_multiplier
                last_dec_time = time.time()

            
            if message.type == "send-event":
                if message.data.content.startswith('!minlength '):
                    try:
                        minimum_unpenalised_length = int(message.data.content.split()[1])
                        hambanner.reply(f"Minimum length set to {minimum_unpenalised_length}")
                    except:
                        hambanner.reply("Invalid minimum length.")
                if message.data.content.startswith('!threshold '):
                    try:
                        warning_threshold = int(message.data.content.split()[1])
                        hambanner.reply(f"Threshold set to {warning_threshold}")
                    except:
                        hambanner.reply("Invalid threshold.")
                if message.data.content.startswith('!time '):
                    try:
                        time_step = int(message.data.content.split()[1])
                        hambanner.reply(f"Time step set to {time_step}")
                    except:
                        hambanner.reply("Invalid time step.")
                if message.data.content.startswith('!dec_multiplier '):
                    try:
                        dec_multiplier = float(message.data.content.split()[1])
                        hambanner.reply(f"Decay multiplier set to {dec_multiplier}")
                    except:
                        hambanner.reply("Invalid dec_multiplier.")
                if message.data.content.startswith('!cooldown '):
                    try:
                        warning_cooldown = int(message.data.content.split()[1])
                        hambanner.reply(f"Cooldown set to {warning_cooldown}")
                    except:
                        hambanner.reply("Invalid cooldown.")
                if message.data.content == "!tabularasa":
                    message_lengths = {}
                    hambanner.reply("Slate cleaned.")
                if message.data.content == '!params':
                    hambanner.reply(f"minimum_unpenalised_length = {minimum_unpenalised_length}\nwarning_threshold = {warning_threshold}\ntime_step = {time_step}\ndec_multiplier = {dec_multiplier}\nwarning_cooldown = {warning_cooldown}")

    finally:
        time.sleep(backoff)
        hambanner.connect()
        backoff *= 2
