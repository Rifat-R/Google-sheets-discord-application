import datetime

def convert_to_analogue(military_time:str):
    print(military_time)
    time_obj = datetime.datetime.strptime(military_time, '%H:%M')

    # format the datetime object as analogue time string
    analogue_time = time_obj.strftime('%I:%M %p')
    return analogue_time



