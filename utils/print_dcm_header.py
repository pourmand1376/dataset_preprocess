from argparse import ArgumentParser
from os import makedirs, path
from pathlib import Path

import pydicom

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", nargs="+", dest="input_files", required=True)
    parser.add_argument("-o", dest="save_dir", default=None)
    parser.add_argument(
        "--save_in_parent", dest="save_in_parent", required=False, default=False
    )
    args = parser.parse_args()

    if args.save_in_parent:
        path = Path(args.input_files[0])
        args.save_dir = path.absolute() / "header_data"

    if args.save_dir is not None:
        makedirs(args.save_dir, exist_ok=True)

    for dcm_f in args.input_files:
        try:
            dcm_f = Path(dcm_f)
            dcm = pydicom.dcmread(dcm_f, stop_before_pixels=True)

            if args.save_dir is not None:
                sd = args.save_dir / Path(dcm_f.name + "_hdr.txt")
                out = open(sd, "w")
            else:
                out = open(str(dcm_f) + "_hdr.txt", "w")

            out.write(str(dcm))
            out.close()
            print(f"File {dcm_f} successfully processed.")

        except Exception:
            pass
