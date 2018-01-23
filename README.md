# multi-process-launcher
A simple Python script to run a group of dependent commands together

# What the hell is this crap ?

A very basic Python script that takes `--cmd "/path/to/command arg1 --arg val2"` multiple time an fork them all.

If one commands die, the whole things die. If it gets stopped, it kills all children too.

It's aimed to be used a single file replacement for supervisord and other crap use to start multiple services in a docker container.

I know it's probably very bad code, feel free to PR...
