import os
import shutil
import unittest

from my_method import DirectoryListing as dl


class TestDirectoryListing(unittest.TestCase):
    def setUp(self) -> None:
        self.cwd = os.getcwd()
        self.test_dir = os.path.join(self.cwd, "test_dir")
        os.mkdir(self.test_dir)
        os.chdir(self.test_dir)
        self.text_ext = ".txt"
        self.wav_ext = ".wav"
        self.test_file_name = "test_file"
        self.test_name = "test"
        self.test1_num = "1"
        self.test2_num = "2"
        self.test1 = self.test_name + self.test1_num
        self.test2 = self.test_name + self.test2_num
        self.test_txt = self.test_file_name + self.text_ext
        self.test_wav = self.test_file_name + self.wav_ext
        os.mkdir(os.path.join(self.test_dir, self.test1))
        os.mkdir(os.path.join(self.test_dir, self.test2))
        self.test_txt_path = os.path.join(self.test_dir, self.test_txt)
        self.test_wav_path = os.path.join(self.test_dir, self.test_wav)
        with open(self.test_txt, "w"):
            pass
        with open(self.test_wav, "w"):
            pass

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        shutil.rmtree(self.test_dir)

    def test_file_listing(self) -> None:
        self.assertEqual(dl.file_listing(self.test_dir), (self.test_txt, self.test_wav))
        self.assertEqual(dl.file_listing(self.test_dir, self.text_ext), (self.test_txt,))
        self.assertEqual(dl.file_listing(self.test_dir, (self.text_ext,)), (self.test_txt,))
        self.assertEqual(dl.file_listing(self.test_dir, self.wav_ext), (self.test_wav,))
        self.assertEqual(dl.file_listing(self.test_dir, (self.wav_ext,)), (self.test_wav,))
        self.assertEqual(dl.file_listing(self.test_dir, (self.text_ext, self.wav_ext)), (self.test_txt, self.test_wav))
        self.assertEqual(dl.file_listing(self.test_dir, "error"), ())
        self.assertEqual(dl.file_listing(self.test_dir, exc_targets=self.test_txt), (self.test_wav,))
        self.assertEqual(dl.file_listing(self.test_dir, exc_targets=(self.test_txt,)), (self.test_wav,))
        self.assertEqual(dl.file_listing(self.test_dir, exc_targets=self.test_wav), (self.test_txt,))
        self.assertEqual(dl.file_listing(self.test_dir, exc_targets=(self.test_wav,)), (self.test_txt,))
        self.assertEqual(dl.file_listing(self.test_dir, exc_targets=(self.test_txt, self.test_wav)), ())
        self.assertEqual(dl.file_listing(self.test_dir, exc_targets="error"), (self.test_txt, self.test_wav))

    def test_dir_listing(self) -> None:
        self.assertEqual(dl.dir_listing(self.test_dir), (self.test1, self.test2))
        self.assertEqual(dl.dir_listing(self.test_dir, self.test1_num), (self.test1,))
        self.assertEqual(dl.dir_listing(self.test_dir, (self.test1_num,)), (self.test1,))
        self.assertEqual(dl.dir_listing(self.test_dir, self.test2_num), (self.test2,))
        self.assertEqual(dl.dir_listing(self.test_dir, (self.test2_num,)), (self.test2,))
        self.assertEqual(dl.dir_listing(self.test_dir, (self.test1_num, self.test2_num)), (self.test1, self.test2))
        self.assertEqual(dl.dir_listing(self.test_dir, "error"), ())
        self.assertEqual(dl.dir_listing(self.test_dir, exc_targets=self.test1), (self.test2,))
        self.assertEqual(dl.dir_listing(self.test_dir, exc_targets=(self.test1,)), (self.test2,))
        self.assertEqual(dl.dir_listing(self.test_dir, exc_targets=self.test2), (self.test1,))
        self.assertEqual(dl.dir_listing(self.test_dir, exc_targets=(self.test2,)), (self.test1,))
        self.assertEqual(dl.dir_listing(self.test_dir, exc_targets=(self.test1, self.test2)), ())
        self.assertEqual(dl.dir_listing(self.test_dir, exc_targets="error"), (self.test1, self.test2))

    def test_all_listing(self) -> None:
        self.assertEqual(dl.all_listing(self.test_dir), (self.test1, self.test2, self.test_txt, self.test_wav))
        self.assertEqual(dl.all_listing(self.test_dir, self.test1_num), (self.test1,))
        self.assertEqual(dl.all_listing(self.test_dir, (self.test1_num,)), (self.test1,))
        self.assertEqual(dl.all_listing(self.test_dir, self.test2_num), (self.test2,))
        self.assertEqual(dl.all_listing(self.test_dir, (self.test2_num,)), (self.test2,))
        self.assertEqual(dl.all_listing(self.test_dir, self.text_ext), (self.test_txt,))
        self.assertEqual(dl.all_listing(self.test_dir, (self.text_ext,)), (self.test_txt,))
        self.assertEqual(dl.all_listing(self.test_dir, self.wav_ext), (self.test_wav,))
        self.assertEqual(dl.all_listing(self.test_dir, (self.wav_ext,)), (self.test_wav,))
        self.assertEqual(dl.all_listing(self.test_dir, (self.test1_num, self.test2_num)), (self.test1, self.test2))
        self.assertEqual(dl.all_listing(self.test_dir, (self.test1_num, self.wav_ext)), (self.test1, self.test_wav))
        self.assertEqual(dl.all_listing(self.test_dir, (self.test2_num, self.text_ext)), (self.test2, self.test_txt))
        self.assertEqual(dl.all_listing(self.test_dir, (self.text_ext, self.wav_ext)), (self.test_txt, self.test_wav))
        self.assertEqual(
            dl.all_listing(self.test_dir, (self.test1_num, self.test2_num, self.text_ext)),
            (self.test1, self.test2, self.test_txt),
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, (self.test1_num, self.test2_num, self.wav_ext)),
            (self.test1, self.test2, self.test_wav),
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, (self.test1_num, self.text_ext, self.wav_ext)),
            (self.test1, self.test_txt, self.test_wav),
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, (self.test2_num, self.text_ext, self.wav_ext)),
            (self.test2, self.test_txt, self.test_wav),
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, (self.test1_num, self.test2_num, self.text_ext, self.wav_ext)),
            (self.test1, self.test2, self.test_txt, self.test_wav),
        )
        self.assertEqual(dl.all_listing(self.test_dir, "error"), ())
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=self.test1), (self.test2, self.test_txt, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1,)), (self.test2, self.test_txt, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=self.test2), (self.test1, self.test_txt, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test2,)), (self.test1, self.test_txt, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=self.test_txt), (self.test1, self.test2, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test_txt,)), (self.test1, self.test2, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=self.test_wav), (self.test1, self.test2, self.test_txt)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test_wav,)), (self.test1, self.test2, self.test_txt)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test2)), (self.test_txt, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test_txt)), (self.test2, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test_wav)), (self.test2, self.test_txt)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test2, self.test_txt)), (self.test1, self.test_wav)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test2, self.test_wav)), (self.test1, self.test_txt)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test_txt, self.test_wav)), (self.test1, self.test2)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test2, self.test_txt)), (self.test_wav,)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test2, self.test_wav)), (self.test_txt,)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test_txt, self.test_wav)), (self.test2,)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test2, self.test_txt, self.test_wav)), (self.test1,)
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets=(self.test1, self.test2, self.test_txt, self.test_wav)), ()
        )
        self.assertEqual(
            dl.all_listing(self.test_dir, exc_targets="error"), (self.test1, self.test2, self.test_txt, self.test_wav)
        )


if __name__ == "__main__":
    unittest.main()
