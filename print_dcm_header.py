from argparse import ArgumentParser
from os import path, makedirs, sep
import pydicom
import types


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', nargs='+', dest='input_files', required=True)
    parser.add_argument('-o', dest='save_dir', default=None)
    args = parser.parse_args()

    if args.save_dir is not None:
        makedirs(args.save_dir, exist_ok=True)

    for dcm_f in args.input_files:
        try:
            dcm = pydicom.dcmread(dcm_f, stop_before_pixels=True)
            #dcm = pydicom.dcmread(dcm_f)

            if args.save_dir is not None:
                sd = path.join(args.save_dir, dcm_f)
                makedirs(path.dirname(sd), exist_ok=True)
                out = open(sd, 'w')
            else:
                out = open(dcm_f + '_hdr.txt', 'w')

            for f in dir(dcm):

                # if f.startswith('_'):
                #    continue

                if 'pixel' not in f.lower():

                    val = getattr(dcm, f)

                    # if isinstance(val, (types.FunctionType, types.BuiltinFunctionType, types.MethodType, types.BuiltinMethodType)):
                    #    continue

                    out.write(f'****\n{f}\n@\n{val}\n\n')

            out.close()
        except:
            continue
