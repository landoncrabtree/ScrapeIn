import json, sys, optparse, argparse, re
from urllib.request import build_opener
from unidecode import unidecode
from colorama import Fore
import ssl
import yaml
ssl._create_default_https_context = ssl._create_unverified_context

class Formatter():
    def __init__(self, first, last, domain):
        self.first = first
        self.last = last
        self.domain = domain
    def format_email(self, format):
        format = format.replace('{first}', self.first)
        format = format.replace('{last}', self.last)
        format = format.replace('{f}', self.first[0:1])
        format = format.replace('{l}', self.last[0:1])
        while True:
            try:
                # first x letters
                fx = int(format.split('{f')[1][0])
                format = format.replace('{f'+str(fx)+'}', self.first[0:fx])
            except:
                try:
                    lx = int(format.split('{l')[1][0])
                    format = format.replace('{l'+str(lx)+'}', self.last[0:lx])
                except:
                    break
        return (format + '@' + self.domain).lower()

class LinkedIn():
    def __init__(self, args):
        with open("config.yml", "r") as file:
            try:
                data = yaml.safe_load(file)
                self.csrf_token = str(data['JSESSIONID'])
                self.session_id = str(data['li_at'])
            except yaml.YAMLError as e:
                print(e)
                exit()
        # Set args
        self.company_id = args.COMPANY
        self.domain = args.DOMAIN
        self.format = args.format
        self.outfile = args.output
        self.keyword = args.keyword
        # Set cookies
        self.li_at = "li_at=" + self.session_id
        self.JSESSIONID = "JSESSIONID=" + self.csrf_token
        # Set other
        self.current = 0
        self.last_page = False
        self.emails = []
        self.req = build_opener()
        self.req.addheaders.append(('csrf-token', self.csrf_token))
        self.req.addheaders.append(('Cookie', self.li_at + ';' + self.JSESSIONID))
        self.req.addheaders.append(('x-restli-protocol-version', '2.0.0'))
    def get_employees(self):
        if self.keyword == None:
            url = f"https://www.linkedin.com/voyager/api/search/blended?count=49&origin=OTHER&queryContext=List(spellCorrectionEnabled-%3Etrue,crelatedSearchesEnabled-%3Etrue,kcardTypes-%3EPROFILE%7CCOMPANY)&q=all&filters=List(currentCompany-%3E{self.company_id},resultType-%3EPEOPLE)&start={str(self.current)}"
        else:
            self.keyword = self.keyword.replace(" ", "%20")
            url = f"https://www.linkedin.com/voyager/api/search/blended?count=49&origin=OTHER&queryContext=List(spellCorrectionEnabled-%3Etrue,crelatedSearchesEnabled-%3Etrue,kcardTypes-%3EPROFILE%7CCOMPANY)&q=all&filters=List(currentCompany-%3E{self.company_id},resultType-%3EPEOPLE)&keywords={str(self.keyword)}&start={str(self.current)}"
        response = self.req.open(url)

        data = json.load(response)
        data = data["elements"][0]
        data = data["elements"]

        if len(data) < 49:
            self.last_page = True

        for employee in data:
            employee = employee["image"]
            employee = employee["attributes"]
            employee = employee[0]
            employee = employee["miniProfile"]
            fname = employee["firstName"]
            lname = employee["lastName"]
            fname = fname.replace(' ', '')
            lname = lname.replace(' ', '')
            if fname == "" or lname == "":
                continue
            f = Formatter(fname, lname, self.domain)
            self.emails.append(f.format_email(self.format))

    def write_emails(self):
        print("Found " + str(len(self.emails)) + " emails.")
        with open(self.outfile, 'w+') as f:
            for email in self.emails:
                f.write(email + "\n")
        print("Wrote emails to " + self.outfile)

def print_banner():
    print(f"{Fore.BLUE}")
    print("                     ██╗     ██╗███╗   ██╗██╗  ██╗███████╗██████╗ ██╗███╗   ██╗                      ")
    print("                     ██║     ██║████╗  ██║██║ ██╔╝██╔════╝██╔══██╗██║████╗  ██║                      ")
    print("                     ██║     ██║██╔██╗ ██║█████╔╝ █████╗  ██║  ██║██║██╔██╗ ██║                      ")
    print("                     ██║     ██║██║╚██╗██║██╔═██╗ ██╔══╝  ██║  ██║██║██║╚██╗██║                      ")
    print("                     ███████╗██║██║ ╚████║██║  ██╗███████╗██████╔╝██║██║ ╚████║                      ")
    print("                     ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═══╝                      ")
    print(f"{Fore.GREEN}")
    print("███████╗███╗   ███╗ █████╗ ██╗██╗         ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗    ")
    print("██╔════╝████╗ ████║██╔══██╗██║██║         ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗   ")
    print("█████╗  ██╔████╔██║███████║██║██║         ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝   ")
    print("██╔══╝  ██║╚██╔╝██║██╔══██║██║██║         ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗   ")
    print("███████╗██║ ╚═╝ ██║██║  ██║██║███████╗    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║   ")
    print("╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝   ")
    print(f"{Fore.RESET}")
    print(f"{Fore.RED}Made by Landon Crabtree.")
    print(f"{Fore.YELLOW}https://git.landon.pw/r/linkedin-scraper")
    print(f"{Fore.RESET}")
                                                                                                  

def main(parser):
    print_banner()
    args = parser.parse_args()
    li = LinkedIn(args)
    
    print(f"{Fore.GREEN}Scraping employees at {args.DOMAIN}...{Fore.RESET}")
    if args.keyword:
        print(f"{Fore.GREEN}Using keyword {args.keyword}...{Fore.RESET}")
    
    while (not li.last_page):
        li.get_employees()
        li.current += 49
    
    li.write_emails()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('COMPANY', help='Company ID')
    parser.add_argument('DOMAIN',help='Domain to be used in email address')
    parser.add_argument("-f", "--format", default='{first}.{last}', help="Format for the email address")
    parser.add_argument("-o", "--output", default='output.txt', help="Filename to write emails to")
    parser.add_argument("-k", "--keyword", default=None, help="Specify a keyword to narrow down the search")
    main(parser)
                                                          









creds='''AAMS
ACA
ADPA
AIF
AWMA
CAIA
CAP
CDFA
CEP
CFA
CFP
ChFC
CIMA
CLU
CPA
CMA
CMM
CMP
CDFA
CPWA
CRPC
CRPS
CTP
CWS
Jr.
MBA
M.A.
RICP
Sr.
WMS'''.split('\n')

# wip to port over.
def format_name(orig):
    orig = unidecode(orig)
    m = re.match(r'\s*(?:(?:(?:[\x80-\xff]|\)(?:[Rr]|[Tt][Mm])\()?(?:%s),?)+|[^,]+,)*\s*([A-Za-z \-\.\'\(\)]+)\s*'%('|'.join([x[::-1] for x in creds])), orig[::-1])
    if not m:
        print('unexpected format for %s' % orig)
    name = m.group(1)[::-1]

    # for now, remove
    ## paren content
    ## initials (only if -f, -l not specified)
    ## all non local email chars
    final = re.subn(r'(\(.*\)%s|[-\'\.,\\])' % (r'|[A-Z]\.' if (not args.abbrevF and not args.abbrevL) else ''), '', name)[0].lower().split(' ')
    email = '.'.join([f for f in final if len(f)>0]) + '@' + domain
    #print('%50s -> %40s -> %50s -> %40s'%(orig,name,final,email))
    
    return email
