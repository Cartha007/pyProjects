import time
import datetime
import winsound



def countdown(seconds):
    time_elapsed = 0
    
    while time_elapsed < seconds:
        time.sleep(1)
        time_elapsed += 1
        
        time_left = seconds - time_elapsed
        minutes_left = time_left // 60
        seconds_left = time_left % 60
        
        print(f"{minutes_left:02}:{seconds_left:02}")

def alarm():
    hour = int(input("Enter hour: "))
    minute = int(input("Enter minutes: "))
    alarmAm = input("am / pm: ").lower()
    
    if alarmAm == "pm":
        hour += 12
        
    while True:
        if hour == datetime.datetime.now().hour and minute == datetime.datetime.now().minute:
            print("Time up!")
            for i in range(20):
                winsound.Beep(1000, 1000)
            break

alarm()