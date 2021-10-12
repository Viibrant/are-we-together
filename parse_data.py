import datetime
import os
import icalendar
from person import Person


def get_files():
    calendars = []
    for _, _, files in os.walk("people/"):
        for file in files:
            filename, extension = os.path.splitext(file)
            if extension == ".ics":
                icalfile = open(f"people/{file}", "rb")
                gcal = icalendar.Calendar.from_ical(icalfile.read())
                calendars.append({"name": filename, "data": gcal})
                icalfile.close()
    return calendars


def parse_description(description: str):
    details = {}
    key_value = description.split("\n")
    for i in key_value:
        aux = i.split(": ")
        details[aux[0]] = aux[1]
    return details


def same_week(d1, d2):
    return d1.isocalendar()[1] == d2.isocalendar()[1] and d1.year == d2.year


def parse_files(calendars):
    people = []
    for calendar in calendars:
        weekly_lectures = []
        for component in calendar["data"].walk():
            lecture = {}
            same = False

            if component.get("dtstart"):
                component_date = component.get("dtstart").dt
                same = same_week(component_date, datetime.date.today())

            if component.name == "VEVENT" and same:
                lecture = parse_description(component.get("description"))
                lecture["day"] = component.get("dtstart").dt.strftime("%A")
                lecture["start-time"] = component.get("dtstart").dt.time()
                lecture["end-time"] = component.get("dtend").dt.time()
            weekly_lectures.append(lecture)
        people.append(Person(calendar["name"], weekly_lectures))

    return people