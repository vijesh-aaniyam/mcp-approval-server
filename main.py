# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# main.py
from fastapi import FastAPI
from tools.approval import router

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


app = FastAPI(title="MCP Approval Server")
app.include_router(router)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
