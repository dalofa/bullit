"""View the current log"""
import pandas as pd
import os

def create(board_name):
    """Creates a data file to store to-do board"""
    board_data = pd.DataFrame(columns=["type","task","date","ID"])
    board_data.to_csv(".boards/" + board_name+".data",index=False)

def view(board_name):
    """Views a task-board"""
    board_data = pd.read_csv(".boards/" + board_name+".data",sep=",")
    print("--------",board_name,"--------")

    # Define column widths for alignment
    type_width = 1
    desc_width = 50
    date_width = 12
    id_width = 5

    for task in board_data.iterrows():
        task_type = task[1].iloc[0]
        task_desc = task[1].iloc[1]
        task_date = task[1].iloc[2]
        task_id = task[1].iloc[3]

        if len(task_desc) > desc_width:
            task_desc = task_desc[:desc_width - 3] + "..."
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
    board_data = board_data[board_data["ID"]!=task_id] # remove ID
    board_data.to_csv(".boards/" + board_name+".data",index=False)

def overview():
    """Displays all task boards side by side with board names and hyphen separators"""
    
    board_dir = ".boards/"
    board_files = [f for f in os.listdir(board_dir) if f.endswith(".data")]
    
    # Define column widths for alignment
    type_width = 1
    desc_width = 20
    date_width = 5
    id_width = 2
    column_total_width = type_width + desc_width + date_width + id_width + 3  # 3 for spacing between fields

    # Print board names as headers with hyphen fillers between
    headers = []
    for board_file in board_files:
        board_name = board_file.split(".")[0]
        header = f"{'-' * 5}{board_name}{'-' * 5}".center(column_total_width, "-")
        headers.append(header)
    print("   ".join(headers))
    
    # Prepare DataFrames for each board
    max_rows = 0
    boards_data = []
    for board_file in board_files:
        board_data = pd.read_csv(os.path.join(board_dir, board_file), sep=",")
        boards_data.append(board_data)
        max_rows = max(max_rows, len(board_data))
    
    # Print tasks row by row
    for i in range(max_rows):
        row_outputs = []
        for board_data in boards_data:
            if i < len(board_data):
                task_type = board_data.iloc[i, 0]
                task_desc = board_data.iloc[i, 1]
                task_date = board_data.iloc[i, 2]
                task_id = board_data.iloc[i, 3]

                # Truncate description if it's too long
                if len(task_desc) > desc_width:
                    task_desc = task_desc[:desc_width - 3] + "..."

                # Format each task as a row
                row_output = f"{task_type:<{type_width}} {task_desc:<{desc_width}} {str(task_date):<{date_width}} {str(task_id):<{id_width}}"
            else:
                # If no row exists in this board, add empty spaces
                row_output = f"{'':<{type_width}} {'':<{desc_width}} {'':<{date_width}} {'':<{id_width}}"
            
            row_outputs.append(row_output)
        
        # Print all boards' tasks in the same row
        print("   ".join(row_outputs))