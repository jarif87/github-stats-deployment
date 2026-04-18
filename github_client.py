import requests
from typing import Dict, List
import os
import re
from datetime import datetime, timedelta

class GitHubClient:
    def __init__(self, token: str | None = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Custom-GitHub-Dashboard"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token.strip()}"
            print(f"✓ Token loaded (length: {len(self.token.strip())})")
        self._cache = {}
        self._cache_expiry = {}
        self.cache_duration = timedelta(hours=1)

    def _is_cache_valid(self, cache_key: str) -> bool:
        if cache_key not in self._cache_expiry:
            return False
        return datetime.now() < self._cache_expiry[cache_key]

    def _set_cache(self, cache_key: str, data):
        self._cache[cache_key] = data
        self._cache_expiry[cache_key] = datetime.now() + self.cache_duration
        print(f"✓ Cached {cache_key} until {self._cache_expiry[cache_key].strftime('%Y-%m-%d %H:%M:%S')}")

    def get_user(self, username: str) -> Dict:
        cache_key = f"user_{username}"
        if cache_key in self._cache and self._is_cache_valid(cache_key):
            print(f"Using cached user data for {username}")
            return self._cache[cache_key]
        
        print(f"Fetching fresh user data for {username}")
        r = requests.get(f"https://api.github.com/users/{username}", headers=self.headers)
        r.raise_for_status()
        data = r.json()
        self._set_cache(cache_key, data)
        return data

    def get_repos(self, username: str) -> List[Dict]:
        cache_key = f"repos_{username}"
        if cache_key in self._cache and self._is_cache_valid(cache_key):
            print(f"Using cached repos for {username}")
            return self._cache[cache_key]
        
        print(f"Fetching fresh repos for {username}")
        repos = []
        page = 1
        while True:
            r = requests.get(
                f"https://api.github.com/users/{username}/repos?per_page=100&page={page}",
                headers=self.headers,
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            if not data:
                break
            repos.extend(data)
            page += 1
            if page > 10:  # Safety limit
                break
        self._set_cache(cache_key, repos)
        return repos

    def get_top_languages(self, username: str, include_all: bool = True, max_repos: int = None) -> Dict[str, float]:
        cache_key = f"languages_{username}_{include_all}_{max_repos}"
        if cache_key in self._cache and self._is_cache_valid(cache_key):
            print(f"Using cached languages for {username}")
            return self._cache[cache_key]
            
        print(f"Fetching fresh language data for {username}")
        all_repos = self.get_repos(username)
        repos = all_repos[:max_repos] if max_repos else all_repos
        
        lang_bytes = {}
        for repo in repos:
            if repo.get("languages_url"):
                try:
                    r = requests.get(repo["languages_url"], headers=self.headers, timeout=5)
                    if r.status_code == 200:
                        for lang, bytes_count in r.json().items():
                            lang_bytes[lang] = lang_bytes.get(lang, 0) + bytes_count
                except:
                    continue
        
        total = sum(lang_bytes.values())
        if total == 0:
            result = {}
        else:
            result = {lang: round(count / total * 100, 1) for lang, count in lang_bytes.items()}
            if not include_all:
                result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:10])
            else:
                result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
        
        self._set_cache(cache_key, result)
        return result

    def get_user_stats(self, username: str) -> Dict:
        cache_key = f"stats_{username}"
        if cache_key in self._cache and self._is_cache_valid(cache_key):
            print(f"Using cached stats for {username}")
            return self._cache[cache_key]
            
        print(f"Fetching fresh stats for {username}")
        user = self.get_user(username)
        repos = self.get_repos(username)
        
        print(f"Counting stats for {username}...")
        
        total_commits = 0
        repos_to_count = repos
        
        print(f"  Counting commits from {len(repos_to_count)} repos...")
        for i, repo in enumerate(repos_to_count):
            try:
                r = requests.get(
                    f"https://api.github.com/repos/{username}/{repo['name']}/commits",
                    headers=self.headers,
                    params={'author': username, 'per_page': 1},
                    timeout=5
                )
                
                if r.status_code == 200:
                    link_header = r.headers.get('Link', '')
                    if 'last' in link_header:
                        match = re.search(r'page=(\d+)>; rel="last"', link_header)
                        if match:
                            total_commits += int(match.group(1))
                    elif r.json():
                        total_commits += len(r.json())
            except:
                continue
        
        print(f"  Counting pull requests...")
        total_prs = 0
        try:
            r_pr = requests.get(
                f"https://api.github.com/search/issues",
                headers=self.headers,
                params={'q': f'type:pr author:{username}', 'per_page': 1},
                timeout=10
            )
            if r_pr.status_code == 200:
                total_prs = r_pr.json().get('total_count', 0)
        except Exception as e:
            print(f"  Error counting PRs: {e}")
        
        print(f"  Counting issues...")
        total_issues = 0
        try:
            r_issue = requests.get(
                f"https://api.github.com/search/issues",
                headers=self.headers,
                params={'q': f'type:issue author:{username}', 'per_page': 1},
                timeout=10
            )
            if r_issue.status_code == 200:
                total_issues = r_issue.json().get('total_count', 0)
        except Exception as e:
            print(f"  Error counting issues: {e}")
        
        print(f"  Calculating contribution streak from ALL {len(repos)} repos...")
        current_streak, longest_streak = self._calculate_streak(username, repos)
        
        print(f"✓ Commits: {total_commits}")
        print(f"✓ PRs: {total_prs}")
        print(f"✓ Issues: {total_issues}")
        print(f"✓ Stars: {sum(r.get('stargazers_count', 0) for r in repos)}")
        print(f"✓ Repos: {user.get('public_repos', 0)}")
        print(f"✓ Followers: {user.get('followers', 0)}")
        print(f"✓ Current Streak: {current_streak} days")
        print(f"✓ Longest Streak: {longest_streak} days")
        
        stats = {
            "followers": user.get("followers", 0),
            "public_repos": user.get("public_repos", 0),
            "total_stars": sum(r.get("stargazers_count", 0) for r in repos),
            "total_commits": total_commits,
            "total_prs": total_prs,
            "total_issues": total_issues,
            "current_streak": current_streak,
            "longest_streak": longest_streak
        }
        
        self._set_cache(cache_key, stats)
        return stats
    
    def _calculate_streak(self, username: str, repos_sample: list) -> tuple:
        try:
            all_commit_dates = set()
            
            print(f"    Analyzing {len(repos_sample)} repositories for streak...")
            
            for idx, repo in enumerate(repos_sample):
                try:
                    r = requests.get(
                        f"https://api.github.com/repos/{username}/{repo['name']}/commits",
                        headers=self.headers,
                        params={'author': username, 'per_page': 100},
                        timeout=5
                    )
                    
                    if r.status_code == 200:
                        commits = r.json()
                        for commit in commits:
                            commit_date = commit.get('commit', {}).get('author', {}).get('date', '')
                            if commit_date:
                                date = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ').date()
                                all_commit_dates.add(date)
                    
                    if (idx + 1) % 10 == 0:
                        print(f"      Processed {idx + 1}/{len(repos_sample)} repos, found {len(all_commit_dates)} unique commit dates")
                        
                except Exception as e:
                    continue
            
            if not all_commit_dates:
                print(f"    ⚠️ No commit dates found!")
                return (0, 0)
            
            print(f"    Found {len(all_commit_dates)} unique commit dates")
            
            sorted_dates = sorted(all_commit_dates, reverse=True)
            today = datetime.now().date()
            
            print(f"    Most recent commit: {sorted_dates[0]}")
            print(f"    Today's date: {today}")
            
            current_streak = 0
            most_recent_commit = sorted_dates[0]
            days_since_last_commit = (today - most_recent_commit).days
            
            print(f"    Days since last commit: {days_since_last_commit}")
            
            if days_since_last_commit <= 1:
                current_streak = 1
                prev_date = most_recent_commit
                
                for i in range(1, len(sorted_dates)):
                    current_date = sorted_dates[i]
                    days_diff = (prev_date - current_date).days
                    
                    if days_diff == 1:
                        current_streak += 1
                        prev_date = current_date
                    elif days_diff == 0:
                        continue
                    else:
                        break
                
                print(f"    ✓ Current streak calculated: {current_streak} days")
            else:
                print(f"    ✗ No current streak (last commit was {days_since_last_commit} days ago)")
            
            longest_streak = 0
            temp_streak = 1
            sorted_dates_asc = sorted(all_commit_dates)
            
            if len(sorted_dates_asc) > 0:
                longest_streak = 1
                
                for i in range(1, len(sorted_dates_asc)):
                    days_diff = (sorted_dates_asc[i] - sorted_dates_asc[i-1]).days
                    
                    if days_diff == 1:
                        temp_streak += 1
                        longest_streak = max(longest_streak, temp_streak)
                    elif days_diff == 0:
                        continue
                    else:
                        temp_streak = 1
            
            print(f"    ✓ Longest streak: {longest_streak} days")
            
            return (current_streak, longest_streak)
            
        except Exception as e:
            print(f"    ✗ Error calculating streak: {e}")
            return (0, 0)
    
    def clear_cache(self, username: str = None):
        if username:
            keys_to_delete = [k for k in self._cache.keys() if username in k]
            for key in keys_to_delete:
                del self._cache[key]
                if key in self._cache_expiry:
                    del self._cache_expiry[key]
        else:
            self._cache.clear()
            self._cache_expiry.clear()