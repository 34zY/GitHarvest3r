import requests, re, sys, time, argparse
from bs4 import BeautifulSoup


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


def banner():
        return """
   ╔═╗┬┌┬┐ ╦ ╦┌─┐┬─┐┬  ┬┌─┐┌─┐┌┬┐┌─┐┬─┐
   ║ ╦│ │  ╠═╣├─┤├┬┘└┐┌┘├┤ └─┐ │ ├┤ ├┬┘
   ╚═╝┴ ┴  ╩ ╩┴ ┴┴└─ └┘ └─┘└─┘ ┴ └─┘┴└─
     Tool to gather exploit on github
                 @34zY
                 """

def main(STATUS_ERR,STATUS_FOUND,STATUS_OK, args):


        cookies = {
        '_gh_sess': '08EwjO1uVbp%2B79varEEmj2yvvV9HCEQAMlZFrzWxudftlHPOH582rs9ImKC7XzIHdryfGZ4PVRJOB%2F3oJYMfEVyJcCMhZWvpdU6GRNiZcjQZ1YgGv0EoDHd6NhX4sm5l21nmlLaQCWxXBsg7el6UAbzJhz0cswYM%2FFEw%2BcXLveYgj2HPvij7WHM%2B5DFeeaGJh5Q3iu%2Bu4W9Oj0dMdnHGkwMhfzzJ0EIyCbYl36T57Qj7cy4xmioitB8rEWIBD30yD%2FhRjTq7DpxREI%2F8mxOBdRM52q39JXpIXQ%3D%3D--KpRVdwx1%2B%2BavAvAc--pJHbOVsLKf3yfrMecflT2A%3D%3D',
        '_octo': 'GH1.1.548229103.1682616213',
        'logged_in': 'no',
        'preferred_color_mode': 'dark',
        }
        
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'If-None-Match': 'W/"722a5d2048a1cd6ead97816c21508a1b"',
        }
        
        # CVE-2017-5637 NO
        # CVE-2017-5638 OK
        CVE_ID = args.search
        print(STATUS_LOAD + "Searching exploit for " + CVE_ID + " ...")
        time.sleep(1)


        params = {
        'q': f'"{CVE_ID}" AND "exploit" in:name in:description in:readme OR "{CVE_ID}" AND "poc" in:name in:description in:readme OR "{CVE_ID} AND" "Proof of Concept" in:name in:description in:readme',
        'type': 'repositories',
        }
        
        response = requests.get('https://github.com/search', params=params, cookies=cookies, headers=headers)
        body = response.content.decode()        
        soup = BeautifulSoup(body, "html.parser")
        no_exploit = 't find any repositories matching'
        
        if no_exploit in body:
                print(STATUS_ERR + "No exploit found!")
        
        else:   
                exploit_number = soup.find_all("h3") # extract number of exploits
                exploit_num = str(exploit_number[1])
                parse_exploit_num = exploit_num.replace('<h3>','')
                parse_exploit_num = parse_exploit_num.replace('</h3>','')
                parse_exploit_num = parse_exploit_num.replace(' repository results','')
                parse_exploit_num = parse_exploit_num.replace('\n','')
                parse_exploit_num = parse_exploit_num.replace('    ','')
                print(STATUS_OK + parse_exploit_num + ' exploits found!')
        
                pattern_retrieve_link = r'&quot;url&quot;:&quot;https://github.com/(.*?)/(.*?)&quot;'
                links = re.findall(pattern_retrieve_link, body)
        
                for link in links:
                        print(STATUS_FOUND + "https://github.com/"+link[0]+"/"+link[1])


if __name__ == '__main__':

        print(style.BOLD + style.RED + banner() + style.RESET)
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--search", help = "CVE ID", required=True)
        args = parser.parse_args()
        main(STATUS_ERR,STATUS_FOUND,STATUS_OK, args)
