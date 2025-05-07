import datetime
import time
import winsound  # For playing sound on Windows

# Ask the user for the alarm time
user = input("Enter time (format: HH:MM:SS): ")
form = "%H:%M:%S"

try:
    datetime_obj = datetime.datetime.strptime(user, form)
    alarm_time = datetime_obj.time()  
    print(f"Alarm set for: {alarm_time}")

    while True:
        
        current_time = datetime.datetime.now().time()

        if current_time.hour == alarm_time.hour and \
           current_time.minute == alarm_time.minute and \
           current_time.second == alarm_time.second:
            print("Wake up! Alarm is ringing!")
            winsound.Beep(2500, 1000) 
            break  
        time.sleep(1)

except ValueError:
    print("Invalid input format. Please use the format HH:MM:SS.")











