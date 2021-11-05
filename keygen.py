from Crypto.PublicKey import RSA

# generate pem
key = RSA.generate(2048)
private_key = key.export_key()
file_out = open("private2.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().export_key()
file_out = open("public2.pem", "wb")
file_out.write(public_key)
file_out.close()