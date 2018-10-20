#! /usr/bin/env python
import logging
from smartcard.System import readers
import smartcard.Exceptions
import yall
import time

logger = logging.getLogger()
sh = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
logger.addHandler(sh)

def _array_to_string(array_of_integers):
    """
    Gives us a nicely formated string instead of an array of bytes which we can then use to update our backend.
    :param array_of_integers:
    :return:
    """
    return ''.join('{:02x}'.format(x) for x in array_of_integers)

# The command we have to send to the NFC card to give us its UID
GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

KNOWN_UID_RESET_INTERVAL = 20  # reset the list of known uids every 20s

# get all the available readers
r = readers()
print("Available readers:", r)

reader = r[0]
print("Using:", reader)

# Keep track of UIDs that we already sent to the backend so we do not spam it with every read cycle
list_known_uids = []

cycle_time = 0  # used to store the loop iterations and will be reset to 0 after KNOWN_UID_RESET_INTERVAL
SLEEP_TIME = 0.1

while True:
    if cycle_time >= KNOWN_UID_RESET_INTERVAL and len(list_known_uids) > 0:
        logger.debug("Reset list of known uids")
        list_known_uids = []
        cycle_time = 0

    try:
        # get a connection to the inserted card if there is any (otherwise the exception will be thrown
        connection = reader.createConnection()
        connection.connect()

    except smartcard.Exceptions.NoCardException:
        # No card...keep waiting
        pass

    else:
        # There is a card so let's ask it for its UID
        data, sw1, sw2 = connection.transmit(GET_UID)

        # get us a nice string out of the ugly byte array
        uid = _array_to_string(data)

        logger.debug("Got uid %s" % uid)
        # Check if we read the card before
        if uid not in list_known_uids:
            logger.info("Adding UID to list of known UIDs")
            list_known_uids.append(uid)  # remember the card so we do not notify again when we see it next time
            try:
                result = yall.update_token(uid)  # Call the backend that the card was inserted
                logger.info("Updated yall api for token %s with result %s" % (uid, result))
            except Exception as exc:
                logger.error("Failed updating yall api for token %s with result %s" % (uid, exc))
        else:
            logger.debug("UID already known")

    time.sleep(SLEEP_TIME)
    cycle_time += SLEEP_TIME
