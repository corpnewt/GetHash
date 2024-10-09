from Scripts import utils
import hashlib, os, sys

def get_size(size, suffix=None, use_1024=False, round_to=2, strip_zeroes=False):
    # size is the number of bytes
    # suffix is the target suffix to locate (B, KB, MB, etc) - if found
    # use_2014 denotes whether or not we display in MiB vs MB
    # round_to is the number of dedimal points to round our result to (0-15)
    # strip_zeroes denotes whether we strip out zeroes 

    # Failsafe in case our size is unknown
    if size == -1:
        return "Unknown"
    # Get our suffixes based on use_1024
    ext = ["B","KiB","MiB","GiB","TiB","PiB"] if use_1024 else ["B","KB","MB","GB","TB","PB"]
    div = 1024 if use_1024 else 1000
    s = float(size)
    s_dict = {} # Initialize our dict
    # Iterate the ext list, and divide by 1000 or 1024 each time to setup the dict {ext:val}
    for e in ext:
        s_dict[e] = s
        s /= div
    # Get our suffix if provided - will be set to None if not found, or if started as None
    suffix = next((x for x in ext if x.lower() == suffix.lower()),None) if suffix else suffix
    # Get the largest value that's still over 1
    biggest = suffix if suffix else next((x for x in ext[::-1] if s_dict[x] >= 1), "B")
    # Determine our rounding approach - first make sure it's an int; default to 2 on error
    try:round_to=int(round_to)
    except:round_to=2
    round_to = 0 if round_to < 0 else 15 if round_to > 15 else round_to # Ensure it's between 0 and 15
    bval = round(s_dict[biggest], round_to)
    # Split our number based on decimal points
    a,b = str(bval).split(".")
    # Check if we need to strip or pad zeroes
    b = b.rstrip("0") if strip_zeroes else b.ljust(round_to,"0") if round_to > 0 else ""
    return "{:,}{} {}".format(int(a),"" if not b else "."+b,biggest)

TERMINAL_WIDTH = 120 if os.name=="nt" else 80

os.chdir(os.path.abspath(os.path.dirname(os.path.realpath(__file__))))
u = utils.Utils("GetHash")
last_hash = {}
while True:
    while True:
        u.head()
        print("")
        if last_hash:
            print("File:\n{}\n\nMD5:\n{}\n\nSHA1:\n{}\n\nSHA256:\n{}\n".format(
                last_hash.get("path","Unknown Path"),
                last_hash.get("md5","Unknown MD5"),
                last_hash.get("sha1","Unknown SHA1"),
                last_hash.get("sha256","Unknown SHA256")
            ))
        print("Q. Quit\n")
        f_path = u.grab("Please input the file path:  ")
        if not f_path: continue
        if f_path.lower() == "q": u.custom_quit()
        checked_path = u.check_path(f_path)
        if checked_path and os.path.isfile(checked_path):
            u.head()
            print("")
            print("Processing {}...".format(os.path.basename(checked_path)))
            hashermd5    = hashlib.md5()
            hashersha1   = hashlib.sha1()
            hashersha256 = hashlib.sha256()
            chunk_size   = 2**20
            print(" - Calculating size...")
            total_bytes  = os.stat(checked_path).st_size
            print(" - Calculating checksum...")
            bytes_read   = 0
            with open(checked_path,"rb") as f:
                while True:
                    fread = f.read(chunk_size)
                    if not fread:
                        break
                    bytes_read += len(fread)
                    percent = round(float(bytes_read)/total_bytes*100, 2)
                    perc_str = " {:.2f}%".format(percent)
                    bar_width = (TERMINAL_WIDTH // 3)-len(perc_str)
                    progress = "=" * int(bar_width * (percent/100))
                    sys.stdout.write("\r\033[K --> {}/{} | {}{}{}".format(
                        get_size(bytes_read),
                        get_size(total_bytes),
                        progress,
                        " " * (bar_width-len(progress)),
                        perc_str
                    ))
                    sys.stdout.flush()
                    hashermd5.update(fread)
                    hashersha1.update(fread)
                    hashersha256.update(fread)
            last_hash["path"]   = checked_path
            last_hash["md5"]    = hashermd5.hexdigest()
            last_hash["sha1"]   = hashersha1.hexdigest()
            last_hash["sha256"] = hashersha256.hexdigest()
