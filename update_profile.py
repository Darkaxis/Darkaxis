"""Update README.md with live GitHub stats in an ANSI terminal block.

Runs daily via GitHub Actions. Stdlib only, no dependencies.
"""
import json
import os
import re
import urllib.request
from datetime import datetime, timezone

USER = "Darkaxis"
W = 60  # padding for left block

ART = r"""
                                                           
                                                           
                                                           
                                                           
                 ###                   ###                 
                   ###               ###                   
                    ####           ####                    
                     ####         ####                     
                     ####         ####                     
                     ###           ###                     
   #######           ###           ###           ########  
       ######        #####       #####        ######       
         ######   ###########  ##########   ######         
           ################## ##################           
             #################################             
              ##      ####### #######       #              
                    ### ##### ##### ###                    
                  #######################                  
                    ###### ##### ######                    
                      ###############                      
                       #############                       
                        ###########                        
                         #########                         
                         #### ####                         
                          ### ####                         
                          ### ###                          
                          ### ###                          
                           ##  #                           
                                                           
                                                           
                                                           
                                                           
"""

# two tokens by design: the Actions GITHUB_TOKEN yields the contribution-style
# commit count (public + private activity), while a PAT (ACCESS_TOKEN secret)
# sees private repos for the repo list and LOC walk. Either falls back to the other.
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("ACCESS_TOKEN") or ""
PRIV_TOKEN = os.environ.get("ACCESS_TOKEN") or TOKEN


def gh(url, payload=None, token=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Authorization": f"Bearer {token or TOKEN}", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req) as r:
        return r.status, json.loads(r.read() or "{}")


def graphql(query, variables=None, token=None):
    _, resp = gh("https://api.github.com/graphql", {"query": query, "variables": variables or {}}, token)
    if resp.get("errors"):
        raise RuntimeError(resp["errors"])
    return resp["data"]


def fetch_stats():
    # Using 2021 as a safe default for when the account was joined
    joined_year = 2021
    yr_aliases = "\n".join(
        f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y + 1}-01-01T00:00:00Z")'
        " { totalCommitContributions restrictedContributionsCount }"
        for y in range(joined_year, datetime.now(timezone.utc).year + 1)
    )
    contrib = graphql(f'query {{ user(login: "{USER}") {{ {yr_aliases} }} }}')["user"]
    commits = sum(
        v["totalCommitContributions"] + v["restrictedContributionsCount"]
        for v in contrib.values()
    )
    u = graphql(f"""
    query {{
      user(login: "{USER}") {{
        id
        followers {{ totalCount }}
        repositories(first: 100, ownerAffiliations: OWNER) {{
          totalCount
          nodes {{ name stargazerCount isFork }}
        }}
        repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, PULL_REQUEST, REPOSITORY]) {{
          totalCount
        }}
      }}
    }}""", token=PRIV_TOKEN)["user"]
    stats = {
        "followers": u["followers"]["totalCount"],
        "repos": u["repositories"]["totalCount"],
        "contributed": u["repositoriesContributedTo"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in u["repositories"]["nodes"]),
        "commits": commits,
    }
    stats.update(loc([n["name"] for n in u["repositories"]["nodes"] if not n["isFork"]], u["id"]))
    return stats


LOC_QUERY = """
query($owner: String!, $name: String!, $id: ID!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    defaultBranchRef { target { ... on Commit {
      history(first: 100, author: {id: $id}, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { additions deletions }
      }
    } } }
  }
}"""


def loc(repo_names, user_id):
    add = rem = 0
    for name in repo_names:
        cursor = None
        try:
            while True:
                ref = graphql(LOC_QUERY, {"owner": USER, "name": name, "id": user_id, "cursor": cursor}, token=PRIV_TOKEN)["repository"]["defaultBranchRef"]
                if ref is None:
                    break
                h = ref["target"]["history"]
                add += sum(n["additions"] for n in h["nodes"])
                rem += sum(n["deletions"] for n in h["nodes"])
                if not h["pageInfo"]["hasNextPage"]:
                    break
                cursor = h["pageInfo"]["endCursor"]
        except Exception as e:
            print(f"loc {name}: {e}")
    return {"loc_add": add, "loc_del": rem, "loc": add - rem}


def generate_ansi(stats):
    esc = chr(27)
    gray = f"{esc}[38;5;244m"
    teal = f"{esc}[38;5;38m"
    orange = f"{esc}[38;5;208m"
    white = f"{esc}[38;5;255m"
    green = f"{esc}[38;5;46m"
    red = f"{esc}[38;5;196m"
    reset = f"{esc}[0m"

    n = lambda x: f"{x:,}"

    info = [
        f"{teal}aubie@rhodes-island {gray}------------------------------------------",
        "",
        f"{orange}OS:{gray} ........................................... {white}Windows, Linux",
        f"{orange}Role:{gray} .............................. {white}Full Stack Web Developer, Pentester",
        f"{orange}Education:{gray} ........................ {white}Bukidnon State University",
        f"{orange}Stack.Backend:{gray} ......................... {white}Node.js, Laravel, PHP",
        f"{orange}Stack.Frontend:{gray} ......... {white}Next.js, React, Vite, Inertia.js",
        f"{orange}Security.Focus:{gray} ... {white}Pen Testing, Vulnerability Research",
        f"{orange}Security.Record:{gray} ..................... {white}Hack4Gov 2025 Finals",
        "",
        f"{teal}- Contact & Links {gray}============================================",
        f"{orange}Email:{gray} ........................... {white}hallazgoaubie@gmail.com",
        f"{orange}LinkedIn:{gray} .... {white}linkedin.com/in/aubie-bryne-5a25763aa",
        f"{orange}Portfolio:{gray} ....................................... {white}daraxis.tech",
        "",
        f"{teal}- GitHub Stats {gray}===============================================",
        f"{orange}Repos:{gray} .. {white}{stats['repos']} {gray}{{{white}Contributed: {stats['contributed']}{gray}}} | {orange}Stars:{gray} .. {teal}{n(stats['stars'])}",
        f"{orange}Commits:{gray} ....... {white}{n(stats['commits'])} | {orange}Followers:{gray} ...... {white}{n(stats['followers'])}",
        f"{orange}Lines of Code:{white} {n(stats['loc'])} {gray}( {green}{n(stats['loc_add'])}++{gray}, {red}{n(stats['loc_del'])}-- {gray})"
    ]

    ascii_lines = ART.strip("\n").split("\n")
    out = ["````ansi"]
    for i in range(max(len(ascii_lines), len(info))):
        left = ascii_lines[i] if i < len(ascii_lines) else ""
        left = left.ljust(W)
        right = info[i] if i < len(info) else ""
        out.append(f"{gray}{left}  {right}{reset}")
    out.append("````")
    return "\n".join(out)


if __name__ == "__main__":
    # Ensure tokens are available
    if not TOKEN:
        print("Skipping real fetch due to missing token, using dummy data for demonstration.")
        stats = {
            "followers": 24, "repos": 30, "contributed": 5, "stars": 128, 
            "commits": 542, "loc": 124567, "loc_add": 102456, "loc_del": 22111
        }
    else:
        stats = fetch_stats()

    ansi_block = generate_ansi(stats)

    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    # Replace the content between <!-- START_ANSI --> and <!-- END_ANSI -->
    pattern = r"<!-- START_ANSI -->.*?<!-- END_ANSI -->"
    replacement = f"<!-- START_ANSI -->\n{ansi_block}\n<!-- END_ANSI -->"
    
    new_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("Updated README.md with latest stats.")
