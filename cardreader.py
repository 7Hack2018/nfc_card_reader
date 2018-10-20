#! /usr/bin/env python
import logging
from smartcard.System import readers
import smartcard.Exceptions
import yall

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

# get all the available readers
r = readers()
print("Available readers:", r)

reader = r[0]
print("Using:", reader)

# Keep track of UIDs that we already sent to the backend so we do not spam it with every read cycle
list_known_uids = []

while True:
    try:
        # get a conection to the inserted card if there is any (otherwise the exception will be thrown
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
