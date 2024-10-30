from board_tools import create_board, add_task, view_board, overview, finish_task, get_current_board
import os
import argparse

def main():
    config_path = ".bullit_config.yaml"

    # Create the parser
    parser = argparse.ArgumentParser(description="Manage task boards.")
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest='command')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new task board')
    create_parser.add_argument('board_name', type=str, help='Name of the task board to create')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task to a task board')
    add_parser.add_argument('board_name', type=str, help='Name of the task board')
    add_parser.add_argument('task_type', type=str, help='Type of the task')
    add_parser.add_argument('description', type=str, help='Description of the task')
    add_parser.add_argument('date', type=str,nargs="?",
                            help='Due date of the task (e.g., YYYY-MM-DD)')

    # view command
    view_parser = subparsers.add_parser('view',help='View a task board')
    view_parser.add_argument('board_name', 
                            type=str,nargs="?",
                            default=get_current_board(config_path),
                            help='Name of the task board')
    # view command alias
    view_parser = subparsers.add_parser('v',help='View a task board.')
    view_parser.add_argument('board_name', 
                            type=str,nargs="?",
                            default=get_current_board(config_path),
                            help='Name of the task board')
    
    # Finish command
    fin_parser = subparsers.add_parser('fin',help='Mark a task as done.')
    fin_parser.add_argument('task_id', 
                            type=str,
                            help='Name of the task board')
    fin_parser.add_argument('board_name', 
                            type=str,nargs="?",
                            default=get_current_board(config_path),
                            help='Name of the task board')
    # Finish command alias
    fin_parser = subparsers.add_parser('f',help='Mark a task as done.')
    fin_parser.add_argument('task_id', 
                            type=str,
                            help='Name of the task board')
    fin_parser.add_argument('board_name', 
                            type=str,nargs="?",
                            default=get_current_board(config_path),
                            help='Name of the task board')
    
    

    # Parse the arguments
    args = parser.parse_args()

    # Call appropriate function based on the command
    
    print(args)
    if args.command == 'create':
        create_board(config_file = config_path,
               board_name=args.board_name
               )
    elif args.command == 'add':
        add_task(config_file=config_path,
                 board_name=args.board_name,
                 task_desc=args.description,
                 )
    elif args.command == 'view' or args.command=="v":
        view_board(config_file=config_path,
                    board_name=args.board_name
                    )
    elif args.command == 'fin' or args.command=="f":
        finish_task(config_file=config_path,
                    board_name=args.board_name,
                    task_id=args.task_id
                    )
    
            
            
        

if __name__ == "__main__":
    # Create the boards directory if it doesn't exist
    os.makedirs('.boards', exist_ok=True)
    main()