from Scripts import utils
import hashlib, os

os.chdir(os.path.abspath(os.path.dirname(os.path.realpath(__file__))))
u = utils.Utils("GetMD5")
while True:
    while True:
        u.head()
        print("")
        f_path = u.grab("Please input the file path:  ")
        if not f_path: continue
        if f_path.lower() == "q": u.custom_quit()
        checked_path = u.check_path(f_path)
        if checked_path and os.path.isfile(checked_path):
            break
    hashermd5    = hashlib.md5()
    hashersha1   = hashlib.sha1()
    hashersha256 = hashlib.sha256()
    with open(checked_path,"rb") as f:
        hashermd5.update(f.read())
        hashersha1.update(f.read())
        hashersha256.update(f.read())
    u.head()
    print("\nFile:\n{}\n\nMD5:\n{}\n\nSHA1:\n{}\n\nSHA256:\n{}\n".format(
        checked_path,
        hashermd5.hexdigest(),
        hashersha1.hexdigest(),
        hashersha256.hexdigest()
    ))
    u.grab("Press [enter] to select a new file...")