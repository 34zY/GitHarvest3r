import requests, sys, time, argparse

class style():
        BLACK_BG = "\033[40m"
        RED_BG = "\033[41m"
        GREEN_BG = "\033[42m"
        YELLOW_BG = "\033[43m"
        BLUE_BG = "\033[44m"
        MAGENTA_BG = "\033[45m"
        CYAN_BG = "\033[46m"
        WHITE_BG = "\033[47m"
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        UNDERLINE = '\033[4m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
        CL_BEFORE = '\r\x1b[2K'

        
STATUS_OK = style.GREEN + '[*] ' + style.RESET
STATUS_FOUND = style.YELLOW + ' > ' + style.RESET
STATUS_ERR = style.RED + '[!] ' +style.RESET
STATUS_LOAD = style.BOLD + style.YELLOW + '[~] ' +style.RESET

USER = 'USER-1337' # SET YOUR USERNAME 
TOKEN = '' # USE YOUR BASIC GITHUB TOKEN 

def Error_not_found():
        return STATUS_ERR + " No exploit found!"

def banner():
        return """
   ╔═╗┬┌┬┐ ╦ ╦┌─┐┬─┐┬  ┬┌─┐┌─┐┌┬┐┌─┐┬─┐
   ║ ╦│ │  ╠═╣├─┤├┬┘└┐┌┘├┤ └─┐ │ ├┤ ├┬┘
   ╚═╝┴ ┴  ╩ ╩┴ ┴┴└─ └┘ └─┘└─┘ ┴ └─┘┴└─
     Tool to gather exploit on github
                 @34zY
                 """

def main(STATUS_ERR,STATUS_FOUND,STATUS_OK, args, USER, TOKEN):

        
        # CVE-2017-5637 NO
        # CVE-2017-5638 OK
        CVE_ID = args.search
        print(STATUS_LOAD + "Searching exploit for " + CVE_ID + " ...", end="\n\n")
        time.sleep(1)

        url_query    = f'"{CVE_ID}" AND "exploit" in:name in:description in:readme OR "{CVE_ID}" AND "poc" in:name in:description in:readme OR "{CVE_ID}" AND "Proof of Concept" in:name in:description in:readme'
        http_header = {'Authorization': 'token %s' % TOKEN }
        
        url = f'https://api.github.com/search/repositories?q={url_query}'
        response = requests.get(url, headers=http_header)
 
        
        if response.status_code != 200:
                print(Error_not_found())
        
        else:   

                search_results = response.json()
                repositories = search_results['items']
                exploit_num = 0

                for repo in repositories:
                        exploit_num += 1
                        print(STATUS_FOUND + repo['html_url'])

                if exploit_num == 0:
                        print(Error_not_found())
                
                print('\n'+STATUS_OK + str(exploit_num) + ' exploits found!')


if __name__ == '__main__':

        print(style.BOLD + style.RED + banner() + style.RESET)
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--search", help = "CVE ID", required=True)
        args = parser.parse_args()
        main(STATUS_ERR,STATUS_FOUND,STATUS_OK, args, USER, TOKEN)
