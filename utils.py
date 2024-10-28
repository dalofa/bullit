"""View the current log"""
import pandas as pd

def create(board_name):
    """Creates a data file to store to-do board"""
    board_data = pd.DataFrame(columns=["type","task","date","ID"])
    board_data.to_csv(".boards/" + board_name+".data",index=False)

def view(board_name):
    """Views a task-board"""
    board_file = board_name + ".data"

    board_data = pd.read_csv(".boards/" + board_name+".data",sep=",")
    print("--------",board_name,"--------")

    # Define column widths for alignment
    type_width = 10
    desc_width = 30
    date_width = 12
    id_width = 5
    for task in board_data.iterrows():
        task_type = task[1].iloc[0]
        task_desc = task[1].iloc[1]
        task_date = task[1].iloc[2]
        task_id = task[1].iloc[3]
        #mes_format = "\t".join([task_type,task_desc,str(task_date),str(task_id)])
            # Print header

        mes_format = f"{task_type:<{type_width}} {task_desc:<{desc_width}} {str(task_date):<{date_width}} {str(task_id):<{id_width}}"
        print(mes_format)

def add(task_type,task_desc,board_name,task_date="NA"):
    """Adds a task to a task-board"""
    board_data = pd.read_csv(".boards/" + board_name+".data")
    new_id = board_data.ID.max()+1
    new_data = [task_type,task_desc,task_date,new_id]
    board_data.loc[len(board_data)] = new_data
    board_data.to_csv(".boards/" + board_name+".data",index=False)

def finish(board_name,task_id):
    """Finish and remove a task from a task board"""
    board_data = pd.read_csv(".boards/" + board_name+".data")
    board_data = board_data[board_data["ID"]!=task_id]
    board_data.to_csv(".boards/" + board_name+".data",index=False)

view("TEST")