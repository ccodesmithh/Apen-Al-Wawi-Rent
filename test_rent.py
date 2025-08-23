import unittest
from unittest.mock import patch
import rent

class TestRentUtils(unittest.TestCase):
    def test_format_rupiah(self):
        self.assertEqual(rent.format_rupiah(1000), "1.000")
        self.assertEqual(rent.format_rupiah(123456789), "123.456.789")
        self.assertEqual(rent.format_rupiah(0), "0")

    def test_pilihan_structure(self):
        self.assertIn("mb1", rent.pilihan)
        self.assertEqual(rent.pilihan["mb1"][0], "G-Class")
        self.assertEqual(rent.pilihan["s2"][2], ["Biru", "Merah", "Hijau"])

    @patch('builtins.input', side_effect=["halomas", "keluar", "mb1"])
    def test_input_user_ai_trigger(self, mock_input):
        # Should call tanya_masyud, then continue to next input
        result = rent.input_user("Masukan jenis kendaraan: ", choices=["mb1", "mb2"])
        self.assertEqual(result, "mb1")

    @patch('builtins.input', side_effect=["invalid", "mb2"])
    def test_input_user_invalid_choice(self, mock_input):
        result = rent.input_user("Masukan jenis kendaraan: ", choices=["mb1", "mb2"])
        self.assertEqual(result, "mb2")

    @patch('builtins.input', side_effect=["merah"])
    def test_input_user_capitalize(self, mock_input):
        result = rent.input_user("Pilih warna: ", choices=["Merah", "Putih"], capitalize=True)
        self.assertEqual(result, "Merah")

if __name__ == "__main__":
    unittest.main()
