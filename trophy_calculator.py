def calculate_trophies(stats: dict) -> list:
    trophies = []
    
    commits = stats.get("total_commits", 0)
    if commits >= 10000:
        trophies.append({"name": "Commits", "rank": "S", "title": "ARCHITECT OF CODE", "count": f"{commits//1000}k+"})
    elif commits >= 5000:
        trophies.append({"name": "Commits", "rank": "AAA", "title": "PRINCIPAL ENGINEER", "count": f"{commits//1000}k+"})
    elif commits >= 2000:
        trophies.append({"name": "Commits", "rank": "AA", "title": "STAFF DEVELOPER", "count": f"{commits//1000}k+"})
    elif commits >= 1000:
        trophies.append({"name": "Commits", "rank": "A", "title": "SENIOR CONTRIBUTOR", "count": f"{commits//1000}k+"})
    elif commits >= 500:
        trophies.append({"name": "Commits", "rank": "B", "title": "DEDICATED CODER", "count": commits})
    elif commits > 0:
        trophies.append({"name": "Commits", "rank": "C", "title": "EMERGING DEVELOPER", "count": commits})
    
    repos = stats.get("public_repos", 0)
    if repos >= 100:
        trophies.append({"name": "Repos", "rank": "S", "title": "DIGITAL ECOSYSTEM", "count": f"{repos}+"})
    elif repos >= 50:
        trophies.append({"name": "Repos", "rank": "AAA", "title": "SOLUTION ARCHITECT", "count": repos})
    elif repos >= 30:
        trophies.append({"name": "Repos", "rank": "AA", "title": "PRODUCT BUILDER", "count": repos})
    elif repos >= 20:
        trophies.append({"name": "Repos", "rank": "A", "title": "PROJECT CRAFTER", "count": repos})
    elif repos >= 10:
        trophies.append({"name": "Repos", "rank": "B", "title": "WORKSPACE OWNER", "count": repos})
    elif repos > 0:
        trophies.append({"name": "Repos", "rank": "C", "title": "INITIAL LAUNCH", "count": repos})
    
    followers = stats.get("followers", 0)
    if followers >= 1000:
        trophies.append({"name": "Followers", "rank": "S", "title": "INDUSTRY ICON", "count": f"{followers//1000}k+"})
    elif followers >= 500:
        trophies.append({"name": "Followers", "rank": "AAA", "title": "THOUGHT LEADER", "count": followers})
    elif followers >= 200:
        trophies.append({"name": "Followers", "rank": "AA", "title": "RISING INFLUENCE", "count": followers})
    elif followers >= 100:
        trophies.append({"name": "Followers", "rank": "A", "title": "COMMUNITY VOICE", "count": followers})
    elif followers >= 50:
        trophies.append({"name": "Followers", "rank": "B", "title": "GROWING NETWORK", "count": followers})
    elif followers > 0:
        trophies.append({"name": "Followers", "rank": "C", "title": "FIRST FOLLOWERS", "count": followers})
    
    stars = stats.get("total_stars", 0)
    if stars >= 1000:
        trophies.append({"name": "Stars", "rank": "S", "title": "OPEN SOURCE LEGEND", "count": f"{stars//1000}k+"})
    elif stars >= 500:
        trophies.append({"name": "Stars", "rank": "AAA", "title": "DEVELOPER FAVORITE", "count": stars})
    elif stars >= 200:
        trophies.append({"name": "Stars", "rank": "AA", "title": "QUALITY SHOWCASE", "count": stars})
    elif stars >= 100:
        trophies.append({"name": "Stars", "rank": "A", "title": "WELL CRAFTED", "count": stars})
    elif stars >= 50:
        trophies.append({"name": "Stars", "rank": "B", "title": "GAINING TRACTION", "count": stars})
    elif stars > 0:
        trophies.append({"name": "Stars", "rank": "C", "title": "FIRST RECOGNITION", "count": stars})
    
    issues = stats.get("total_issues", 0)
    if issues >= 1000:
        trophies.append({"name": "Issues", "rank": "S", "title": "QUALITY CHAMPION", "count": f"{issues//1000}k+"})
    elif issues >= 500:
        trophies.append({"name": "Issues", "rank": "AAA", "title": "BUG DETECTIVE", "count": issues})
    elif issues >= 200:
        trophies.append({"name": "Issues", "rank": "AA", "title": "PROBLEM SOLVER", "count": issues})
    elif issues >= 100:
        trophies.append({"name": "Issues", "rank": "A", "title": "FEEDBACK PIONEER", "count": issues})
    elif issues >= 50:
        trophies.append({"name": "Issues", "rank": "B", "title": "DETAIL ORIENTED", "count": issues})
    elif issues > 0:
        trophies.append({"name": "Issues", "rank": "C", "title": "FIRST REPORTS", "count": issues})
    
    prs = stats.get("total_prs", 0)
    if prs >= 1000:
        trophies.append({"name": "PRs", "rank": "S", "title": "COLLABORATION MASTER", "count": f"{prs//1000}k+"})
    elif prs >= 500:
        trophies.append({"name": "PRs", "rank": "AAA", "title": "TEAM CATALYST", "count": prs})
    elif prs >= 200:
        trophies.append({"name": "PRs", "rank": "AA", "title": "CODE INTEGRATOR", "count": prs})
    elif prs >= 100:
        trophies.append({"name": "PRs", "rank": "A", "title": "VALUABLE COLLABORATOR", "count": prs})
    elif prs >= 50:
        trophies.append({"name": "PRs", "rank": "B", "title": "ACTIVE CONTRIBUTOR", "count": prs})
    elif prs > 0:
        trophies.append({"name": "PRs", "rank": "C", "title": "FIRST CONTRIBUTION", "count": prs})
    
    gists = stats.get("public_gists", 0)
    if gists >= 100:
        trophies.append({"name": "Gists", "rank": "S", "title": "CODE CURATOR", "count": f"{gists}+"})
    elif gists >= 50:
        trophies.append({"name": "Gists", "rank": "AAA", "title": "SNIPPET ARCHITECT", "count": gists})
    elif gists >= 20:
        trophies.append({"name": "Gists", "rank": "AA", "title": "KNOWLEDGE SHARER", "count": gists})
    elif gists >= 10:
        trophies.append({"name": "Gists", "rank": "A", "title": "USEFUL SNIPPETS", "count": gists})
    elif gists >= 5:
        trophies.append({"name": "Gists", "rank": "B", "title": "CODE COLLECTOR", "count": gists})
    elif gists > 0:
        trophies.append({"name": "Gists", "rank": "C", "title": "FIRST SNIPPET", "count": gists})
    
    forks = stats.get("total_forks", 0)
    if forks >= 500:
        trophies.append({"name": "Forks", "rank": "S", "title": "DISTRIBUTION PIONEER", "count": f"{forks//100}k+"})
    elif forks >= 200:
        trophies.append({"name": "Forks", "rank": "AAA", "title": "WIDELY ADOPTED", "count": forks})
    elif forks >= 100:
        trophies.append({"name": "Forks", "rank": "AA", "title": "COMMUNITY DRIVEN", "count": forks})
    elif forks >= 50:
        trophies.append({"name": "Forks", "rank": "A", "title": "GROWING REACH", "count": forks})
    elif forks >= 20:
        trophies.append({"name": "Forks", "rank": "B", "title": "INSPIRING OTHERS", "count": forks})
    elif forks > 0:
        trophies.append({"name": "Forks", "rank": "C", "title": "FIRST FORK", "count": forks})
    
    sponsors = stats.get("sponsors", 0)
    if sponsors >= 100:
        trophies.append({"name": "Sponsors", "rank": "S", "title": "SUSTAINABILITY LEGEND", "count": f"{sponsors}+"})
    elif sponsors >= 50:
        trophies.append({"name": "Sponsors", "rank": "AAA", "title": "CREATOR ECONOMY", "count": sponsors})
    elif sponsors >= 20:
        trophies.append({"name": "Sponsors", "rank": "AA", "title": "COMMUNITY BACKED", "count": sponsors})
    elif sponsors >= 10:
        trophies.append({"name": "Sponsors", "rank": "A", "title": "SUPPORTED BUILDER", "count": sponsors})
    elif sponsors >= 5:
        trophies.append({"name": "Sponsors", "rank": "B", "title": "EARLY ADOPTER", "count": sponsors})
    elif sponsors > 0:
        trophies.append({"name": "Sponsors", "rank": "C", "title": "FIRST BACKER", "count": sponsors})
    
    return trophies