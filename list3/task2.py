import random
import collections as col
import copy

CHANNEL_LENGTH = 30
MESSAGE_LENGTH = 2 * CHANNEL_LENGTH
MESSAGE_PROBABILITY = 0.05
# EMPTY_PLACE = '0'
COLLISION = '#'
DISRUPT_SIGNAL = '!'
# NO_DIRECTION = '-'
LEFT = 'L'
RIGHT = 'R'
BOTH = 'B'
channel = list(list() for i in range(0, CHANNEL_LENGTH))
directions = list(list() for i in range(0, CHANNEL_LENGTH))


class Station:
    def __init__(self, location, station_id, talkativeness=MESSAGE_PROBABILITY):
        self.location = location
        self.station_id = station_id
        self.talkativeness = talkativeness
        self.transmitting = 0
        self.disrupting = 0
        self.collision = 0
        self.waiting = 0
        self.resend = False

    def __str__(self):
        return "{Location: " + str(self.location) + " Id:" + str(self.station_id) + "}"


stations = [
    Station(2, 'A'),
    Station(8, 'B'),
    Station(24, 'C'),
    # Station(17, 'C')
]


def peek(l):
    if len(l) > 0:
        return l[0]
    else:
        None


class ChannelWorld:
    def __init__(self, ch, d, s):
        self.channel = ch
        self.directions = d
        self.stations = s
        self.collision_counter = 0

    def print_stations_to_file(self, filename=None):
        if filename is None:
            filename = "stations"
        file1 = open(filename, "a+")
        # file1.writelines('\n' + str(list(map(lambda x: '-' if len(x) <= 0 else x.pop(), self.directions))) + '\n')
        # file1.write('\n')
        # file1.write('\n')
        # for d in self.directions:
        #     if len(d) > 0:
        #         file1.write(str(d[0]))
        #     else:
        #         file1.write('Z-')
        # file1.write('\n')
        for d in self.channel:
            if len(d) > 0:
                if DISRUPT_SIGNAL in d:
                    file1.write(str(DISRUPT_SIGNAL))
                else:
                    file1.write(str(d[0]))
            else:
                file1.write('0')
        file1.write('\n')
        # stations_str = ""
        # for c in range(0, len(self.channel)):
        #     filtered = list(filter(lambda x: x.location == c, stations))
        #     if len(filtered) <= 0:
        #         stations_str = stations_str + ' '
        #     else:
        #         stations_str = stations_str + "{:1}".format(str(filtered[0].station_id))  # + str(filtered[0].resend)
        #     # stations_str = stations_str + '  '
        # file1.writelines(stations_str)
        # file1.write('\n')
        # stati.writelines(stations_str)

    def update_lists(self, chan, dirs):
        self.channel = chan
        self.directions = dirs

    def run_simulation(self, file_name="simulation"):
        k = 3000
        while k > 0:
            new_channel = copy.deepcopy(self.channel)
            new_directions = copy.deepcopy(self.directions)
            for i in range(0, len(self.channel)):
                if len(self.channel[i]) > 0:
                    for j in range(0, len(self.channel[i])):
                        print(i)
                        directions_i = self.directions[i][j]
                        new_directions[i].remove(directions_i)
                        channel_i = self.channel[i][j]
                        new_channel[i].remove(channel_i)
                        print(list(self.channel[i]))
                        if directions_i == LEFT:
                            if i >= 1:
                                new_channel[i - 1].append(channel_i)
                                new_directions[i - 1].append(LEFT)
                        elif directions_i == RIGHT:
                            if i < len(self.channel) - 1:
                                new_channel[i + 1].append(channel_i)
                                new_directions[i + 1].append(RIGHT)
                        elif directions_i == BOTH:
                            print("Both")
                            if i >= 1:
                                new_channel[i - 1].append(channel_i)
                                new_directions[i - 1].append(LEFT)
                            if i < len(self.channel) - 1:
                                new_channel[i + 1].append(channel_i)
                                new_directions[i + 1].append(RIGHT)
                        else:
                            print("ERROR: none corresponding value in directions list")
                # new_channel[i].clear()
                # new_directions[i].clear()

            self.directions = new_directions
            self.channel = new_channel

            for c in range(0, len(self.channel)):
                collision = False
                chan = self.channel[c]
                if len(chan) > 0:
                    tmp = chan[0]
                    for l in chan:
                        if l != tmp:
                            collision = True
                if collision:
                    # chan.clear()
                    # chan.append(COLLISION)
                    # self.directions[c].clear()
                    # self.directions[c].append(BOTH)
                    for i in range(0, len(chan)):
                        if chan[i] != DISRUPT_SIGNAL:
                            chan[i] = COLLISION
                        # self.directions[c][i] =

            for station in stations:
                if station.transmitting > 0:
                    print("Station" + str(station) + " is still talking")
                    station.transmitting = station.transmitting - 1

                    self.channel[station.location].append(station.station_id)
                    self.directions[station.location].append(BOTH)

                    if len(self.channel[station.location]) > 0:
                        if self.channel[station.location][0] == COLLISION:
                            print("Station" + str(station) + "detected collision")
                            self.collision_counter = self.collision_counter + 1
                            station.transmitting = 0
                            station.collision = station.collision + 1
                            station.disrupting = 2 * CHANNEL_LENGTH
                            station.resend = False
                    if station.transmitting == 1:
                        print("Station" + str(station) + " ended sending message successfully")
                        station.collision = 0
                elif station.disrupting > 0: #sygnal zaklocajacy
                    print("Station" + str(station) + " is sending disrupting signal")
                    station.disrupting = station.disrupting - 1
                    self.channel[station.location].append(DISRUPT_SIGNAL)
                    self.directions[station.location].append(BOTH)
                elif station.waiting > 0:
                    print("Station" + str(station) + " is still waiting ("+str(station.waiting)+")")
                    station.waiting = station.waiting - 1
                    if station.waiting == 0:
                        # station.transmitting = 2*CHANNEL_LENGTH
                        station.resend = True
                elif station.collision > 15:
                    print("ERROR: channel overloaded")
                    return
                elif (station.collision > 0) & (not station.resend): #losowanie szczelin czasowych
                    station.waiting = (2*CHANNEL_LENGTH) * random.randint(1, pow(2, min(station.collision, 10)))
                    print("[Choosing waiting time] Station" + str(station) + " is waiting (" + str(station.waiting) + ")")

                elif (station.talkativeness >= random.random()) | station.resend:
                    if len(self.channel[station.location]) <= 0:
                        station.resend = False
                        print("Station" + str(station) + " is talking")
                        station.transmitting = 2 * CHANNEL_LENGTH
                        # station.transmitting = 2
                        self.channel[station.location].append(station.station_id)
                        self.directions[station.location].append(BOTH)
            k = k - 1



            print("END")
            self.print_stations_to_file(file_name)


w = ChannelWorld(channel, directions, stations)
