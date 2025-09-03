#!/usr/bin/env python
"""Regenerate PDF case sheets for receipes.

Usage:
    python scripts/regenerate_pdfs.py --all
    python scripts/regenerate_pdfs.py --id 11
"""
import os
import sys
import argparse

# Ensure project root is on path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Muvva.settings')
import django
django.setup()

from home.models import Receipe
from home.views import _write_case_pdf

parser = argparse.ArgumentParser()
parser.add_argument('--all', action='store_true', help='Regenerate PDFs for all receipes')
parser.add_argument('--id', type=int, help='Regenerate PDF for a specific receipe id')
args = parser.parse_args()

if not args.all and not args.id:
    print('Nothing to do. Use --all or --id <id>')
    sys.exit(1)

qs = None
if args.all:
    qs = Receipe.objects.all()
else:
    try:
        qs = [Receipe.objects.get(id=args.id)]
    except Receipe.DoesNotExist:
        print('Receipe id not found:', args.id)
        sys.exit(2)

print('Will regenerate PDFs for', qs.count() if hasattr(qs, 'count') else len(qs), 'receipe(s)')

count = 0
for r in qs:
    try:
        path = _write_case_pdf(r)
        print('WROTE:', path)
        count += 1
    except Exception as e:
        print('ERROR writing for id', r.id, e)

print('Done. Regenerated', count, 'PDF(s)')
