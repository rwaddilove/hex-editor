# Hex editor by Roland Waddilove
# Open a file on disk and show it in hexadecimal or decimal views.
# Edit any byte in the file and save the modified file.
# It reads/shows 256 bytes at a time, so files can be any size.
# This program was written as a Python learning exercise and reflects
# what I've learnt so far. There are probably better ways of doing this.
# More Python learning programs at https://github.com/rwaddilove/

import os


def select_file(filetype) -> str:
    """ List files of type filetype like '.csv' in current folder. Use '*' for all."""
    print(f"\nFiles of type '{filetype}' in this folder:")
    # add files to list and display
    files = []
    i = 0
    for item in os.listdir():
        if not os.path.isfile(item): continue
        if item.startswith('.'): continue
        if filetype == '*' or item.endswith(filetype):
            files.append(item)
            print(i, item)
            i += 1
    print()
    # select file to use. Enter to exit with no file selected
    i = -1
    inp = input(f"Enter file num: ").strip()
    if inp.isdigit(): i = int(inp)
    if i < 0 or i >= len(files): return ''
    return files[i]


def select_folder() -> str:
    """Allow user to browse the disk and select a folder. Most system folders are hidden."""
    print("\n==== Select folder to use ====")
    os.chdir(os.path.expanduser('~'))       # user's home folder
    print("Current folder: ", os.getcwd())
    inp = input("Use this (Y)es (N)o? ").upper()
    if inp == 'Y': return os.getcwd()

    # select folder to store task data
    os.chdir(os.path.expanduser('~'))       # user's home folder
    while inp != 'U':
        print()
        dirs = []
        i = 0
        for item in os.listdir():
            if os.path.isdir(item) and not item.startswith('.'):
                dirs.append(item)
                print(f"{i} {item} ".ljust(30))
                i += 1
        print("\nCurrent Folder: ", os.getcwd())
        inp = input(f"(U)se this, (B)ack, or folder num: ").upper()
        if inp.isdigit():
            i = int(inp)
            if i < len(dirs): os.chdir(dirs[i])
        if inp == 'B' and os.getcwd() != os.path.expanduser('~'): os.chdir('..')
    return os.getcwd()


def read_file() -> bytearray:
    """Read in a chunk of a file from position fptr*chunk size."""
    with open(file, 'rb') as f:     # read file
        f.seek(fptr * 256)           # go to position in file
        b = bytearray(f.read(256))   # read chunk of data
    return b


def show_file() -> None:
    """Show the chunk of data read from the file in hex or dec."""
    for b in range(0, len(data), 8):
        asc = '  '
        if numbase == 16:
            s = '000000' + hex(b + fptr*256)[2:]    # leading zeros
            print(f"{s[-6:]}: ", end='')
        else:
            print(f"{(b + fptr*256):08d}: ", end='')
        for i in range(b, b + 8):
            if i >= len(data): continue
            if numbase == 16:
                s = '00' + hex(data[i])[2:]
                print(f"{s[-2:]} ", end='')
            else:
                print(f"{data[i]:03d} ", end='')
            if 31 < data[i] < 127:       # unprintable character?
                asc += chr(data[i])
            else:
                asc += '.'
        print(asc)
    print()


def edit_file() -> None:
    """Change a byte in the file and save it."""
    inp = input("Address of byte to change: ").strip()
    try:
        addr = int(inp, numbase)    # byte to change
    except ValueError:
        print("Invalid address!")
        return
    inp = input("New value of byte: ").strip()
    try:
        value = int(inp, numbase)   # new byte value
    except ValueError:
        print("Invalid number!")
        return
    if addr < 0 or addr > filesize: return  # valid address?
    with open(file, 'rb+') as f:
        f.seek(addr)                        # goto byte
        f.write(int.to_bytes(value, 1))      # write byte


def jump_to_location() -> int:
    """Goto a location - useful for navigating large files."""
    inp = input(f"Jump to location: ").strip()
    try:
        addr = int(inp, numbase)    # byte to change
    except ValueError:
        print("Invalid address!")
        return 0
    if addr > filesize: return 0
    return addr // 256      # new value for fptr


# ================ MAIN ================
os.system('cls') if os.name == 'nt' else os.system('clear')     # clear screen

folder = select_folder()
file = select_file('*')
filesize = os.path.getsize(file)
numbase = 16 if input("Use (H)ex or (D)ecimal? ").upper() == 'H' else 10
fptr = 0                        # file pointer, current data chunk
inp = ''
while inp != 'Q':
    print()
    data = read_file()                          # read chunk of file
    show_file()                                 # show data
    inp = input("(J)ump, (N)ext, (B)ack (E)dit, (Q)uit: ").upper()
    if inp == 'N' and ((fptr + 1) * 256) < filesize: fptr += 1   # next chunk
    if inp == 'B' and fptr > 0: fptr -= 1       # previous chunk
    if inp == 'E': edit_file()
    if inp == 'J': fptr = jump_to_location()           # handy for big files
