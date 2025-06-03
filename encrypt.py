import base64
import hashlib
from typing import Optional


class PasswordCipher:
    def __init__(self, salt: Optional[bytes] = None):
        """
        初始化密码加密器

        参数:
            salt: 可选的盐值，如果为None则使用默认盐值
        """
        self.salt = salt if salt else b'Cyber Cricket'
        self.xor_key = 0x55  # 基础异或密钥
        self.rot_offset = 13  # ROT13偏移量

    def _derive_key(self, input_str: str, index: int = 0) -> int:
        """从输入字符串派生动态密钥"""
        md5 = hashlib.md5((input_str + self.salt.decode()).encode()).hexdigest()
        return (sum(ord(c) for c in md5) + index) % 256

    def encrypt_pwd(self, raw_pwd: str) -> str:
        """
        加密原始密码，返回可硬编码的加密字符串

        参数:
            raw_pwd: 原始明文密码

        返回:
            加密后的字符串
        """
        # 多层加密
        encrypted = []
        for i, c in enumerate(raw_pwd):
            # 派生当前字符的密钥
            dynamic_key = self._derive_key(raw_pwd[:i], i)

            # 第一层: XOR with dynamic key
            xor_val = ord(c) ^ dynamic_key
            # 第二层: ROT13变种
            rot_val = (xor_val + self.rot_offset + i) % 256
            # 第三层: Base64编码
            encrypted_char = base64.b64encode(bytes([rot_val])).decode()
            encrypted.append(encrypted_char)

        # 组合并添加校验头
        encrypted_str = ''.join(encrypted)
        checksum = hashlib.sha256((raw_pwd + self.salt.decode()).encode()).hexdigest()[:8]
        return f"$AES${checksum}${encrypted_str}"

    def get_pwd(self, encrypted_pwd: str) -> Optional[str]:
        """
        从加密字符串解密获取原始密码

        参数:
            encrypted_pwd: 加密后的密码字符串

        返回:
            解密后的原始密码，如果解密失败返回None
        """
        if not encrypted_pwd.startswith("$AES$"):
            print("加密字符串格式错误")
            return None

        try:
            # 提取校验和和加密内容
            _, _, checksum, encrypted_str = encrypted_pwd.split('$', 3)

            # 解密过程
            encrypted_chars = [encrypted_str[i:i + 4] for i in range(0, len(encrypted_str), 4)]
            decrypted = []

            for i, ec in enumerate(encrypted_chars):
                # 反向Base64
                rot_val = base64.b64decode(ec)[0]
                # 反向ROT13
                xor_val = (rot_val - self.rot_offset - i) % 256
                # 派生当前字符的密钥
                dynamic_key = self._derive_key(''.join(decrypted), i)
                # 反向XOR
                decrypted_char = chr(xor_val ^ dynamic_key)
                decrypted.append(decrypted_char)

            raw_pwd = ''.join(decrypted)

            # 验证校验和
            calculated_checksum = hashlib.sha256((raw_pwd + self.salt.decode()).encode()).hexdigest()[:8]
            if calculated_checksum == checksum:
                return raw_pwd
            print(f"校验和不匹配: {calculated_checksum} != {checksum}")
            return None

        except Exception as e:
            print(f"解密过程出错: {e}")
            return None


# 实例化全局密码加密器
_cipher = PasswordCipher()


def encrypt_str(raw_pwd: str) -> str:
    """对外暴露的加密函数"""
    return _cipher.encrypt_pwd(raw_pwd)


def get_pwd(
        encrypted_pwd: str = "$AES$d7c9b645$ug==LA==Zg==7A==ow==6w==vg==RA==rQ==3Q==Og==2g==PQ==eQ==KA==WQ==Jw==Vg==PA==eQ==XA==9w==YQ==WQ==HQ==3A==Xg==kw==Iw==Dg==wg==og==Sg==PA==uw==QQ==mg==gg==8Q==RQ==KQ==jg==gg==xg==Gg==ZQ==ZA==kg==HQ==0w==7w==Ow==Nw==Zg==Ow==zA==Zw==ag==9g==/Q==mQ==JA==5A==LA==") -> \
Optional[str]:
    """对外暴露的解密函数"""
    return _cipher.get_pwd(encrypted_pwd)


if __name__ == '__main__':
    import json

    with open('pwd.json', 'r') as f:
        pwd_dict = json.load(f)
        raw_pwd = pwd_dict['pwd']

    # 加密测试
    encrypted = encrypt_str(raw_pwd)
    print(f"加密结果: {encrypted}")

    # 解密测试
    decrypted = get_pwd()
    print(f"解密结果: {decrypted}")
    print(f"验证结果: {raw_pwd == decrypted}")
