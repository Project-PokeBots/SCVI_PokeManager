from backend import *
import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 4, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (33, 33, 33), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (48, 48, 48), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200), category=dpg.mvThemeCat_Core)

with dpg.theme() as disabled_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (100, 100, 100), category=dpg.mvThemeCat_Core)


def main_window_setup():
    dpg.create_viewport(title="SCVI PokeManager", x_pos=0, y_pos=0, width=750, height=373, resizable=False)

    with dpg.window(pos=[0, 0], autosize=True, no_collapse=True, no_resize=True, no_close=True, no_move=True, no_title_bar=True) as main_window:

        with dpg.group(horizontal=True):
            with dpg.group():
                with dpg.child_window(width=500, height=325, tag="logging_window") as log_window:
                    dpg.add_text("Logging Initialized\n")

            with dpg.child_window(autosize_x=True, height=325):
                with dpg.group():
                    with dpg.child_window(height=203):
                        dpg.add_spacer(height=5)
                        dpg.add_text(default_value=" Settings")
                        dpg.add_spacer(height=5)
                        dpg.add_separator()
                        dpg.add_spacer(height=5)
                        dpg.add_input_text(label="Switch IP", width=130, default_value="192.168.1.10", tag="switch_ip")
                        dpg.add_input_text(label="Switch Port", width=130, default_value="6000", tag="switch_port")
                        dpg.add_button(label="Connect", width=-1, height=30, callback=backend_connect)

                    dpg.add_separator()
                    dpg.add_spacer()

                    with dpg.group(horizontal=True):
                        dpg.add_button(label="-", callback=lambda: dpg.set_value("boxnumber", dpg.get_value("boxnumber") - 1 if dpg.get_value("boxnumber") > 1 else 1))
                        dpg.add_drag_int(label="##boxnumber", width=100, clamped=True, min_value=1, max_value=31, default_value=1, tag="boxnumber")
                        dpg.add_button(label="+", callback=lambda: dpg.set_value("boxnumber", dpg.get_value("boxnumber") + 1 if dpg.get_value("boxnumber") < 31 else 31))
                        dpg.add_text(default_value="Box")

                    with dpg.group(horizontal=True):
                        dpg.add_button(label="-", callback=lambda: dpg.set_value("posInBox", dpg.get_value("posInBox") - 1 if dpg.get_value("posInBox") > 1 else 1))
                        dpg.add_drag_int(label="##posInBox", width=100, clamped=True, min_value=1, max_value=30, default_value=1, tag="posInBox")
                        dpg.add_button(label="+" ,callback=lambda: dpg.set_value("posInBox", dpg.get_value("posInBox") + 1 if dpg.get_value("posInBox") < 30 else 30))
                        dpg.add_text(default_value="Slot")

                    dpg.add_button(label="Dump", width=-1, height=30, callback=backend_dump)
                    dpg.add_button(label="Inject", width=-1, height=30, callback=lambda: dpg.show_item("file_dialog_id"))

    with dpg.file_dialog(directory_selector=False, show=False, callback=backend_inject, cancel_callback=None, id="file_dialog_id", width=724, height=313, modal=True) as filepicker:
        try:
            dpg.set_item_pos(filepicker, [0, 0])
        except:
            pass
        dpg.add_file_extension("All pkx {.ek8,.pk8,.eb8,.pb8,.ek9,.pk9}")
        dpg.add_file_extension("SWSH (ek8/pk8){.ek8,.pk8}")
        dpg.add_file_extension("BDSP (eb8/pb8){.eb8,.pb8}")
        dpg.add_file_extension("SCVI (ek9/pk9){.ek9,.pk9}")

    dpg.bind_theme(global_theme)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(window=main_window, value=True)
    dpg.start_dearpygui()
    dpg.destroy_context()


main_window_setup()
