import asyncio
import threading
import traceback

import dearpygui.dearpygui as dpg

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
    text = f"Connecting to {switch_ip}"
    dpg.add_text(text, parent="logging_window")
    print(sender, app_data, user_data)


@dpg_callback(sender=True, app_data=True, user_data=True)
async def backend_dump(sender, app_data, user_data):
    mytext = "AAAAAA\nBBBBBBBB\nCCCCCCCC\n"
    mytext += f"dumping number {dpg.get_value('posInBox')} from box 1"
    dpg.add_text(mytext, parent="logging_window")


@dpg_callback(sender=True, app_data=True, user_data=True)
async def backend_inject(sender, app_data, user_data):
    dpg.add_text(f"Injecting into number {dpg.get_value('posInBox')} from box 1", parent="logging_window")
