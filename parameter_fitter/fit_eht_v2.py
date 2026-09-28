#!/usr/bin/env python3
"""EHT fitter V2: image fitting with optional frontier-energy window."""
from pathlib import Path
import argparse,sys
HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description='Generic Extended-Huckel/YAeHMOP parameter fitter V2')
    ap.add_argument('structure',help='structure CIF')
    ap.add_argument('reference',help='band reference (PNG/JPG for --format image)')
    ap.add_argument('--format',choices=['image'],default='image')
    args,rest=ap.parse_known_args()
    if args.format=='image':
        sys.path.insert(0,str(HERE))
        import fit_from_image_staged_v2
        sys.argv=[str(HERE/'fit_from_image_staged_v2.py'),args.structure,args.reference,*rest]
        return fit_from_image_staged_v2.main()

if __name__=='__main__': main()
