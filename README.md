# ScrapeIn
### OSINT gathering tool that allows you to compile a list of employee email addresses from a specific company via LinkedIn. Useful during the reconnaissance phase of a penetration test and can be used further to try and get initial access (ie: targeted phishing campaigns)

**This tool is for EDUCATIONAL purposes only.**

This tool is based off @Morganc3's <https://github.com/morganc3/LinkedInHarvester>. I cleaned up the code and added some vital features that were missing. 

## Features
* Collect employee email addresses en-masse from a specific company
* Custom address formating, such as {first}.{last} or {l}{first}
* Output email addresses to a text file
* Narrow down employee search results by keywords, such as "human resources" or "sales"

## Getting Started
1. `git clone https://github.com/landoncrabtree/ScrapeIn.git`
2. `cd ScrapeIn`
3. `pip install -r requirements.txt`
4. `python3 scrapein.py`

## Usage (basic)
### Finding Company ID
![search](https://i.imgur.com/fM7AIGa.png)
![searchbar](https://i.imgur.com/9DVkoSV.png)
And then where it says `currentCompany=["<ID>"]`

### Authorizing LinkedIn
In order to use LinkedIn search to its full capabilities, you must authenticate with a CSRF token and a session ID. These are stored as cookies.
![cookies](https://i.imgur.com/F5vCX09.png)
You are looking for `JSESSIONID` and `li_at`. These values will need to be pasted in the `config.yml`.

### Running the tool
```
$ scrapein.py <company_id> <domain>
$ python3 scrapein.py 12345 google.com
```

## Usage (advanced)
* -o|--output  : Filename or path to output
* -k|--keyword : Keyword to narrow results down by
* -f|--format  : Custom email address formatting string
```
$python3 scrapein.py <company_id> <domain> -o|--output -k|--keyword -f|--format
$ python3 scrapein.py 12345 google.com -o emails.txt -k 'human resources' -f '{l}-{first}'
```

## Email Address Formatting
One of the features this tool is the ability to format emails to virtually any format with some simple placeholders. It is recommended to use [Hunter.io](https://hunter.io) to figure out the company's email address formatting scheme.
Then, you can use the following placeholders in the `-f` argument:

```
{first} = first name
{last} = last name
{f} = first initial
{l} = last initial
{fx} = first x characters in first name (ie: {f3} )
{lx} = first x characters in last name (ie: {l3} )
```

![google](https://i.imgur.com/rg2CrF6.png)
```
-f {first}{last}
```

![meta](https://i.imgur.com/RgCW17q.png)
```
-f {last}
```

![microsoft](https://i.imgur.com/Ea9DsoA.png)
```
-f {last}{f}
```
