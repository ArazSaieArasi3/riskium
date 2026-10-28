"""Project verified source-publication labels onto maintained pages after release."""
import argparse
import json
from pathlib import Path
import tempfile
from bs4 import BeautifulSoup

import build_snapshot_site as base
import snapshot_registry as snapshots

ROOT=snapshots.ROOT
RECEIPT='evaluation/releases/v0.3.4-publication.json'
COMPONENT='evaluation/releases/v0.3.4-publication-status/component.json'
SOURCES=['tools/publication/build_publication_status.py','tests/test_publication_status.py',
         '.github/workflows/publication-status.yml',RECEIPT]


def checked_publication(value):
    snapshots.require(value['tag']=='v0.3.4' and value['publication_state']=='PUBLISHED_AND_INDEPENDENTLY_DOWNLOADED_VERIFIED'
        and value['downloaded_bytes_match'] is True and value['tag_commit_verified'] is True
        and value['latest_verified'] is True and value['final_metadata']==dict(draft=False,prerelease=False)
        and len(value['assets'])==6 and len(value['previous_releases'])==10,'Unverified source publication status')
    snapshots.require(value['release_url']=='https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.4',
                      'Unreviewed source publication route')
    return value


def build(output,root=ROOT):
    publication=checked_publication(json.loads((root/RECEIPT).read_text()))
    manifest=base.build(output,root=root)
    base_manifest_sha=snapshots.original.sha((output/'publication-manifest.json').read_bytes())
    projected={}
    paths=sorted((output/'current').rglob('*.html'))+[output/'versions/index.html']
    snapshots.require(len(paths)==31,'Unexpected publication header scope')
    for path in paths:
        soup=BeautifulSoup(path.read_text(),'html.parser')
        anchors=soup.select('.publication-context a[href="https://github.com/ArazSaieArasi3/riskium/issues/45"]')
        snapshots.require(len(anchors)==1,'Missing maintained source release context')
        anchors[0]['href']=publication['release_url'];anchors[0].string='v0.3.4 published'
        if path==output/'versions/index.html':
            for paragraph in soup.select('main p'):
                if 'The v0.3.4 entry below is a frozen documentation snapshot' in paragraph.get_text():
                    paragraph.clear()
                    paragraph.append('The v0.3.4 entry below preserves documentation 0.3.0. Source distribution v0.3.4 is published and independently verified. ')
                    link=soup.new_tag('a',href=publication['release_url']);link.string='Read the published source release'
                    paragraph.append(link)
            for text in soup.find_all(string=lambda s:s and 'documentation snapshot; source release preparation remains open' in s):
                text.replace_with(text.replace('documentation snapshot; source release preparation remains open',
                    'documentation snapshot; source distribution v0.3.4 published'))
        path.write_text(str(soup)+'\n')
        projected[path.relative_to(output).as_posix()]=snapshots.original.sha(path.read_bytes())
    descriptor=dict(schema='riskium-post-publication-status-component-v1',id='RELEASE_PUBLICATION_STATUS',version='0.1.0',
        source_release='v0.3.4',source_commit=publication['source_commit'],release_id=publication['release_id'],
        current_documentation='0.3.0',native_model='0.3.1',unchanged_frozen_snapshots=4,
        projected_html_sha256=projected,files_sha256={p:snapshots.original.sha((root/p).read_bytes()) for p in SOURCES},
        scope='Post-publication maintained navigation/status projection. Frozen snapshot bytes and original source release assets remain unchanged.')
    manifest['publication_status_projection']=dict(component_version='0.1.0',source_release='v0.3.4',
        published_source_commit=publication['source_commit'],release_id=publication['release_id'],
        publication_receipt_sha256=descriptor['files_sha256'][RECEIPT],
        renderer_sha256=descriptor['files_sha256'][SOURCES[0]],base_deployment_manifest_sha256=base_manifest_sha,
        scope='Publication labels/navigation only; model and dated explanatory checkpoint text are preserved.')
    manifest['files_sha256']={p:snapshots.original.sha(b) for p,b in base.legacy.file_map(output).items() if p!='publication-manifest.json'}
    (output/'publication-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    return manifest,descriptor


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path);parser.add_argument('--check',action='store_true')
    parser.add_argument('--write-component',action='store_true');args=parser.parse_args()
    if args.check or args.write_component:
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'site';manifest,descriptor=build(output);result=base.audit(output)
        if args.write_component:
            target=ROOT/COMPONENT;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(json.dumps(descriptor,indent=2)+'\n')
        else:snapshots.require(json.loads((ROOT/COMPONENT).read_text())==descriptor,'Stale publication status component')
    else:
        if not args.output:parser.error('--output is required')
        manifest,descriptor=build(args.output)
        snapshots.require(json.loads((ROOT/COMPONENT).read_text())==descriptor,'Stale publication status component')
        result=base.audit(args.output)
    result.update(publication_status='PUBLISHED_AND_INDEPENDENTLY_DOWNLOADED_VERIFIED',source_release='v0.3.4',
                  published_source_commit=descriptor['source_commit'],projected_html_pages=31)
    print(json.dumps(result))


if __name__=='__main__':main()
