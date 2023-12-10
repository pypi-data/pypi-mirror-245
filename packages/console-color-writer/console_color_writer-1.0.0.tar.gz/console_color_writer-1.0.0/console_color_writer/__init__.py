'''
Black: \033[30m
Red: \033[31m
Green: \033[32m
Yellow: \033[33m
Blue: \033[34m
Magenta: \033[35m
Cyan: \033[36m
White: \033[37m
'''


def print_red(str1,str2 = ''):
    print(f"\033[1;31m {str1} \033[0m {str2}")
def print_green(str1,str2 = ''):
    print(f"\033[1;32m {str1} \033[0m {str2}")
def print_yellow(str1,str2 = ''):
    print(f"\033[1;33m {str1} \033[0m {str2}")
def print_cyan(str1,str2 = ''):
    print(f"\033[1;36m {str1} \033[0m {str2}")
def print_gray(str1,str2 = ''): 
    print(f"\033[1;34m {str1} \033[0m {str2}")
def print_magenta(str1,str2 = ''):
    print(f"\033[1;35m {str1} \033[0m {str2}")
def print_white(str1,str2 = ''):
    print(f"\033[1;37m {str1} \033[0m {str2}")

    
def print_red_tag(str1,str2 = ''):
    print(f"\033[1;31;40m {str1} \033[0m {str2}")
def print_green_tag(str1,str2 = ''):
    print(f"\033[1;32;40m {str1} \033[0m {str2}")
def print_yellow_tag(str1,str2 = ''):
    print(f"\033[1;33;40m {str1} \033[0m {str2}")
def print_cyan_tag(str1,str2 = ''):
    print(f"\033[1;36;40m {str1} \033[0m {str2}")
def print_gray_tag(str1,str2 = ''): 
    print(f"\033[1;34;40m {str1} \033[0m {str2}")
def print_magenta_tag(str1,str2 = ''):
    print(f"\033[1;35;40m {str1} \033[0m {str2}")
def print_white_tag(str1,str2 = ''):
    print(f"\033[1;37;40m {str1} \033[0m {str2}")
    
