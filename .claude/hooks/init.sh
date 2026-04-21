#!/bin/bash
set -e
echo "=== sob-python Environment Check ==="
cd /home/kay/repos/sob-python
echo "1. Python..."
python3 --version 2>/dev/null || echo "   ✗ Python3 nicht gefunden"
echo "2. Package..."
pip show sob-python 2>/dev/null | grep -E "^(Name|Version)" || echo "   ✗ Nicht installiert (pip install -e '.[dev]')"
echo "=== Check Complete ==="
