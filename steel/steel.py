import json
import os
from tabulate import tabulate

time_blocks = {
    "CAMPUS TECNOLOGICO CENTRAL CARTAGO": [
        "7:30 a 8:20", "8:30 a 9:20", "9:30 a 10:20", "10:30 a 11:20", "11:30 a 12:20",
        "12:30 a 12:50", "13:00 a 13:50", "14:00 a 14:50", "15:00 a 15:50", "16:00 a 16:50",
        "17:00 a 17:50", "18:00 a 18:50", "19:00 a 19:50", "20:00 a 20:50", "21:00 a 21:50"
    ],
    "CAMPUS TECNOLOGICO LOCAL SAN JOSE": [
        "7:30 a 8:20", "8:30 a 9:20", "9:30 a 10:20", "10:30 a 11:20", "11:30 a 12:20",
        "12:30 a 12:50", "13:00 a 13:50", "14:00 a 14:50", "15:00 a 15:50", "16:00 a 16:50",
        "17:00 a 17:50", "18:00 a 18:50", "19:00 a 19:50", "20:00 a 20:50", "21:00 a 21:50"
    ],
    "CENTRO ACADEMICO DE LIMON": [
        "7:30 a 8:20", "8:30 a 9:20", "9:30 a 10:20", "10:30 a 11:20", "11:30 a 12:20",
        "12:30 a 12:50", "13:00 a 13:50", "14:00 a 14:50", "15:00 a 15:50", "16:00 a 16:50",
        "17:00 a 17:50", "18:00 a 18:50", "19:00 a 19:50", "20:00 a 20:50", "21:00 a 21:50"
    ],
    "CENTRO ACADEMICO DE ALAJUELA": [
        "7:00 a 7:50", "8:00 a 8:50", "9:00 a 9:50", "10:00 a 10:50", "11:00 a 11:50",
        "12:00 a 12:50", "13:00 a 13:50", "14:00 a 14:50", "15:00 a 15:50", "16:00 a 16:50",
        "17:00 a 17:50", "18:00 a 18:50", "19:00 a 19:50", "20:00 a 20:50", "21:00 a 21:50"
    ],
    "CAMPUS TECNOLOGICO LOCAL SAN CARLOS": [
        "7:00 a 7:50", "7:55 a 8:45", "8:50 a 9:40", "9:45 a 10:35", "10:40 a 11:30",
        "11:35 a 12:25", "12:30 a 13:20", "13:25 a 14:15", "14:20 a 15:10", "15:15 a 16:05",
        "16:10 a 17:00", "17:05 a 17:55", "18:00 a 18:50", "18:55 a 19:45", "19:50 a 20:40"
    ]
}

def display_schedule(selected_campus, selected_courses, table, time_slots):
    for i in range(1, len(table)):
        for j in range(1, len(table[0])):
            table[i][j] = ""

    for course in selected_courses:
        for session in course["schedule"]:
            day = session["day"]
            start_time = session["start_time"].lstrip("0")
            end_time = session["end_time"].lstrip("0")
            day_index = ["L", "K", "M", "J", "V"].index(day) + 1

            start_matched = False
            for i, slot in enumerate(time_slots):
                if start_time in slot:
                    table[i + 1][day_index] = course["name"]
                    start_matched = True
                elif start_matched and end_time in slot:
                    table[i + 1][day_index] = course["name"]
                    break

    print("\nUpdated Schedule Table:")
    print(tabulate(table, headers="firstrow", tablefmt="grid"))

def check_conflict(course, table, time_slots):
    for session in course["schedule"]:
        day = session["day"]
        start_time = session["start_time"].lstrip("0")
        end_time = session["end_time"].lstrip("0")

        day_index = ["L", "K", "M", "J", "V"].index(day) + 1

        for i, slot in enumerate(time_slots):
            if start_time in slot:
                if table[i + 1][day_index] != "":
                    return True

            if end_time in slot:
                if table[i + 1][day_index] != "":
                    return True
    return False

def main():
    print("""\033[38;2;202;78;50m
  ▄████████   ▄▄▄▄███▄▄▄▄   ▀█████████▄     ▄████████    ▄████████
  ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███   ███    ███   ███    ███
  ███    █▀  ███   ███   ███   ███    ███   ███    █▀    ███    ███
 ▄███▄▄▄     ███   ███   ███  ▄███▄▄▄██▀   ▄███▄▄▄      ▄███▄▄▄▄██▀
▀▀███▀▀▀     ███   ███   ███ ▀▀███▀▀▀██▄  ▀▀███▀▀▀     ▀▀███▀▀▀▀▀
  ███    █▄  ███   ███   ███   ███    ██▄   ███    █▄  ▀███████████
  ███    ███ ███   ███   ███   ███    ███   ███    ███   ███    ███
  ██████████  ▀█   ███   █▀  ▄█████████▀    ██████████   ███    ███
                                                         ███    ███
\033[0m
              █████████ █████                 ████
             ███░░░░░██░░███                 ░░███
            ░███    ░░░███████   ██████ ██████░███
            ░░████████░░░███░   ███░░█████░░██░███
             ░░░░░░░░███░███   ░██████░███████░███
             ███    ░███░███ ██░███░░░░███░░░ ░███
            ░░█████████ ░░█████░░█████░░███████████
             ░░░░░░░░░   ░░░░░  ░░░░░░ ░░░░░░░░░░░

"Steel" is the second part of the Ember project, in order to utilize this you must have an export of the classes you can currently take from "Flint".
""")
    file_path = input("[\033[31m♡\033[0m] Enter the path to the JSON file: ")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("""
\033[31mError: Invalid file or JSON format.\033[0m

A "path" refers to the location of a file or directory within your computer's file system. It tells your program where to find a file.

Paths differ slightly depending on the operating system:

1. Windows:
   - Examples:
     - `C:\\Users\\JohnDoe\\Desktop\\ember_schedule_export.json`

2. Mac and Linux:
   - Use forward slashes (`/`) to separate directories.
   - Examples:
     - `/Users/JohnDoe/Desktop/ember_schedule_export.json`
""")
        return

    campus_list = list(time_blocks.keys())
    print("\nSelect a campus:\n")
    for i, campus in enumerate(campus_list):
        print(f"{i + 1}. {campus}")
    campus_choice = int(input("\n[\033[31m♡\033[0m] Enter the number of your choice: ")) - 1
    if campus_choice < 0 or campus_choice >= len(campus_list):
        print("Invalid selection.")
        return

    selected_campus = campus_list[campus_choice]
    print(f"\nSelected campus: {selected_campus}")

    available_courses = []
    for course_id, course in data.items():
        if selected_campus in course["campuses"]:
            for group, details in course["campuses"][selected_campus].items():
                available_courses.append({
                    "id": len(available_courses) + 1,
                    "name": course["course_name"],
                    "group": group,
                    "schedule": details["schedule"],
                    "professor": details["professors"]
                })

    selected_courses = []

    time_slots = time_blocks[selected_campus]
    days = ["Time", "Monday (L)", "Tuesday (K)", "Wednesday (M)", "Thursday (J)", "Friday (V)"]
    table = [days] + [[slot] + [""] * 5 for slot in time_slots]

    while True:
        print("\nRun the 'help' command to see available commands.\n")
        command = input("\033[90m[\033[37mSteel\033[90m@\033[38;2;202;78;50mEmber\033[90m]\033[0m $ ").strip().lower()

        if command == "done":
            break
        elif command == "list_available":
            print("\nAvailable Courses:")
            print(tabulate(
                [
                    [
                        c["id"],
                        c["name"],
                        c["group"],
                        c["professor"],
                        ", ".join(
                            f"{s['day']} {s['start_time']}-{s['end_time']}"
                            for s in c["schedule"]
                        )
                    ]
                    for c in available_courses
                ],
                headers=["ID", "Name", "Group", "Professor", "Schedule"],
                tablefmt="grid"
            ))
        elif command == "help":
            print("""
            Available Commands:

            'add COURSE_NUMBER'     : Add a course to your schedule. Use the course ID provided in the list of available courses.
            'remove COURSE_NUMBER'  : Remove a course from your schedule. Use the course ID from the signed-up courses list.
            'list_available'        : List all available courses with details like name, group, professor, and schedule.
            'list_signed_up'        : List all the courses you are currently signed up for.
            'view_schedule'         : Display your current schedule with the selected courses.
            'clear'                 : Clears the screen.
            'done'                  : Exit the program.
            """)
        elif command == "list_signed_up":
            print("\nSigned Up Courses:")
            if selected_courses:
                print(tabulate(
                    [
                        [
                            c["id"],
                            c["name"],
                            c["group"],
                            c["professor"],
                            ", ".join(
                                f"{s['day']} {s['start_time']}-{s['end_time']}"
                                for s in c["schedule"]
                            )
                        ]
                        for c in selected_courses
                    ],
                    headers=["ID", "Name", "Group", "Professor", "Schedule"],
                    tablefmt="grid"
                ))
            else:
                print("You are not signed up for any courses.")
        elif command.startswith("add "):
            try:
                course_id = int(command.split()[1])
                course = next((c for c in available_courses if c["id"] == course_id), None)
                if course:
                    if check_conflict(course, table, time_slots):
                        print(f"Error: The course '{course['name']}' conflicts with an existing course in the schedule.")
                    else:
                        selected_courses.append(course)
                        available_courses.remove(course)
                        print(f"Course '{course['name']}' added.")
                        display_schedule(selected_campus, selected_courses, table, time_slots)
                else:
                    print("Invalid course ID.")
            except ValueError:
                print("Invalid input. Use 'add NUMBER'.")
        elif command == "view_schedule":
            display_schedule(selected_campus, selected_courses, table, time_slots)
        elif command == "clear":
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
            print("Screen cleared.")
        elif command.startswith("remove "):
            try:
                course_id = int(command.split()[1])
                course = next((c for c in selected_courses if c["id"] == course_id), None)
                if course:
                    available_courses.append(course)
                    selected_courses.remove(course)
                    print(f"Course '{course['name']}' removed.")
                    display_schedule(selected_campus, selected_courses, table, time_slots)
                else:
                    print("Invalid course ID.")
            except ValueError:
                print("Invalid input. Use 'remove NUMBER'.")
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
