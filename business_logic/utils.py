import hashlib


def print_api_title() -> None:
    server_title = """
 _____  ________      ________ _      ____  _____  ______ _____  
|  __ \|  ____\ \    / /  ____| |    / __ \|  __ \|  ____|  __ \ 
| |  | | |__   \ \  / /| |__  | |   | |  | | |__) | |__  | |__) |
| |  | |  __|   \ \/ / |  __| | |   | |  | |  ___/|  __| |  _  / 
| |__| | |____   \  /  | |____| |___| |__| | |    | |____| | \ \ 
|_____/|______|   \/   |______|______\____/|_|    |______|_|  \_\ 

                                                                                                
██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
██║  ██║███████║███████╗███████║██████╔╝██║   ██║███████║██████╔╝██║  ██║
██║  ██║██╔══██║╚════██║██╔══██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
██████╔╝██║  ██║███████║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  
    """
    print(server_title)


def hash_string_value(value: str) -> str:
    return str(hashlib.md5(value.encode("utf-8")).hexdigest())
