import os
from src.logger import logger

from cryptography.fernet import Fernet


class FernetEncrypter:

    def __init__(self, key_path: str) -> None:

        self.key = None
        self.time_key = None
        self.get_key(key_path)
        self.status = {'success': 0, 'fail': 0}
        self.logger = logger(log_name='enCryptor')

        self.filter_ascii_char = lambda x: ''.join(e if e.isascii() else '' for e in x )
        
    def string_cryptor(self, string: str, encode: bool) -> str:

        # Instance the Fernet class with the key
        fernet = Fernet(self.key)

        # then use the Fernet class instance
        if encode:
            cryp_string = str(fernet.encrypt(string.encode()), 'UTF-8')
        else:
            cryp_string = fernet.decrypt(string).decode()

        return cryp_string
    
    def file_cryptor(self, new_file:str, encode:bool) -> None:

        # using the generated key
        fernet = Fernet(self.key)

        # opening the original file to encrypt
        with open(new_file, 'rb') as eFile:
            original = eFile.read()

        if encode:
            # encrypting the file
            crypted = fernet.encrypt(original)
        else:
            # decrypting the file
            crypted = fernet.decrypt(original)

        # opening the file in write mode and
        # writing the encrypted data
        with open(new_file, 'wb') as crypted_file:
            crypted_file.write(crypted)

    def rename_file(self, folder_path:str, file:str, encode:bool) -> str:

        if encode:
            new_file_name = self.filter_ascii_char(str(os.path.basename(file)))
        else:
            new_file_name = str(os.path.basename(file))

        new_file_name = self.string_cryptor(new_file_name, encode)
        new_file = os.path.join(folder_path, new_file_name)
        os.rename(file, new_file)

        return new_file

    def get_key(self, key_path: str) -> None:

        if not os.path.exists(key_path):
            key = Fernet.generate_key()

            # string the key in a file
            self.logger.warning(f"No Key found, creating one at path:{key_path}")
            with open(key_path, 'wb') as filekey:
                filekey.write(key)

        # opening the key
        with open(key_path, 'rb') as filekey:
            self.key = filekey.read()

    def folder_cryptor(self, folder_path: str, encode: bool, code_lvl: bool) -> None:

        # iterate over files in that directory
        for filename in os.listdir(folder_path):
            file = os.path.join(folder_path, filename)

            try:
                # checking if it is a file
                if os.path.isfile(file):

                    new_file = self.rename_file(folder_path, file, encode)

                    # encrypts files at root level
                    if code_lvl:
                        self.logger.info(f"crypting lvl_{encode}: old {file} -> new {new_file}")
                        self.file_cryptor(new_file, encode)

                    self.status['success'] += 1

                # else calling itself
                else:
                    # encrypted folder names were bugging the os.stat logics
                    # hence while decrypting renaming first to transverse properly
                    if encode:
                        self.folder_cryptor(file, encode, code_lvl)
                        self.rename_file(folder_path, file, encode)
                    else:
                        file = self.rename_file(folder_path, file, encode)
                        self.folder_cryptor(file, encode, code_lvl)
            
            except Exception as e:

                self.status['fail'] += 1
                status = file + '---->\n' + str(e.args)
                self.logger.error(f"ERROR in cryption lvl-{encode}: {status}")

                continue
        
        # self.logger.info(f'Final Status cryption lvl-{encode} {self.status}')
        return self.status


if __name__ == '__main__':
    enc = FernetEncrypter('key.k')
    # status = enc.folder_cryptor(r"path", encode=1, code_lvl=0)

    print(enc.string_cryptor('he', 1))
