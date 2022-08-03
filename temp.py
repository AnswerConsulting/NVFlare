with open("rootpath", "rb") as f:
    trusted_certs = f.read()
with open("clientkeypath", "rb") as f:
    private_key = f.read()
with open("clientcertpath", "rb") as f:
    certificate_chain = f.read()

credentials = grpc.ssl_channel_credentials(
    certificate_chain=certificate_chain, private_key=private_key, root_certificates=trusted_certs
)

# make sure that all headers are in lowecase,
# otherwise grpc throws an exception
# call_credentials = grpc.metadata_call_credentials(
#     lambda context, callback: callback((("x-custom-token", token),), None)
# )