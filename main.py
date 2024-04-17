import base64
import distutils
from Crypto.Cipher import AES


def generate_license_code(generate_computer_code, expiration_time):
    """使用机器码和有效时间来生成授权码"""
    iv = b'0123456789abcdef'
    key = '01234567890abcdefABCDEF!'  # 加密密钥
    key = (key + ' ' * (AES.block_size - len(key) % AES.block_size)).encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    code = generate_computer_code + "*" + expiration_time
    plaintext = (code + ' ' * (AES.block_size - len(code) % AES.block_size)).encode()
    ciphertext = cipher.encrypt(plaintext)
    return base64.b64encode(ciphertext).decode().swapcase()


if __name__ == '__main__':
    generate_computer_code = "5DEB9565E6291F9B1314A1BF066CAE85685B8510D3C96FEA063AC0D49181B37A"  # 机器码
    expiration_time = "2029-11-01"  # 有效日期
    print(generate_license_code(generate_computer_code, expiration_time))

