from typing import NoReturn
import colorama
from pythonping import ping as ping_func
import sys
import socket

###########################
green = colorama.Fore.GREEN
red = colorama.Fore.RED
violet = '\033[95m'
reset_color = colorama.Style.RESET_ALL
###########################

def ping(host: str) -> list:
    """Ping host function"""
    response = ping_func(host, count=3)

    return response

def jitter(min_secs: float, max_secs: float) -> float:
    """Add jitter to a sleep call"""
    
    return round(((min_secs + max_secs) / 2), 2)

def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = [f'{reset_color}{feol}┌' + '─' * width + f'{feol}{reset_color}┐']
    count = 0
    for s in lines:
        a = ""
        count += 1
        if count == 2: a = "\t\t"
        res.append(f'{reset_color}{feol}│{reset_color}' + (s + ' ' * width)[:width] + f'{reset_color}{feol}{a}│{reset_color}')
    res.append(f'{reset_color}{feol}└' + f'{feol}─' * width + f'{feol}┘{reset_color}')
    return '\n'.join(res)

def main() -> NoReturn:
    if len(sys.argv) > 1: 
        IPs = [socket.gethostbyname(ip) for ip in sys.argv[1:]] #hosts to ping
    else: 
        print(f"{reset_color}No hosts to ping!{reset_color}")
        return None

    for host in IPs:
        ping_response = ping(host)

        if ping_response.stats_packets_returned == 0:
            status = f"{reset_color}{red}Offline{reset_color}"
        else:
            status = f"{reset_color}{green}OK{reset_color}"

        print(bordered(f"IP: {host} \n \
            Status: {status} \n \
            Speed: {ping_response.rtt_min_ms} ms \n \
            Packets Lost: {ping_response.stats_packets_lost}/3 packets \n \
            Jitter: {jitter(ping_response.rtt_min_ms, ping_response.rtt_max_ms)} ms"))

if __name__ == "__main__":
    main()
