import binascii
import unittest

from sdk.algo import hash


class TestAlgo(unittest.TestCase):
    def setUp(self):
        self.fromGroup = 1
        self.toGroup = 1
        self.headerBlob = "0007000000000001baf7b5b4201dbb9c0d720096f0f3fc21cd8f9578e0d106ffc2200000000000013fbc0733bf1d70feed5602ad30099ff45e466fc03a954842d0ba00000000000058e8324fd030bdf759c6dcfd2736be5560c50cf9de82b0acb2ef000000000000ec29cf83ad840f2595686576f8d4a87dbcefddb061ea45c72814000000000001f2d25a0ee3f16fd47ac8020d94ebaba7004e268a3e364d9fc805000000000000f48ac22dae1728cb6cfb2f3e958a986357d9fcc31ec2ef3df326000000000001fb65a45d5421df327e2a2361463e6b7885ef0c6de63fdfd0e597d31119f2d4285cf23a6e4f3b5b54bb12e6c2db12fd25879dbdeeba8dc5d0757fa54b4bc3988fb5a66aca61cdd6a19779d0d0d9d36b03c80de165f5c004f64f580000018deea0bf7a1b0224b5"
        self.targetBlob = "0000000225c17d04dad2965cc5a02a23e254c0c3f75d9178046aeb27ce1ca575"
        self.nonce = "f408010101000400040000040303010401040002d3ecfd20"
        self.pow_hash = "00000000625b67cd0addda9688dfd0a0a6cf2cb2fea9329e5b58967545261f55"

    def test_pow_hash(self):
        hash_bytes = hash.pow_hash(self.nonce, self.headerBlob)
        self.assertEqual(self.pow_hash, binascii.b2a_hex(hash_bytes).decode())
        self.assertTrue(int(binascii.b2a_hex(hash_bytes).decode(), 16) <= int(self.targetBlob, 16))

    def test_chain_index(self):
        fromGroup, toGroup = hash.get_block_chain_index(self.pow_hash)
        self.assertEqual(self.fromGroup, fromGroup)
        self.assertEqual(self.toGroup, toGroup)


if __name__ == '__main__':
    unittest.main()
