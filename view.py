"""View the current log"""
import pandas as pd

from datetime import datetime

# Get the current date and time
today = datetime.now().date()


def get_sign_type(word):
    if word=="dot":
        return "•"
    if word=="exp":
        return "!"
    if word=="dash":
        return "-"
    

def view_date(test_file,date_in):
    """views the entries for today"""
    data = pd.read_csv(test_file,sep=",")
    
    # Convert input to datetime
    date_in_dt = pd.to_datetime(date_in)

    # Convert date column to datetime
    data["date"]= pd.to_datetime(data["date"])

    entries = data[data.date==date_in_dt]
    
    # format for printing
    print("------",date_in,"------")
    for entry in entries.iterrows():
        task_type = entry[1].iloc[1]
        task_type = get_sign_type(task_type)
        task_desc = entry[1].iloc[2]
        task = " ".join([task_type,task_desc])
        print(task)




view_date("test_file.csv",today)