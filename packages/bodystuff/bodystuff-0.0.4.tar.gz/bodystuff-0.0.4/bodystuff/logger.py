import colorama
import time

def log(message, **kwargs):
    args = []
    for key, value in kwargs.items():
        args.append(f"{colorama.Fore.LIGHTBLACK_EX}{key}={colorama.Fore.WHITE}{value}")
    print(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.WHITE}{time.strftime('%H:%M:%S')}{colorama.Fore.LIGHTBLACK_EX}] {colorama.Fore.WHITE}{message} {' '.join(args)}")

def success(message, **kwargs):
    log(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.GREEN}success{colorama.Fore.LIGHTBLACK_EX}] {colorama.Fore.WHITE}{message}", **kwargs)

def info(message, **kwargs):
    log(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.BLUE}info{colorama.Fore.LIGHTBLACK_EX}] {colorama.Fore.WHITE}{message}", **kwargs)

def error(message, **kwargs):
    log(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.RED}error{colorama.Fore.LIGHTBLACK_EX}] {colorama.Fore.WHITE}{message}", **kwargs)