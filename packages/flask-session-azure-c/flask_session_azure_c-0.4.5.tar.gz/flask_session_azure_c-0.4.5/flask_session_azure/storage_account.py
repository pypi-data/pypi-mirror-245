import base64
from typing import Dict, List, Union, Tuple

from Cryptodome.Cipher import AES
from azure.core.exceptions import ResourceNotFoundError
from flask.json.tag import TaggedJSONSerializer
from azure.data.tables import TableClient

class StorageAccount(object):
    json_serializer = TaggedJSONSerializer()

    def __init__(self, connection_str: str, table_name: str, partition_key: str, create_table_if_not_exists: bool):
        self.table_name = table_name
        self.partition_key = partition_key
        self.create_table_if_not_exists = create_table_if_not_exists
        self.table_service = TableClient.from_connection_string(conn_str=connection_str, table_name=self.table_name)

    def write(self, key: str, data: dict, encryption_key: bytes) -> None:
        """
        serializes and encrypts the passed dict object object and writes it to the storage
        """

        data = self.json_serializer.dumps(data)
        encoded_data, tag, nonce = self.encrypt(data, encryption_key)
        entity = {
            "PartitionKey": self.partition_key,
            "RowKey": key,
            "Data": encoded_data,
            "Tag": tag,
            "Nonce": nonce
        }
        try:
            self.table_service.upsert_entity(entity=entity)
        except ResourceNotFoundError:
            if not self.create_table_if_not_exists:
                raise
            self.table_service.create_table()
            self.table_service.upsert_entity(entity=entity)

    def read(self, key: str, app_key: bytes) -> Union[List[Dict], None]:
        """
        reads encrypted data from storage and decrypts and deserializes it.
        Returns None if no data was found or decryption failed.
        """
        try:
            data = self.table_service.get_entity(self.partition_key, key)
            decoded = self.decrypt(data["Data"], data["Tag"], data["Nonce"], app_key)
            if decoded is not None:
                return self.json_serializer.loads(decoded)
            return None
        except ResourceNotFoundError:
            return None

    def delete(self, key: str) -> None:
        """
        Removes an element from storage if it exists
        """
        try:
            self.table_service.delete_entity(self.partition_key, key)
        except ResourceNotFoundError:
            pass

    @staticmethod
    def encrypt(data: str, secret_text: bytes) -> Tuple[str, str, str]:
        """
        encrypts the passed data with the secret text.
        :return: a tuple of three elements: encrypted data, verification_tag and nonce element.
        All elements are base64 encoded strings
        """
        cipher = AES.new(secret_text, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest((data.encode("utf-8")))
        return (base64.b64encode(ciphertext).decode("ascii"),
                base64.b64encode(tag).decode("ascii"),
                base64.b64encode(cipher.nonce).decode("ascii"))

    @staticmethod
    def decrypt(encrypted_data: str, verification_tag: str, nonce: str, secret_text: bytes) -> Union[str, None]:
        """
        Decrypts encoded data using the passed secret_text
        :param encrypted_data:  as base64 encoded string or byte array
        :param verification_tag: as base64 encoded string or byte array
        :param nonce: as base64 encoded string or byte array
        :param secret_text: the same secret text with wich the element was encoded
        :return: the plaintext on success, None if the data could not be decoded or verified
        """
        nonce = base64.b64decode(nonce)
        cipher = AES.new(secret_text, AES.MODE_EAX, nonce=nonce)
        data = base64.b64decode(encrypted_data)
        plaintext = cipher.decrypt(data)
        tag = base64.b64decode(verification_tag)
        try:
            cipher.verify(tag)
            return plaintext.decode("utf-8")
        except ValueError:
            return None
