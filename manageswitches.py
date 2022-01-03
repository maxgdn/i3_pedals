import asyncio, evdev

from i3ipc import Connection
from evdev import InputDevice
from evdev import KeyEvent

#find values with evtest 
path1 = '/dev/input/event6'
path2 = '/dev/input/event23'

i3 = Connection()

pedal1 = InputDevice(path1)
pedal2 = InputDevice(path2)

pedal1.grab()
pedal2.grab()

async def print_events(device):
    async for event in device.async_read_loop():
        input_event = evdev.categorize(event)
        
        if(isinstance(input_event,KeyEvent)):
            if(input_event.keystate == 0):
                workspaces = i3.get_workspaces()
                tree = i3.get_tree()
                focused = tree.find_focused()
                target = focused.workspace()
                spaces = list(map(lambda x: x.name, workspaces)) 
                pos = spaces.index(target.name)
                cmd = 'workspace' 
                if(device.path == path1):
                    #left
                    #circular
                    #win = max(pos-1,0)
                    if(pos - 1 < 0):
                        win = len(spaces)-1
                    else:
                        win = pos - 1
                    i3.command(cmd+str(spaces[win]))
                if(device.path == path2):
                    #right
                    #circular
                    #win = min(pos+1, len(spaces)-1)
                    if(pos + 1 > (len(spaces)-1)):
                        win = 0
                    else:
                        win = pos + 1
                    i3.command(cmd+str(spaces[win]))
        
for device in pedal1, pedal2:
    asyncio.ensure_future(print_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()