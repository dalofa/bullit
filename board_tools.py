"""View the current log"""
import pandas as pd
import os
import yaml
from datetime import datetime

def board_found(config_object,board_name,):
    """Checks if a board exists in a config object"""
    # check that a config object is given
    assert type(config_object)==dict, "config_object is not a yaml-derived dict()"

    # iterate through board meta-data
    for board in config_object["boards"]:
            if board["name"]==board_name:
                return True
    return False

def create_board(config_file,board_name,tags=["default"]):
    """Create an empty data file for a task-board and adds it to the config file"""
    with open(config_file,"r") as file:
        config=yaml.safe_load(file)

    if board_found(config,board_name):
        print(f"{board_name} already exists")
    else:
        # Create metadata for board
        c_date = datetime.now()
        c_date_iso = c_date.date().isoformat() #ISO8601-format
        board_dir = config.get("board_dir")
        data_path = os.path.join(board_dir,board_name + ".data")

        board_info = {
            "name": board_name,
            "created": c_date_iso,
            "tags": tags,
            "data_file": data_path}
        
        # Write to config file
        config["boards"].append(board_info)

        with open(config_file, "w") as file:
            yaml.dump(config, file, default_flow_style=False, sort_keys=False)
        
        # create data file
        board_data = pd.DataFrame(columns=["type","task","date","ID","done"])
        board_data.to_csv(data_path,index=False,sep="\t")

def get_current_board(config_file):
    """Returns the current board in a .yaml file"""
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    current_board = config.get("current_board")
    return current_board

def set_current_board(config_file,board_name):
    """Sets the current board in a .yaml file"""
    with open("config_file", "r") as file:
        config = yaml.safe_load(file)

    # Confirm that the board exits before setting it as current
    if board_found(config,board_name,):

        # update current board and write to file
        config["current_board"]=board_name
        with open(config_file, "w") as file:
            yaml.dump(config, file, default_flow_style=False, sort_keys=False)
    else:
        print(f"Board {board_name} does not exist")

def get_board_path(config_file,board_name):
    """Returns the path to a boards data file from a .yaml file"""
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    for board in config["boards"]:
        if board["name"]==board_name:
            return(board["data_file"])
    
    # if no board with the name exists
    print(f"Board {board_name} doest not exist.")
    
def view_board(config_file,board_name):
    """Prints a task-board"""
    board_data = pd.read_csv(get_board_path(config_file,board_name), 
                             sep="\t",
                             dtype={0: str},
                             header=0)
    columns, rows = os.get_terminal_size() # find terminal size
    task_print_size = int(columns/2)
    l_header = (task_print_size-len(board_name.upper()))/2
    r_header = task_print_size - int(l_header)
    board_header = "-" * int(l_header) + board_name.upper() + "-" * int(r_header)
    print(board_header)
    # Define column widths for alignment
    type_width = 1
    date_width = 12
    id_width = 5
    desc_width = int(task_print_size)-id_width-date_width-type_width

    for task in board_data.iterrows():
        task_type = task[1].iloc[0]
        task_desc = task[1].iloc[1]
        task_date = task[1].iloc[2]
        task_id = task[1].iloc[3]
        task_done = bool(task[1].iloc[4])
        if len(task_desc) > desc_width:
            task_desc = task_desc[:desc_width - 3] + "..."
        mes_format = f"{task_type:<{type_width}} {task_desc:<{desc_width}} {str(task_date):<{date_width}} {str(task_id):<{id_width}}"
        
        # strikethrough a finished task
        if task_done:
            print(f"\033[9m{mes_format}\033[0m")
        else:
            print(mes_format)

def add_task(config_file,board_name, task_desc, task_type="•",task_date="NA"):
    """Adds a task to a task-board"""
    board_data = pd.read_csv(get_board_path(config_file,board_name), 
                             sep="\t",
                             dtype={0: str},
                             header=0)
    
    new_id = board_data.ID.max()+1
    task_done=False
    new_data = [task_type,task_desc,task_date,new_id,task_done]
    board_data.loc[len(board_data)] = new_data
    board_data.to_csv(get_board_path(config_file,board_name),
                      index=False,
                      sep="\t")

def finish_task(config_file,board_name,task_id):
    """Update the stauts of a task to done"""
    board_data = pd.read_csv(get_board_path(config_file,board_name), 
                             sep="\t",
                             dtype={0: str},
                             header=0)
    
    # Update board using .loc[row_indexer,col_indexer]=value
    board_data.loc[board_data["ID"]==task_id,"done"]=True

    board_data.to_csv(get_board_path(config_file,board_name),
                      index=False,
                      sep="\t")


def remove_task(config_file,board_name,task_id):
    """Remove a task from a task board"""
    board_data = pd.read_csv(get_board_path(config_file,board_name), 
                             sep="\t",
                             dtype={0: str},
                             header=0)
    
    # Set dataframe to everything except specified ID
    board_data = board_data[board_data["ID"]!=task_id]

    board_data.to_csv(get_board_path(config_file,board_name),
                      index=False,
                      sep="\t")

def clean_board(config_file,board_name):
    """Removes all tasks marked as done"""
    board_data = pd.read_csv(get_board_path(config_file,board_name), 
                            sep="\t",
                            dtype={0: str},
                            header=0)
    
    for task in board_data.iterrows():
        task_id = task[1].iloc[3]
        task_done = task[1].iloc[4]

        if task_done:
            remove(config_file,board_name,task_id)

def overview():
    
    """Displays all task boards side by side with board names and hyphen separators"""
    
    board_dir = ".boards/"
    board_files = [f for f in os.listdir(board_dir) if f.endswith(".data")]
    
    # Define column widths for alignment
    columns, rows = os.get_terminal_size()
    task_print_size = int(columns/2)
    
    type_width = 1
    desc_width = int(task_print_size/3)
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




