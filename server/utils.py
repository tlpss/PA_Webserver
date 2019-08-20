from datetime import  datetime

def datetime_to_unix(timestamp):
    return (timestamp - datetime(1970,1,1)).total_seconds()

def unix_to_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp)