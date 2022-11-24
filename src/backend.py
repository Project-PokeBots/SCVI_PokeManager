import asyncio, threading
import re, pathlib, traceback, datetime, sys
import dearpygui.dearpygui as dpg
from px8parse import *
from socketSwitch import *

socketSwitch = SocketConnection()

pk_config = {
    "offset": "0x42FD510 0xA90 0x9B0 0x0",
    "box_array": 0x158,
    "pk_size": 344
}

def assetLoader(relative_filePath):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = pathlib.Path(__file__).parent.absolute().parent.absolute()
    return pathlib.Path(base_path).joinpath("assets").joinpath(relative_filePath).absolute()

def log2window(message, window="logging_window"):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    dpg.add_text(f"[{now}] {message}\n", parent=window, wrap=480)
    dpg.set_y_scroll(window, 999999)

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
        log2window(f"{switch_ip} is not a valid IP.")
        return False

    log2window(f"Connecting to {switch_ip}:{switch_port}...")

    socketSwitch.setConnection(switch_ip, switch_port)
    ret = socketSwitch.connect()
    log2window(ret)


@dpg_callback(sender=True, app_data=True, user_data=True)
async def backend_dump(sender, app_data, user_data):
    boxNumber = dpg.get_value('boxnumber')
    positionInBox = dpg.get_value('posInBox')

    log2window(f"Dumping box {boxNumber} position {positionInBox}...")
    
    pokemon = socketSwitch.recv(f"pointerPeek 344 {pk_config['offset']}")
    pkmDataStr = str(PX8(buf = bytes.fromhex(pokemon.decode("utf-8"))))
    pkmName = pkmDataStr.split("\n")[0].split(" ")[0]

    if not pkmName or len(pkmName)<2:
        log2window(f"Unable to dump Pokemon.")
        return False

    filename = f"{boxNumber}_{positionInBox}_{pkmName.lower()}.ek9"
    with open(filename, "wb+") as writer:
        try:
            writer.write(bytes.fromhex(pokemon.decode("utf-8")))
            log2window(f"Dumped '{pkmName}' to {filename}")
        except:
            log2window(f"Unable to dump pokemon.")


@dpg_callback(sender=True, app_data=True, user_data=True)
async def backend_inject(sender, app_data, user_data):
    box = dpg.get_value('boxnumber')
    pos = dpg.get_value('posInBox')

    try:
        with open(app_data["file_name"], "rb") as f:
            pk = f.read().hex()
            log2window(f"Injecting {app_data['file_name']} into box {box} position {pos}...")
            pokemon = socketSwitch.send(f"pointerPoke 0x{pk} {pk_config['offset']}")
    except Exception:
        log2window(f"Unable to open file")
        return False
    log2window(f"Injected {app_data['file_name']}")
