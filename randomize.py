"""
Filename: randomize.py
Author: Roland Pelzel
Last Updated: 2026-20-2
Description: This script chooses a random item from an item file and provides
             command line arguments to interact with the item data. 
"""

import random
import sys
import time

ITEMS = "items.txt" # The file from which random items will be selected.
USED  = "used.txt"  # File keeping track of selected items to avoid duplicates.
TYPEPRINT = True    # Turns on/off the typing effect to the console.

# Main program logic.
def main():
    
    ########## COMMAND LINE ARGUMENTS ##########
    
    # Error checking argc.
    if len(sys.argv) > 9:
        if TYPEPRINT:
            typePrint("Too many arguments")
        else:
            print("Too many arguments")
        sys.exit(1)
    
    #### TWO LENGTH ARGUMENTS ####
    if len(sys.argv) == 2:
        
        # To append to item file.
        if sys.argv[1] == "-e":
            count = enter(ITEMS)
            if TYPEPRINT:
                typePrint(f"{count} items entered into {ITEMS}")
            else:
                print(f"{count} items entered into {ITEMS}")
            return
        
        # To sort the file alphanumerically.
        if sys.argv[1] == "-s":
            count = sort(ITEMS)
            if TYPEPRINT:
                typePrint(f"Sorted {count} items alphanumerically")
            else:
                print(f"Sorted {count} items alphanumerically")
            return
        
        # To remove multiple items from item file.
        if sys.argv[1] == "-r":
            count = remove(ITEMS)
            if TYPEPRINT:
                typePrint(f"Removed {count} items from {ITEMS}")
            else:
                print(f"Removed {count} items from {ITEMS}")
            return
        
        # To rename multiple items from item file.
        if sys.argv[1] == "--rename":
            count = rename()
            if TYPEPRINT:
                if count == 1:
                    typePrint(f"Renamed {count} item in {ITEMS}")
                else:
                    typePrint(f"Renamed {count} items in {ITEMS}")
            else:
                if count == 1:
                    print(f"Renamed {count} item in {ITEMS}")
                else:
                    print(f"Renamed {count} items in {ITEMS}")
            return
        
        # To clear item file.
        if sys.argv[1] == "-c":
            if clear() == 0:
                if TYPEPRINT:
                    typePrint(f"Cleared {ITEMS}")
                else:
                    print(f"Cleared {ITEMS}")
            else:
                if TYPEPRINT:
                    typePrint("Cannot clear, invalid file")
                else:
                    print("Cannot clear, invalid file")
            return
        
        else:
            if TYPEPRINT:
                typePrint("Unrecognized flag")
            else:
                print("Unrecognized flag")
            return
    
    #### THREE LENGTH ARGUMENTS ####
    if len(sys.argv) == 3:

        # To remove a single item from file.
        if sys.argv[1] == "-r":
            remove(ITEMS, True, sys.argv[2])
            if TYPEPRINT:
                typePrint(f"Removed '{sys.argv[2]}' from {ITEMS}")
            else:
                print(f"Removed '{sys.argv[2]}' from {ITEMS}")
            return
        
        # To append a single item to file.
        if sys.argv[1] == "-e":
            enter(ITEMS, True, sys.argv[2])
            if TYPEPRINT:
                typePrint(f"'{sys.argv[2]}' was entered into {ITEMS}")
            else:
                print(f"'{sys.argv[2]}' was entered into {ITEMS}")
            return
        
        # To clear file.
        if sys.argv[1] == "-c":
            status = clear(sys.argv[2])
            if status == 0:
                if TYPEPRINT:
                    typePrint(f"Cleared {sys.argv[2]}")
                else:
                    print(f"Cleared {sys.argv[2]}")
            else:
                if TYPEPRINT:
                    typePrint("Cannot clear, invalid file")
                else:
                    print("Cannot clear, invalid file")
            return
        
        else:
            if TYPEPRINT:
                typePrint("Unrecognized flag")
            else:
                print("Unrecognized flag")
            return
    
    #### FOUR LENGTH ARGUMENTS ####
    if len(sys.argv) == 4:
        
        # To rename a single item in item file.
        if sys.argv[1] == "--rename":
            status = rename(sys.argv[2], sys.argv[3], True)
            if status == 0:
                if TYPEPRINT:
                    typePrint(f"Renamed '{sys.argv[2]}' to '{sys.argv[3]}'")
                else:
                    print(f"Renamed '{sys.argv[2]}' to '{sys.argv[3]}'")
            else:
                if TYPEPRINT:
                    typePrint("Name not in file (names are case-sensitive!)")
                else:
                    print("Name not in file (names are case-sensitive!)")
            return
        
        else:
            if TYPEPRINT:
                typePrint("Unrecognized flag")
            else:
                print("Unrecognized flag")
            return
        
    #### VARIABLE LENGTH ARGUMENTS ####
    if len(sys.argv) > 4 and len(sys.argv) < 10:
        # (likely shouldn't need to ever input more than 10 arguments)
        
        # To remove a single item from file.
        if sys.argv[1] == "-r":
            argv2 = catargs(sys.argv)
            remove(ITEMS, True, argv2)
            if TYPEPRINT:
                typePrint(f"Removed '{argv2}' from {ITEMS}")
            else:
                print(f"Removed '{argv2}' from {ITEMS}")
            return
        
        # To append a single item to file.
        if sys.argv[1] == "-e":
            argv2 = catargs(sys.argv)
            enter(ITEMS, True, argv2)
            if TYPEPRINT:
                typePrint(f"'{argv2}' was entered into {ITEMS}")
            else:
                print(f"'{argv2}' was entered into {ITEMS}")
            return
        
        # To rename a single item in item file.
        if sys.argv[1] == "--rename":
            args = (sys.argv, True)
            status = rename(args[0], args[1], True)
            if status == 0:
                if TYPEPRINT:
                    typePrint(f"Renamed '{args[0]}' to '{args[1]}'")
                else:
                    print(f"Renamed '{args[0]}' to '{args[1]}'")
            else:
                if TYPEPRINT:
                    typePrint("Name not in file (names are case-sensitive!)")
                else:
                    print("Name not in file (names are case-sensitive!)")
            return
        
        else:
            if TYPEPRINT:
                typePrint("Unrecognized flag")
            else:
                print("Unrecognized flag")
            return
    
    ########## PROGRAM LOGIC ##########
    
    # Read items file. 
    itemList = []
    try:
        with open(ITEMS, "r") as file:
            line = file.readline()
            while line != "":
                itemList.append(line.strip())
                line = file.readline()
    except FileNotFoundError as fnf:
        if TYPEPRINT:
            typePrint(str(fnf))
            open(ITEMS, "w").close()
            typePrint(f"Created file '{ITEMS}'; re-run script to continue")
        else:
            print(str(fnf))
            open(ITEMS, "w").close()
            print(f"Created file '{ITEMS}'; re-run script to continue")
        sys.exit(1)

    # Read used items. 
    usedList = []
    try:
        with open(USED, "r") as file:
            line = file.readline()
            while line != "":
                usedList.append(line.strip())
                line = file.readline()
    except FileNotFoundError as fnf:
        if TYPEPRINT:
            typePrint(str(fnf))
            open(USED, "w").close()
            typePrint(f"Created file '{USED}'; re-run script to continue")
        else:
            print(str(fnf))
            open(USED, "w").close()
            print(f"Created file '{USED}'; re-run script to continue")
        sys.exit(1)

    if len(usedList) >= len(itemList) and itemList:
        open(USED, "w").close()
        usedList = []
        if TYPEPRINT:
            typePrint("ALL ITEMS CYCLED THROUGH; RESTARTING CYCLE")
        else:
            print("ALL ITEMS CYCLED THROUGH; RESTARTING CYCLE")

    # Remove already used items from itemList.
    for i in usedList:
        if i in itemList:
            itemList.remove(i)
    
    try:
        choice = random.choice(itemList)
    except IndexError as ie:
        if TYPEPRINT:
            typePrint(str(ie))
            typePrint(f"Enter at least one item into {ITEMS} with the " + 
                      "'-e' flag or in a text editor")
            sys.exit(1)
        else:
            print(str(ie))
            print(f"Enter at least one item into {ITEMS} with the " + 
                      "'-e' flag or in a text editor")
            sys.exit(1)
    
    enter(USED, True, choice)
    if TYPEPRINT:
        typePrint(choice)
    else:
        print(choice)
    return


def enter(FILENAME: str, single: bool = False, choice: str = "") -> int:
    """
    Enters one or more items into a specified file.
    
    :param FILENAME: The file to which data will be entered
    :param single: Will prompt user for more input if False
    :param choice: Will enter choice into file if it's a single input
    :return: How many items were entered into the file
    :rtype: int
    """
    count = 0
    if single:
        with open(FILENAME, "a") as file:
            file.write(choice + '\n')
            count += 1
    else:
        with open(FILENAME, "a") as file:
            if TYPEPRINT:
                typePrint("Enter items into the randomize list: ", False)
                item = input()
            else:
                item = input("Enter items into the randomize list:\n")
            while item != "":
                file.write(item + '\n')
                count += 1
                item = input()
    
    return count


def remove(FILENAME: str, single: bool = False, item: str = "") -> int:
    """
    Removes the specified item(s) from the specified file.
    
    :param FILENAME: The file from which to data will be removed
    :param single: Will prompt user for more input if False
    :param item: Single item to be removed
    :return: How many items were removed from the file
    :rtype: int
    """
    # Read items file. 
    itemList = []
    try:
        with open(FILENAME, "r") as file:
            line = file.readline()
            while line != "":
                itemList.append(line.strip())
                line = file.readline()
    except FileNotFoundError as fnf:
        if TYPEPRINT:
            typePrint(str(fnf))
        else:
            print(str(fnf))
        sys.exit(1)
    
    itemList.sort()

    # Remove item from itemList
    count = 0
    if single:
        if item in itemList:
            itemList.remove(item)
            count += 1
        else:
            if TYPEPRINT:
                typePrint(f"'{item}' was not in {FILENAME} " + 
                        "(remember, it's case-sensitive!)")
            else:
                print(f"'{item}' was not in {FILENAME} " + 
                    "(remember, it's case-sensitive!)")
            sys.exit()
    else:
        if TYPEPRINT:
            typePrint("Enter an item you want removed: ", False)
            item = input()
        else:
            item = input("Enter an item you want removed: ")
        while item != "":
            if item in itemList:
                itemList.remove(item)
                count += 1
            else:
                if TYPEPRINT:
                    typePrint(f"'{item}' was not in {FILENAME} " + 
                            "(remember, it's case-sensitive!)")
                else:
                    print(f"'{item}' was not in {FILENAME} " + 
                        "(remember, it's case-sensitive!)")
            
            if TYPEPRINT:
                typePrint("Enter another item or enter/return to quit: ", False)
                item = input()
            else:
                item = input("Enter another item or enter/return to quit: ")
        
    
    # Overwrite the file with the updated list. 
    with open(FILENAME, "w") as file:
        for i in itemList:
            file.write(i + '\n')
            
    return count
        

def sort(FILENAME: str) -> int:
    """
    Sorts the items of the specified file alphanumerically.
    
    :param FILENAME: The file to sort
    :return: Number of items sorted
    :rtype: int
    """
    # Read items file. 
    itemList = []
    try:
        with open(FILENAME, "r") as file:
            line = file.readline()
            while line != "":
                itemList.append(line.strip())
                line = file.readline()
    except FileNotFoundError as fnf:
        if TYPEPRINT:
            typePrint(str(fnf))
        else:
            print(str(fnf))
        sys.exit(1)
    
    itemList.sort() # Sort the list.

    # Overwrite the file with the sorted list. 
    with open(FILENAME, "w") as file:
        for i in itemList:
            file.write(i + '\n')
            
    return len(itemList)


def rename(item: str = "", newname: str = "", single: bool = False) -> int:
    """
    Renames the specified item(s) in the item file.
    
    :param item: Item to be renamed
    :param newname: New item name
    :param single: Will prompt user for more input if False
    :return: Number of items renamed or an status code, 0 for OK; 1 for not OK
    :rtype: int
    """
    count = 0
    # Read items file. 
    itemList = []
    try:
        with open(ITEMS, "r") as file:
            line = file.readline()
            while line != "":
                itemList.append(line.strip())
                line = file.readline()
    except FileNotFoundError as fnf:
        if TYPEPRINT:
            typePrint(fnf)
        else:
            print(fnf)
        sys.exit(1)
    
    if single:
        if item in itemList:
            itemList[itemList.index(item)] = newname
            itemList.sort()
            # Overwrite the file with the updated list. 
            with open(ITEMS, "w") as file:
                for i in itemList:
                    file.write(i + '\n')
            return 0
        else:
            return -1
    else:
        if TYPEPRINT:
            typePrint(
                "Enter the name of the item you would like to change: ", False)
            item = input()
        else:
            item = input(
                "Enter the name of the item you would like to change: ")
        while item != "":
            if item in itemList:
                if TYPEPRINT:
                    typePrint("Enter the item's new name: ", False)
                    newname = input()
                else:
                    newname = input("Enter the item's new name: ")
                itemList[itemList.index(item)] = newname
                count += 1
            else:
                if TYPEPRINT:
                    typePrint("That item was not in the file")
                else:
                    print("That item was not in the file")
                    
            if TYPEPRINT:
                typePrint(
                    "Enter another item name or enter/return to quit: ", False)
                item = input()
            else:
                item = input(
                    "Enter another item name or enter/return to quit: ")
        
        # Overwrite the file with the updated list. 
        itemList.sort()
        with open(ITEMS, "w") as file:
            for i in itemList:
                file.write(i + '\n')
            
        return count


def clear(FILENAME: str = ITEMS) -> int:
    """
    Clears the contents of the provided file, the item file by default
    
    :param FILENAME: Name of the file to clear
    :return: 0 is successful, -1 if unsuccessful
    :rtype: int
    """
    if FILENAME == ITEMS or FILENAME == USED:
        open(FILENAME, "w").close()
        return 0
    return -1

# TODO
def catargs(args: list[str], rename: bool = False) -> str | list[str]:
    """
    Concatenates command line arguments into one string.
    
    :param args: List of command line arguments
    :return: Concatenated command line arguments
    :rtype: str
    """
    #flags = ["-e", "-r", "--rename"]
    string = ""
    if rename:
        new = ""
        to = False
        for i in range(2, len(args)):
            if i == 'TO':
                to = True
                continue
            elif to:
                (new + " ").join(i)
            else:
                (string + " ").join(i)
        return [string, new]
    
    for i in range(2, len(args)):
        (string + " ").join(i)
    return string


def typePrint(text: str, newline: bool = True):
    """
    Creates a typing effect when printing to the console. Bit of fun.
    
    :param text: The text to be printed
    :param newline: Toggle newline, prints newline on default True
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)  # Adjust speed (lower = faster).
    if newline:
        print() # For newline character.

main()