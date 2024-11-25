#!/bin/bash
######################################################################
#
#
#           ██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗
#           ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔════╝
#           ██████╔╝███████║███████╗███████║██████╔╝██║
#           ██╔══██╗██╔══██║╚════██║██╔══██║██╔══██╗██║
#           ██████╔╝██║  ██║███████║██║  ██║██║  ██║╚██████╗
#           ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝
#
#
######################################################################

set -o vi

HISTTIMEFORMAT="%F %T "

HISTCONTROL=ignoredups

HISTSIZE=2000

HISTFILESIZE=2000

alias tree='tree --dirsfirst -F'
alias dnf='sudo dnf'

# Set Escape to Caps Lock key
test -n "$DISPLAY" && setxkbmap -option caps:escape &>/dev/null

# private alias setup
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias m=more
alias tn=telnet
alias l='ls -alF'
alias la='ls -a'
alias lm='ls -al|more'
alias lh='ls -alh'
alias c=clear
alias h=history
alias ps='ps -w'
alias ldir='ls -al|grep ^d'

# private function setup
function find_largest_files() {
    du -h -x -s -- * | sort -r -h | head -20;
}

mkcdir ()
{
    mkdir -p -- "$1" &&
       cd -P -- "$1"
}

# custom by user
if [[ "$(id -u -n)" == "jbentley" ]];then
   alias ll='ls -lah'
fi
