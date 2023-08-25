# ______            _   _              ___    ____  _____ 
# | ___ \          | | | |            |_  |  / ___||  _  |
# | |_/ / ___ _ __ | |_| | ___ _   _    | | / /___  \ V / 
# | ___ \/ _ \ '_ \| __| |/ _ \ | | |   | | | ___ \ / _ \ 
# | |_/ /  __/ | | | |_| |  __/ |_| /\__/ / | \_/ || |_| |
# \____/ \___|_| |_|\__|_|\___|\__, \____/  \_____/\_____/
#                               __/ |                     
#                              |___/                      
#
# Qtile config file
#

import os
import re
import psutil
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401

@hook.subscribe.startup_once

def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])

def search():
    qtile.cmd_spawn("rofi -show drun")

def power():
    qtile.cmd_spawn("sh -c ~/.config/rofi/scripts/power")

mod = "mod4"
terminal = 'alacritty'     
# myBrowser = 'brave-browser'
myBrowser = 'firefox'
home = os.path.expanduser('~')

keys = [
    
    # Qtile Controls
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "o", lazy.layout.maximize()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    Key([mod, "shift"], "Return",
             lazy.spawn("dmenu_run -p 'Run: '"),
             desc='Run Launcher'
             ),

    Key([mod, "control"], "Return",
             lazy.spawn("rofi -show drun -theme solarized"),
             desc='Run Launcher'
             ),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    # Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    # Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
    Key([mod], "b",
             lazy.spawn(myBrowser),
             desc='Qutebrowser'
             ),
    Key([mod], "p", lazy.spawn("sh -c ~/.config/rofi/scripts/power"), desc='powermenu'),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-"), 
            desc="Lower Volume by 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+"), 
            desc="Raise Volume by 5%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master 1+ toggle"), 
            desc="Mute/Unmute Volume"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause player"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),
    # Key([mod2], "Print", lazy.spawn('xfce4-screenshooter')),
    # Key([mod2, "shift"], "Print", lazy.spawn('gnome-screenshot -i')),
    # Add key command for ScratchPad DropDown
    Key([mod], "0", lazy.group["scratchpad"].dropdown_toggle("term")),
    Key([mod], "F9", lazy.group["scratchpad"].dropdown_toggle("khal")),
    Key([mod], "F10", lazy.group["scratchpad"].dropdown_toggle("glow")),
    Key([mod, 'control'], 'f', lazy.window.toggle_fullscreen()),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),

    ])

# Append ScratchPad to Group List
groups.append(
    ScratchPad("scratchpad", [
        # define a dropdown terminal
        DropDown("term", terminal, opacity=0.8, height=0.5, width=0.80),
        # glow cheat sheet
        DropDown("glow", terminal + " -e glow /home/jbentley/OneDrive/Temp/Personal", opacity=0.8, height=0.5, width=0.80),
        # calendar
        DropDown('khal', terminal + " -e khal interactive", x=0.6785, width=0.32, height=0.997, opacity=0.8),
    ]),
)

layouts = [
    layout.MonadTall(),
    layout.MonadWide(),
    layout.Columns(border_focus_stack=['#d75f5f', '#8f3d3d'], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

colours = [["#080808", "#080808"], # Background
		   ["#FFFFFF", "#FFFFFF"], # Foreground
		   ["#ABB2BF", "#ABB2BF"], # Grey Colour
		   ["#E35374", "#E35374"],
		   ["#89CA78", "#89CA78"],
		   ["#F0C674", "#F0C674"],
		   ["#61AFEF", "#61AFEF"],
		   ["#D55FDE", "#D55FDE"],
		   ["#2BBAC5", "#2BBAC5"]]


prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

widget_defaults = dict(
	background = colours[0],
	foreground = colours[1],
	font = "SF Pro Text Regular",
	fontsize = 12,
	padding = 1,
)

extension_defaults = widget_defaults.copy()

widgets = [
	widget.Sep(
		foreground = colours[0],
		linewidth = 4,
	),
	widget.Image(
		filename = "~/.config/qtile/py.png",
		mouse_callbacks = {"Button1": lambda: qtile.cmd_spawn("rofi -show drun")},
		scale = True,
	),
	widget.Sep(
		foreground = colours[2],
		linewidth = 1,
		padding = 10,
	),
	widget.GroupBox(
		active = colours[4],
		inactive = colours[6],
		other_current_screen_border = colours[5],
		other_screen_border = colours[2],
		this_current_screen_border = colours[7],
		this_screen_border = colours[2],
		urgent_border = colours[3],
		urgent_text = colours[3],
		disable_drag = True,
		highlight_method = "text",
		invert_mouse_wheel = True,
		margin = 2,
		padding = 0,
		rounded = True,
		urgent_alert_method = "text",
	),
	widget.Sep(
		foreground = colours[2],
		linewidth = 1,
		padding = 10,
	),
	widget.CurrentLayout(
		foreground = colours[7],
		font = "SF Pro Text Semibold",
	),
	widget.Sep(
		foreground = colours[2],
		linewidth = 1,
		padding = 10,
	),
    widget.Prompt(),
	widget.WindowName(
		max_chars = 75,
	),
	widget.Systray(
		icon_size = 14,
		padding = 4,
	),
    widget.Sep(
		foreground = colours[2],
		linewidth = 1,
		padding = 10,
	),
	widget.TextBox(
		foreground = colours[4],
		font = "mononoki Nerd Font",
		fontsize = 14,
		padding = 0,
        text = " ",  
	),
    # widget.Net(
    #    interface = "wlp4s0",
    #    format = '{down} ↓↑ {up}',
    #    foreground = colours[3],
    #    padding = 5
    #),
    widget.NetGraph(graph_color = colours[4]),
    widget.Sep(
		foreground = colours[2],
		linewidth = 1,
		padding = 10,
	),
	widget.TextBox(
		foreground = colours[7],
		font = "mononoki Nerd Font",
		fontsize = 14,
		padding = 0,
        text = " ",  
	),
    widget.Volume(
        foreground = colours[7],
        padding = 5
    ),
    widget.Sep(
		foreground = colours[2],
		linewidth = 1,
		padding = 10,
	),
	widget.TextBox(
		foreground = colours[8],
		font = "mononoki Nerd Font",
		fontsize = 14,
		padding = 0,
		text = " ",
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(terminal + " -e khal interactive")},
	),
    widget.Clock(
		foreground = colours[8],
		format = "%a %b %d  %I:%M %P    ",
        mouse_callbacks={"Button1": lazy.group['scratchpad'].dropdown_toggle('khal')},
	),
	#widget.StockTicker(
	#	apikey = "AESKWL5CJVHHJKR5",
	#	url = "https://www.alphavantage.co/query?"
	#),
]

status_bar = lambda widgets: bar.Bar(widgets, 18, opacity=1.0)

screens = [Screen(top=status_bar(widgets), )]

# screens = [
#    Screen(
#        top=bar.Bar(
#            [
#                widget.Image(
#		            filename = "~/.config/qtile/py.png",
#		            mouse_callbacks = {"Button1": lambda: qtile.cmd_spawn("rofi -show drun")},
#		            scale = True,
#	            ),
#                widget.CurrentLayout(),
#                widget.GroupBox(),
#                widget.Prompt(),
#                widget.WindowName(),
#                widget.Chord(
#                    chords_colors={
#                        'launch': ("#ff0000", "#ffffff"),
#                    },
#                    name_transform=lambda name: name.upper(),
#                ),
#                # widget.TextBox("default config", name="default"),
#                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
#                widget.Systray(),
#                widget.NetGraph(),
#                # widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
#                widget.QuickExit(),
#            ],
#            24,
#        ),
#    ),
# ]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
