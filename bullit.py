from board_tools import create, add, view, overview, finish
import os
import argparse

def main():
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
    add_parser.add_argument('date', type=str, help='Due date of the task (e.g., YYYY-MM-DD)')
    add_parser.add_argument('task_id', type=int, help='ID of the task')
    add_parser.add_argument('--status', type=str, default='in progress', help='Status of the task (default: in progress)')

    # Parse the arguments
    args = parser.parse_args()

    # Call appropriate function based on the command
    if args.command == 'create':
        create(args.board_name)
    elif args.command == 'add':
        add(args.board_name, args.task_type, args.description, args.date, args.task_id, args.status)

if __name__ == "__main__":
    # Create the boards directory if it doesn't exist
    os.makedirs('.boards', exist_ok=True)
    main()