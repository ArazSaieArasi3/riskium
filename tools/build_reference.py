"""Build the source-bound documentation portal (see tools/publication/README.md)."""
from publication.build_portal import main
from build_formal_reference import build, ROOT

if __name__ == '__main__':
    for name, expected in build().items():
        if not (ROOT / name).is_file() or (ROOT / name).read_text() != expected:
            raise SystemExit('Regenerate formal explanation: python tools/build_formal_reference.py')
    main()
