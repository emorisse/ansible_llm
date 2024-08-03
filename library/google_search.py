from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import requests
from bs4 import BeautifulSoup
import json

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        # query=dict(type='string', required=True)
        query=dict(required=True),
        headers=dict(required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        output=[]
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    result['output'].append(parse_search_results(google_search(module.params['query'])))
    result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def google_search(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_search_results(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    
    for result in soup.select('.tF2Cxc'):
        title_tag = result.select_one('h3')
        link_tag = result.select_one('.yuRUbf a')
        snippet_tag = result.select_one('.IsZvec')
        
        title = title_tag.get_text() if title_tag else ''
        link = link_tag['href'] if link_tag else ''
        snippet = snippet_tag.get_text(separator=' ') if snippet_tag else ''
        
        results.append({
            "title": title,
            "link": link,
            "snippet": snippet
        })
    
    return results


def parse_search_results_ori(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    for g in soup.find_all('div', class_='g'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text if g.find('h3') else ''
            snippet = g.find('span', class_='aCOpRe').text if g.find('span', class_='aCOpRe') else ''
            if not snippet:
                snippet = g.find('div', {'class': 'IsZvec'}).text if g.find('div', {'class': 'IsZvec'}) else ''
            results.append({"title": title, "link": link, "snippet": snippet})
    return results

def main():
    query = "Voodoo, Ltd. murder mystery"
    run_module()

if __name__ == "__main__":
    main()
