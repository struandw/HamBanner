import pprint
import sys
import time

from pushover import Client

import karelia

ROOM = sys.argv[1]

hambanner = karelia.bot("HamBanner", ROOM)

hambanner.stock_responses["short_help"] = "I respond to spam."
hambanner.stock_responses[
    "long_help"
] = "I respond to spam. Specifically, when users are percieved to sending repeated low-quality messages in a short window, I warn them. Direct criticism to @PouncySilverkitten and the cabal."

hambanner.connect()
message_lengths = {}

minimum_unpenalised_length = 30
warning_threshold = 300
ban_threshold = 400
time_step = 15
dec_multiplier = 0.85

warning_cooldown = 60
ban_cooldown = 300
most_recent_warnings = {}
most_recent_ban_warnings = {}

last_dec_time = time.time()
backoff = 1

while True:
    message = hambanner.parse()
    if message.type == "send-event":
        id = message.data.sender.id
        name = message.data.sender.name
        if id not in message_lengths:
            message_lengths[id] = 0
        message_lengths[id] += minimum_unpenalised_length - len(message.data.content) # Tracks message content; lower is better


        if message_lengths[id] > ban_threshold:
            if id not in most_recent_ban_warnings:
                most_recent_ban_warnings[id] = 0
            if most_recent_ban_warnings[id] < time.time() - ban_cooldown:
                hambanner.reply("Your current posting pattern may cause you to be temporarily banned.")
                Client().send_message(f"@{name} needs a ban.", title="hambanner", url=f"https://euphoria.leet.nu/room/{ROOM}")
                most_recent_ban_warnings[id] = time.time()
                most_recent_warnings[id] = time.time()

        elif message_lengths[id] > warning_threshold:
            if id not in most_recent_warnings:
                most_recent_warnings[id] = 0 # If the user's never been warned, we add them to the dict
            if most_recent_warnings[id] < time.time() - warning_cooldown: # Otherwise, if the cooldown since their last warning has expired...
                hambanner.reply("You're sending lots of short messages. Please consider consolidating them into fewer, longer ones.")
                Client().send_message(f"@{name} may be spamming.", title="hambanner", url=f"https://euphoria.leet.nu/room/{ROOM}")
                message_lengths[id] = warning_threshold # Reset their count; if they stop misbehaving, their score will go down before the cooldown expires.
                most_recent_warnings[id] = time.time()

    if time.time() > last_dec_time + time_step: # Every time_step seconds we move every user score closer to equilibrium
        for user_id in message_lengths:
            message_lengths[user_id] *= dec_multiplier
        last_dec_time = time.time()
