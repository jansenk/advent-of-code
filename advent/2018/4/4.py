import re
import sys
t = '[1518-02-06 23:52] Guard #3109 begins shift'
et = '\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})\] (?P<message>.*)'
bt = 'Guard \#(?P<id>\d*?) begins shift'
class Guard:
    def __init__(self, id):
        self.id = id
        self.sleep_history = [0 for _ in range(0, 60)]
        self.total_minutes = 0
        self.most_slept_minute = None
        self.personal_best = 0
    
    def add_sleep(self, start, end):
        self.total_minutes += (end - start)
        for min in range(start, end):
            self.sleep_history[min] += 1
            if self.sleep_history[min] > self.personal_best:
                self.personal_best = self.sleep_history[min]
                self.most_slept_minute = min    

class GuardEntry:
    def __init__(self, line):
        self.line = line
        entrymatch = re.match(et, line)
        entrydict = entrymatch.groupdict()
        self.year = int(entrydict["year"])
        self.month = int(entrydict["month"])
        self.day = int(entrydict["day"])
        self.hour = int(entrydict["hour"])
        self.minute = int(entrydict["minute"])
        self.guardEvent = False
        self.sleepEvent = False
        self.wakeEvent = False
        message = entrydict["message"]
        if message.find("Guard") != -1:
            self.guardEvent = True
            guardMatch = re.search(bt, message)
            self.guardId = int(guardMatch.group("id"))
        elif message.find("asleep") != -1:
            self.sleepEvent = True
        elif message.find("wakes") != -1:
            self.wakeEvent = True
        else:
            raise Exception("I've discovered a message I can't parse: %s" % message)

    def __lt__(self, other):
        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month
        if self.day != other.day:
            return self.day < other.day
        if self.hour != other.hour:
            return self.hour < other.hour
        return self.minute < other.minute

entries = [GuardEntry(l.strip()) for l in open("in.txt", "r")]
entries = sorted(entries)
#for entry in entries:
#    print(entry.line)
guards = dict()
guard = None
sleepStart = None
for entry in entries:
    if entry.guardEvent:
        if entry.guardId not in guards:
            guards[entry.guardId] = Guard(entry.guardId)
        guard = guards[entry.guardId]
    elif entry.sleepEvent:
        sleepStart = entry.minute
    elif entry.wakeEvent:
        guard.add_sleep(sleepStart, entry.minute)
        sleepStart = None

def getBestGuard(maxGetter):
    maxVal = 0
    sleepiest = None
    for guard in guards.values():
        val = maxGetter(guard)
        if val > maxVal:
            maxVal = val
            sleepiest = guard
    return sleepiest

sleepiest_total = getBestGuard(lambda g: g.total_minutes)
gid = sleepiest_total.id
gm = sleepiest_total.most_slept_minute
f = (gid, gm, gid, gm, gid * gm)
print("Sleepiest Guard is #%d, sleeps most on minute %d\n%d * %d = %d" % f)

sleepiest_pb = getBestGuard(lambda g: g.personal_best)
gid = sleepiest_pb.id
gm = sleepiest_pb.most_slept_minute
f = (gid, gm, gid, gm, gid * gm)
print("Sleepiest Guard is #%d, sleeps for the most on minute %d\n%d * %d = %d" % f)


