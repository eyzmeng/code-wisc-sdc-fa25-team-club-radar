#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# scripts/poe2txt.py - poetry.lock to requirements.txt
#
# A hopefully cross-platform script for... whatever.
# I forgot what I was going to say, but this trick keeps
# me sane, and, as a somewhat pleasant side-effect, also
# happens to teaches Vercel how to install dependencies.
#
# NOTE: You should have poetry-export plugin installed:
#     <https://github.com/python-poetry/poetry-plugin-export>
# The command to install is:
#     poetry self add poetry-plugin-export
#

import os
import pathlib
import subprocess
import sys

def main():
    backend_root = pathlib.Path(__file__).parent.parent / 'api'
    try:
        subprocess.run('poetry export --format requirements.txt --output requirements.txt --without-hashes'
                       .split(), check=True, cwd=os.fspath(backend_root))
    except subprocess.CalledProcessError as exc:
        if not poetry_may_have_export():
            import textwrap
            raise RuntimeError(textwrap.dedent("""
                Failed to exec poetry export.  Note that as of Poetry 2.0,
                poetry export is removed from core.  The command to install
                it as a plugin is:

                poetry self add poetry-plugin-export

                See the <https://github.com/python-poetry/poetry-plugin-export>
                README for more information.
            """)) from exc
        raise exc
    # Compute this retroactively in case someone complains to me
    # that this command is too quiet (being an introvert in this
    # world is hard, sigh...  u.u)
    target = backend_root / 'requirements.txt'
    print("Write", target, "OK", file=sys.stderr)

def poetry_may_have_export():
    """
    Poke around and find out... if we don't, let's just say it is.
    Be conservative of our judgment, anyways.
    """
    try:
        import poetry.__version__
    except ImportError:
        # Poetry has no stable API; anything could happen at this point.
        return False

    try:
        poetry_version = poetry.__version__.__version__
    except AttributeError:
        return False

    try:
        (major_version, *_) = poetry_version.split('.', maxsplit=2)
    except (AttributeError, TypeError):
        return False

    try:
        return int(major_version) >= 2
    except (TypeError, ValueError):
        return False


if __name__ == '__main__':
    main()
