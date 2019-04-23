import zlib


def decode(frame=None):
    if frame is None:
        file1 = open("frame1", "r")
        lines = file1.readlines()
        frame = ""
        for line in lines:
            frame = frame + line.rstrip()
        file1.close()
    # print(frame)
    if (frame[0:8] == "01111110") & (frame[-8:] == "01111110"):
        stuffed_frame_data = frame[8:-8]
        frame_data = stuff_back(stuffed_frame_data)
        crc_from_frame = frame_data[-32:]
        message = frame_data[0:-32]
        # print(message)
        crc_from_message = bin(zlib.crc32(message.encode()))[2:].zfill(32)
        # print("CRC FRAME"+crc_from_frame)
        # print("CRC MESS "+crc_from_message)
        if crc_from_message != crc_from_frame:
            print("ERROR: CRC VALUE IS INCORRECT")
            return "ERROR"
        else:
            return message
    else:
        return "ERROR - no opening or closing frame sequence"


def encode(message=None):
    if message is None:
        file1 = open("message1", "r")
        lines = file1.readlines()
        message = ""
        for line in lines:
            message = message + line.rstrip()
        file1.close()

    crc = bin(zlib.crc32(message.encode()))[2:].zfill(32)
    stuffed_crc = stuff(crc)
    print(crc)
    print(stuffed_crc)
    stuffed_message = stuff(message)

    file = open("frame1", "w")
    file.write("01111110")
    file.write(stuffed_message)
    file.write(stuffed_crc)
    file.write("01111110")
    file.close()
    # print("01111110\n" + stuffed_message + "\n" + stuffed_crc + "\n" + "01111110\n")
    return "01111110" + stuffed_message + stuffed_crc + "01111110"


def stuff(caption):
    stuffed_caption = ""
    one_counter = 0
    for c in caption:
        if one_counter == 5:
            stuffed_caption = stuffed_caption + '0'
            # print(stuffed_caption)
            one_counter = 0
        if c == '1':
            one_counter = one_counter + 1
        else:
            one_counter = 0
        stuffed_caption = stuffed_caption + c
        # print(stuffed_caption+" c = " + str(one_counter))
    return stuffed_caption


def stuff_back(stuffed_caption):
    caption = ""
    one_counter = 0
    for c in caption:
        if one_counter != 5:
            caption = caption + c
        if c == '1':
            one_counter = one_counter + 1
        else:
            one_counter = 0

    return str.replace(stuffed_caption, "111110", "11111")
