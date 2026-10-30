#!/usr/bin/env python3
"""Import a committed course source revision; never import a working-tree copy."""
import argparse,hashlib,io,json,shutil,subprocess,tarfile,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LOCK=ROOT/'tools/course-source.json'
REPOSITORY='https://github.com/chorok-daddy/courses'
def run(args,cwd=None):return subprocess.check_output(args,cwd=cwd)
def allowed(name):
    p=Path(name)
    return not p.is_absolute() and '..' not in p.parts and (name.startswith(('niil/ko/courses/','niil/en/courses/','niil/assets/courses/')) or name in ('tools/course-catalog.json','tools/course-paths.json','tools/publication_layout.py','tools/publication-layout.json'))
def extract(archive,destination):
    # Only regular files/directories within the destination; reject links/devices.
    for member in archive.getmembers():
        target=destination/member.name
        if not target.resolve().is_relative_to(destination.resolve()):raise ValueError('Unsafe archive path')
        if member.isdir():target.mkdir(parents=True,exist_ok=True)
        elif member.isfile():
            target.parent.mkdir(parents=True,exist_ok=True)
            with archive.extractfile(member) as source,target.open('wb') as output:shutil.copyfileobj(source,output)
        else:raise ValueError('Unsupported archive member')
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,help='Local courses checkout; imports HEAD objects, not working files')
    ap.add_argument('--publication-output',type=Path,help='Also emit the generated English GitHub tree')
    ap.add_argument('--prepared-export',type=Path,help='Import a locally validated publication snapshot')
    ap.add_argument('--locked',action='store_true',help='Reproduce the recorded revision')
    args=ap.parse_args()
    if not args.source and not args.locked:ap.error('Choose --source or --locked')
    if args.source and args.locked:ap.error('Choose only one mode')
    previous=json.loads(LOCK.read_text()) if LOCK.exists() else {}
    source=args.source or ROOT.parent/'courses'
    if args.locked:
        if not previous:raise SystemExit('Missing course source lock')
        revision=previous['revision']
    else:
        revision=run(['git','rev-parse','HEAD'],source).decode().strip()
        if run(['git','status','--porcelain'],source).strip():raise SystemExit('Commit course source changes before importing')
    with tempfile.TemporaryDirectory(prefix='niil-course-source-') as temp:
        temp=Path(temp);snapshot=temp/'source';snapshot.mkdir();output=temp/'output'
        if args.prepared_export:
            if args.locked:raise SystemExit('Prepared export requires --source')
            prepared=json.loads(args.prepared_export.read_text())
            if prepared['source_revision']!=revision:raise SystemExit('Prepared revision differs from source HEAD')
            output=args.prepared_export.resolve().parent/'web'
            files=prepared['web_files']
        else:
            available=False
            if (source/'.git').exists():
                origin=run(['git','remote','get-url','origin'],source).decode().strip().removesuffix('.git')
                if origin not in (REPOSITORY,'git@github.com:chorok-daddy/courses'):raise SystemExit('Unexpected course repository origin')
                available=subprocess.run(['git','cat-file','-e',revision+'^{commit}'],cwd=source,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
            if available:
                archive=run(['git','archive','--format=tar',revision],source)
                with tarfile.open(fileobj=io.BytesIO(archive)) as tf:extract(tf,snapshot)
            else:
                archive=run(['gh','api','repos/chorok-daddy/courses/tarball/'+revision])
                unpack=temp/'unpack';unpack.mkdir()
                with tarfile.open(fileobj=io.BytesIO(archive),mode='r:gz') as tf:extract(tf,unpack)
                snapshot=next(unpack.iterdir())
            command=['python3',str(snapshot/'tools/export_site.py'),'--output',str(output),'--source-revision',revision]
            if args.publication_output:command+=['--publication-output',str(args.publication_output.resolve())]
            result=run(command)
            files=json.loads(result)
        if not all(allowed(p) for p in set(files)|set(previous.get('files',{}))):raise SystemExit('Unsafe export path')
        if args.locked and files!=previous['files']:raise SystemExit('Pinned export no longer matches recorded hashes')
        for name,digest in files.items():
            if hashlib.sha256((output/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Export digest mismatch: '+name)
        for name in set(previous.get('files',{}))-set(files):(ROOT/name).unlink(missing_ok=True)
        for name in files:
            target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(output/name,target)
        LOCK.write_text(json.dumps({'repository':REPOSITORY,'revision':revision,'files':files},ensure_ascii=False,indent=2)+'\n')
        print(f'Imported {len(files)} course source files at {revision[:12]}')
if __name__=='__main__':main()
