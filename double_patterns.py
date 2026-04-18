from colorama import Fore

patterns = {
    "Bullish Engulfing": [
        f'                        ',
        f'                {Fore.GREEN}║{Fore.RESET}            ',
        f'      {Fore.RED}║{Fore.RESET}     {Fore.GREEN}|███████|{Fore.RESET}        ',
        f'  {Fore.RED}|███████|{Fore.RESET} {Fore.GREEN}|███████|{Fore.RESET}        ',
        f'  {Fore.RED}|███████|{Fore.RESET} {Fore.GREEN}|███████|{Fore.RESET}        ',
        f'  {Fore.RED}|███████|{Fore.RESET} {Fore.GREEN}|███████|{Fore.RESET}        ',
        f'  {Fore.RED}|███████|{Fore.RESET} {Fore.GREEN}|███████|{Fore.RESET}        ',
        f'      {Fore.RED}║{Fore.RESET}     {Fore.GREEN}|███████|{Fore.RESET}        ',
        f'                {Fore.GREEN}║{Fore.RESET}            ',
        f'                        '
    ],
    "Bearish Engulfing": [
        f'                        ',
        f'                {Fore.RED}║{Fore.RESET}            ',
        f'      {Fore.GREEN}║{Fore.RESET}     {Fore.RED}|███████|{Fore.RESET}        ',
        f'  {Fore.GREEN}|███████|{Fore.RESET} {Fore.RED}|███████|{Fore.RESET}        ',
        f'  {Fore.GREEN}|███████|{Fore.RESET} {Fore.RED}|███████|{Fore.RESET}        ',
        f'  {Fore.GREEN}|███████|{Fore.RESET} {Fore.RED}|███████|{Fore.RESET}        ',
        f'  {Fore.GREEN}|███████|{Fore.RESET} {Fore.RED}|███████|{Fore.RESET}        ',
        f'      {Fore.GREEN}║{Fore.RESET}     {Fore.RED}|███████|{Fore.RESET}        ',
        f'                {Fore.RED}║{Fore.RESET}            ',
        f'                        '
    ]
}
