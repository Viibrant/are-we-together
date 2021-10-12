import parse_data

if __name__ == "__main__":
    calendars = parse_data.get_files()
    people = parse_data.parse_files(calendars)

    for person in people:
        print(person.get_lectures("Wednesday"))