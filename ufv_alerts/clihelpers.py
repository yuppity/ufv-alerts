import sys

def stderr(*args, nl=True):
    sys.stdout.write(' '.join(args) + '\n' if nl else '')

def stderrfatal(*args, ec=1, nl=True):
    sys.stdout.write(' '.join(args) + '\n' if nl else '')
    sys.exit(ec)

def stdout(*args, nl=True):
    sys.stdout.write(' '.join(args) + '\n' if nl else '')
