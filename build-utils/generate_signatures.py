import os
import pickle
import datetime

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


def sign_all(content_folder, signing_pri_key):
    signatures = dict()
    for f in os.listdir(content_folder):
        path = os.path.join(content_folder, f)
        if os.path.isfile(path):
            signature = signing_pri_key.sign(
                data=open(path, "rb").read(),
                padding=padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                algorithm=hashes.SHA256(),
            )
            signatures[f] = signature
    return signatures


dest_dir = os.path.join(os.getcwd(), "app", "server", "startup")
root_pri_key_path = os.path.join(os.getcwd(), "root-private-key.pem")
with open(root_pri_key_path, 'rb') as pem_in:
    pemlines = pem_in.read()
root_pri_key = serialization.load_pem_private_key(pemlines, password=None, backend=default_backend())

signatures = sign_all(dest_dir, root_pri_key)

pickle.dump(signatures, open(os.path.join(dest_dir, "signature.pkl"), "wb"))
