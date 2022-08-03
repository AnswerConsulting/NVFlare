import os
import pickle
import datetime

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509 import Certificate
from cryptography.x509.oid import NameOID

def _generate_keys():
        pri_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        pub_key = pri_key.public_key()
        return pri_key, pub_key


def _generate_cert(subject, issuer, signing_pri_key, subject_pub_key, valid_days=360, ca=False):
        builder = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(subject_pub_key)
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(
                # Our certificate will be valid for 360 days
                datetime.datetime.utcnow()
                + datetime.timedelta(days=valid_days)
                # Sign our certificate with our private key
            )
        )
        if ca:
            builder = (
                builder.add_extension(
                    x509.SubjectKeyIdentifier.from_public_key(subject_pub_key),
                    critical=False,
                )
                .add_extension(
                    x509.AuthorityKeyIdentifier.from_issuer_public_key(subject_pub_key),
                    critical=False,
                )
                .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=False)
            )
        return builder.sign(signing_pri_key, hashes.SHA256(), default_backend())


def _x509_name(cn_name, org_name=None):
        name = [x509.NameAttribute(NameOID.COMMON_NAME, cn_name)]
        if org_name is not None:
            name.append(x509.NameAttribute(NameOID.ORGANIZATION_NAME, org_name))
        return x509.Name(name)


def serialize_pri_key(pri_key):
    return pri_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )


def serialize_cert(cert):
    return cert.public_bytes(serialization.Encoding.PEM)


def _build_root(subject, issuer):
    root_pri_key, root_pub_key = _generate_keys()
    subject_name = _x509_name(subject)
    issuer_name = _x509_name(issuer)
    root_cert = _generate_cert(subject_name, issuer_name, root_pri_key, root_pub_key, ca=True)
    # serialized_root_cert = serialize_cert(root_cert)
    # serialized_pri_key = serialize_pri_key(pri_key)
    return root_pri_key, root_pub_key, root_cert


def _build_cert_pair(subject, root_cert: Certificate, root_pri_key):
    pri_key, pub_key = _generate_keys()
    subject_name = _x509_name(subject)
    issuer_name = root_cert.issuer
    cert = _generate_cert(subject_name, issuer_name, root_pri_key, pub_key, ca=False)
    return pri_key, cert

working_dir = os.getcwd()
dest_dir = os.path.join(working_dir, "build-utils", "generated-certs")

root_pri_key,root_pub_key,root_cert = _build_root("flip", "flip")

server_pri_key, server_cert = _build_cert_pair("flip-server", root_cert, root_pri_key)

client_pri_key, client_cert = _build_cert_pair("flip-client", root_cert, root_pri_key)

with open(os.path.join(dest_dir, "root", f"rootCA.crt"), "wb") as f:
    f.write(serialize_cert(root_cert))
with open(os.path.join(dest_dir, "root", f"root.key"), "wb") as f:
    f.write(serialize_pri_key(root_pri_key))
with open(os.path.join(dest_dir, "server", f"server.crt"), "wb") as f:
    f.write(serialize_cert(server_cert))
with open(os.path.join(dest_dir, "server", f"server.key"), "wb") as f:
    f.write(serialize_pri_key(server_pri_key))
with open(os.path.join(dest_dir, "client", f"client.crt"), "wb") as f:
    f.write(serialize_cert(client_cert))
with open(os.path.join(dest_dir, "client", f"client.key"), "wb") as f:
    f.write(serialize_pri_key(client_pri_key))
