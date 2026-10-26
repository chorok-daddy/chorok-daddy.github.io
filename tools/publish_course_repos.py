#!/usr/bin/env python3
"""Publish reproducible course exports to their existing GitHub repositories.

Requires explicit --publish. No force-push, repo creation, or unrelated file removal.
Run build_niil.py and checks first. Then publish these mirrors before the website.
"""
import argparse,json,subprocess,tempfile
from pathlib import Path
from export_course_repos import CONFIG,export_course

def run(args,cwd=None):return subprocess.run(args,cwd=cwd,check=True,text=True,capture_output=True).stdout.strip()

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--publish',action='store_true',required=True);ap.parse_args()
    for course in CONFIG['courses']:
        url=f"https://github.com/{CONFIG['owner']}/{course['repository']}.git"
        with tempfile.TemporaryDirectory(prefix='niil-course-publish-') as temp:
            repo=Path(temp)/'repo';run(['git','clone',url,str(repo)])
            previous=repo/'SOURCE.json'
            if previous.exists():
                # Only replace files recorded as generated in the preceding export.
                for name in json.loads(previous.read_text())['files']:
                    target=(repo/name).resolve()
                    if not target.is_relative_to(repo.resolve()) or '.git' in Path(name).parts:raise ValueError(name)
                    target.unlink(missing_ok=True)
                previous.unlink()
            result=export_course(course,repo)
            run(['git','add','--all'],repo)
            if not run(['git','diff','--cached','--name-only'],repo):
                print(course['repository']+': already current');continue
            run(['git','commit','-m','Update course source snapshot '+result['snapshot']],repo)
            run(['git','push','origin','HEAD:main'],repo)
            print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
