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

        self.events = [
            CalendarEvent(0, 1, 30, 30, "9:30 - Cours1"),
            CalendarEvent(1, 1, 40, 30, "9:40 - Cours2",
              onclick="alert(\"hello\");",
              css="calendar_event_red"
            )
        ]

