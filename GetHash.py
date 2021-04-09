from Scripts import utils
import hashlib, os

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
            hashermd5    = hashlib.md5()
            hashersha1   = hashlib.sha1()
            hashersha256 = hashlib.sha256()
            with open(checked_path,"rb") as f:
                hashermd5.update(f.read())
                hashersha1.update(f.read())
                hashersha256.update(f.read())
            last_hash["path"]   = checked_path
            last_hash["md5"]    = hashermd5.hexdigest()
            last_hash["sha1"]   = hashersha1.hexdigest()
            last_hash["sha256"] = hashersha256.hexdigest()