NAME
        main_frame/main.py - the template of tool

SYNOPSIS
        python3 main_frame/main.py -h
        python3 main_frame/main.py --help
        python3 main_frame/main.py -v
        python3 main_frame/main.py --version
        python3 main_frame/main.py [-c config_file] [-p profile_file] [-m] [-s] [-t]

        (See the OPTIONS section for alternate option syntax with long option names.)

DESCRIPTION
        main_frame/main.py is a program, include the mail system, scheduler, self-profile. 

COMMANDS
        In the following descriptions, ^X means control-x.

        ^X: running in front, close the program

OPTIONS
        Command line options are described below. 

        -h or --help
            show the help info

        -v or --version
            show the version info

        -c config_name or --config config_name
            input the config name, it's format like config/config_template.conf

        -p profile_file or --cProfile profile_file
            open profile, output to the profile_file and the console

        -m or --mail
            open the mail system. you should set mail variable(user, password, host, to) in config/render.yml

            ~~~
                mail:
                    user: xx
                    password: xx
                    host: xx
                    to: xx
            ~~~

        -s or --scheduler
            open the scheduler. you can config the scheduler in scheduler.json.

        -t or --test
            test flag. we can pass some process when test



ENVIRONMENT VARIABLES