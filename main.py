from typing import NoReturn
import colorama
from pythonping import ping as ping_func
import sys
import socket

##### Color samples in variables #####
green = colorama.Fore.GREEN
red = colorama.Fore.RED
violet = '\033[95m'
reset_color = colorama.Style.RESET_ALL
######################################

def ping(host: str) -> list:
    """Ping host function"""

    return ping_func(host, count=3) # Ping the IP and return the result

def jitter(min_secs: float, max_secs: float) -> float:
    """Add jitter to a sleep call"""
    
    return round(((min_secs + max_secs) / 2), 2) # Calculate the arithmetic mean between the largest and smallest values, round to hundredths and return the result

def bordered(text: str, add: int = 0, rm: int = 0) -> str:
    """A function that creates a frame for text"""
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = [f'{reset_color}{violet}┌' + '─' * width + f'{violet}┐{reset_color}']
    count = 0
    for s in lines:
        count += 1
        if count == 2:
            res.append(f'{reset_color}{violet}│{reset_color}' + (s + ' ' * (width + (add - rm)))[:(width + (add - rm))] + f'{reset_color}{violet}│{reset_color}')
        else:
            res.append(f'{reset_color}{violet}│{reset_color}' + (s + ' ' * width)[:width] + f'{reset_color}{violet}│{reset_color}')
    res.append(f'{reset_color}{violet}└' + f'{violet}─' * width + f'{violet}┘{reset_color}')
    return '\n'.join(res)

def main() -> NoReturn:
    """Main function"""
    if len(sys.argv) > 1: 
        IPs = [socket.gethostbyname(ip) for ip in sys.argv[1:]] #hosts to ping
    else: 
        print(f"{reset_color}No hosts to ping!{reset_color}")
        return None

    for host in IPs:
        ping_response = ping(host) # Ping the ip and save it to a variable
        
        if ping_response.stats_packets_returned == 0: # Checking if the ip is available
            status = f"{reset_color}{red}Offline{reset_color}"
        else:
            status = f"{reset_color}{green}OK{reset_color}"

        print(bordered(f"IP: {host} \n \
            Status: {status} \n \
            Speed: {ping_response.rtt_min_ms} ms \n \
            Packets Lost: {ping_response.stats_packets_lost}/3 packets \n \
            Jitter: {jitter(ping_response.rtt_min_ms, ping_response.rtt_max_ms)} ms", add=13)) # Оutput the ping result

if __name__ == "__main__":
    main()
