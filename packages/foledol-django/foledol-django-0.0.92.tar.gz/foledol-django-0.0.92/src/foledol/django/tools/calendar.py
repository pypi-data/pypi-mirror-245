class CalendarDay:
    def __init__(self, label):
        self.label = label


class CalendarHour:
    def __init__(self, label):
        self.label = label


class CalendarEvent:
    def __init__(self, day, hour, minute, duration, label, onclick=None, css=None):
        self.day = day
        self.hour = hour
        self.minute = minute
        self.duration = duration
        self.label = label
        self.onclick = onclick
        self.css = css


class Calendar:
    def __init__(self, days, hours, events):
        self.days = days
        self.hours = hours
        self.events = events

