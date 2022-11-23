import asyncio
import threading
import traceback
import re
import random
import string
import dearpygui.dearpygui as dpg
from px8parse import *
from socketSwitch import *

socketSwitch = SocketConnection()

pk_config = {
    "offset": "0x42FD510 0xA90 0x9B0 0x0",
    "box_array": 0x158,
    "pk_size": 344
}

def dpg_callback(sender: bool = False, app_data: bool = False, user_data: bool = False):
    def decorator(function):
        def wrapper(sender_var=None, app_data_var=None, user_data_var=None, *args, **kwargs):
            args = list(args)
            if user_data:
                args.insert(0, user_data_var)
            if app_data:
                args.insert(0, app_data_var)
            if sender:
                args.insert(0, sender_var)
            args = tuple(args)

            def run(function):
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(function(*args, **kwargs))
                    loop.close()
                except Exception:
                    traceback.print_exc()
            threading.Thread(target=run, args=(function,), daemon=True).start()
        return wrapper
    return decorator


@dpg_callback(sender=True, app_data=True, user_data=True)
async def backend_connect(sender, app_data, user_data):
    switch_ip = dpg.get_value("switch_ip")
    switch_port = dpg.get_value("switch_port")
    if not re.match(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", switch_ip):
        return dpg.add_text(f"[!] {switch_ip} is not a valid IP.", parent="logging_window")

    dpg.add_text(f"Connecting to {switch_ip}", parent="logging_window")
    try:
        socketSwitch.setConnection(switch_ip, switch_port)
        socketSwitch.connect()
    except socket.error:
        dpg.add_text(f"[!] Unable to connect to {switch_ip}:{switch_port}.", parent="logging_window")
    print(sender, app_data, user_data)


@dpg_callback(sender=True, app_data=True, user_data=True)
async def backend_dump(sender, app_data, user_data):
    name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    pokemon = socketSwitch.recv(f"pointerPeek 344 {pk_config['offset']}")
    with open(f"{name}.ek9", "wb+") as writer:
        try:
            writer.write(bytes.fromhex(pokemon.decode("utf-8")))
            dpg.add_text(f"Dumped pokemon {dpg.get_value('posInBox')} from box {dpg.get_value('boxnumber')} to {name}.ek9.", parent="logging_window")
        except Exception as e:
            return dpg.add_text(f"[!] Dump failed.", parent="logging_window")
    with open(f"{name}.ek9", "rb") as reader:
        try:
            dpg.add_text(str(PX8(buf = reader.read())), parent="logging_window")
        except:
            pass
    print(sender, app_data, user_data)


@dpg_callback(sender=True, app_data=True, user_data=True)
async def backend_inject(sender, app_data, user_data):
    try:
        with open(app_data["file_name"], "rb") as f:
            pk = f.read().hex()
    except Exception as e:
        return dpg.add_text(f"[!] Unable to open file {e}", parent="logging_window")
    pokemon = socketSwitch.send(f"pointerPoke 0x{pk} {pk_config['offset']}")
    dpg.add_text(f"Injecting pokemon {dpg.get_value('posInBox')} from box {dpg.get_value('boxnumber')}", parent="logging_window")
    print(sender, app_data, user_data)
