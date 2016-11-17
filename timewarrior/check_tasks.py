#!/usr/bin/env /usr/local/bin/python3

import subprocess
import datetime
import os
import pickle

STORAGE = "/tmp/timewarrior_storage"

SAME_ACTIVITY_CHECK_PERIOD = datetime.timedelta(minutes=30)
NO_ACTIVITY_CHECK_PERIOD = datetime.timedelta(minutes=2)

def get_timewarrior_output(args):
    args = ["/usr/local/bin/timew"] + args
    return subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')

def get_current_tracked_activity():
    output = get_timewarrior_output([])
    lines = output.split('\n')
    first_line = lines[0]
    if first_line.startswith("Tracking"):
        return first_line.split("Tracking ")[1]
    else:
        return None

def get_last_activity():
    if os.path.exists(STORAGE):
        return pickle.load(open(STORAGE, 'rb'))
    return None

def set_last_activity(activity):
    p = pickle.Pickler(open(STORAGE, "wb"))
    p.dump(activity)

def show_notification(message):
    subprocess.run(["/usr/local/bin/terminal-notifier", "-title", 'Timewarrior', "-message", message, "-appIcon", "/Users/acid/Documents/scripts/icons/taskwarrior.png"])

def main():
    activity = get_current_tracked_activity()
    last_activity = get_last_activity()
    now = datetime.datetime.now()
    if last_activity is None or last_activity.get("activity") != activity:
        set_last_activity({"activity": activity, "start_time": now, "last_check_time": now})
    else:
        last_check_time = last_activity.get("last_check_time")
        if not activity is None:
            if now - last_check_time > SAME_ACTIVITY_CHECK_PERIOD:
                show_notification("Are you still working on " + activity + "?")
                last_activity["last_check_time"] = now
                set_last_activity(last_activity)
        else:
            if now - last_check_time > NO_ACTIVITY_CHECK_PERIOD:
                show_notification("What is your current activity?")
                last_activity["last_check_time"] = now
                set_last_activity(last_activity)


if __name__ == "__main__":
    main()
