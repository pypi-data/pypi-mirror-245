"""
module:: sm2mpx.sm2mpx
:platform: Any
:synopsis: SM2MPX format file object
moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
license:: GPL v3

::

    The file format is:
    *****************************
    HEADER with TABLE_OF_CONTENTS
    *****************************
    PAYLOAD / PACKED_FILES
    *****************************

    The header format is:

    *****************************
    ASCII @ 0x0
    FILE_FORMAT_VERSION_STRING
    *****************************
    UINT32BE @ 0x8
    NUMBER_OF_HEADER_ENTRIES
    *****************************
    UINT32BE @ 0x12
    HEADER_SIZE
    *****************************
    ASCII @ 0x10
    RELATIVE_PATH or DIRECTORY
    *****************************
    UINT32BE @ 0x1C
    UNKNOWN_VALUE
    *****************************
    0x20 START_OF_HEADER_ENTRIES
    *****************************
    @HEADER_SIZE START_OF_PAYLOAD

    ALIGNED_FILES to 0x10

    END_OF_FILE
    *****************************


    A HEADER_ENTRY is 20 bytes long:

    *****************************
    ASCII @ 0x0
    FILENAME 12 CHARACTERS
    *****************************
    UINT32BE @ 0x0C
    OFFSET_FROM_FILE_START
    *****************************
    UINT32BE @ 0x10
    FILE_SIZE
    *****************************

"""

from collections import OrderedDict
from pathlib import Path
from stat import S_IRGRP, S_IROTH, S_IXUSR, S_IWUSR, S_IRUSR
from typing import BinaryIO, Tuple


def parse_header(stream: BinaryIO) -> Tuple[str, int, dict]:
    """
    parse a SM2MPX10 packed file header

    Note: The files inside are 0x10 aligned. The header consists of a Folder entry and then file entries.
    :return: The content.
    :rtype: OrderedDict
    """
    stream.seek(0)
    file_format_version = stream.read(8).decode()
    assert file_format_version == "SM2MPX10"
    number_of_header_entries = int.from_bytes(stream.read(4), "little")
    header_size = int.from_bytes(stream.read(4), "little")
    print(hex(header_size))
    rel_dir = Path(stream.read(12).decode().strip("\x00"))
    stream.seek(0x20)
    file_dict = OrderedDict()
    for idx in range(number_of_header_entries):
        name = stream.read(12).decode().strip("\x00")
        offset = int.from_bytes(stream.read(4), "little")
        size = int.from_bytes(stream.read(4), "little")
        rel_path = str(rel_dir.joinpath(Path(name)))

        file_dict.update({name: dict(offset=offset, size=size, rel_path=rel_path)})
    # with Path("debug_header.bin").open("wb") as fp:
    #     stream.seek(0)
    #     fp.write(stream.read(header_size))
    return file_format_version, header_size, file_dict


class Sm2MpxFile:
    """
    A Sm2Mpx10 file.
    """

    def __init__(self, filepath: Path):
        """
        Constructor

        :param filepath: The path to the file.
        :type filepath: Path
        """
        self._stream = None

        self._file_version = None
        self._header_size = None
        self._files = None
        self._stream = None
        if not filepath.exists():
            raise ValueError("Invalid filepath.")
        self.read_file_contents(filepath=filepath)

    @property
    def file_version(self):
        return self._file_version

    @property
    def files(self):
        return self._files

    def read_file_contents(self, filepath):
        """
        Read the file contents.

        :param filepath: The path to the file.
        :type filepath: Path
        """
        self._stream = filepath.open("rb")
        self._file_version, self._header_size, self._files = parse_header(stream=self._stream)

    def extract_file(self, filename: str, output_base_dir: Path) -> None:
        """
        Extract a file to the given destination. It will create directories as needed.

        :param filename: The file to be extracted. It is the key in the files dictionary.
        :type filename: str
        :param output_base_dir: The destination where to extract to.
        :type output_base_dir: Path
        :return: Nothing.
        """
        file_data = self.files.get(filename)

        output_file_path = output_base_dir.joinpath(file_data.get("rel_path"))

        if not output_file_path.parent.exists():
            output_file_path.parent.mkdir(mode=(S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IROTH), parents=True)
        self._stream.seek(file_data.get("offset"))
        print("Writing {0}".format(output_file_path), end="")
        with output_file_path.open("wb") as output_file:
            bytes_written = output_file.write(self._stream.read(file_data.get("size")))
            print(" - Wrote {0} bytes".format(bytes_written))

    def extract_all(self, output_base_dir: Path) -> None:
        """
        Extract all files to the given destination.

        :param output_base_dir: The destination where to extract to.
        :type output_base_dir: Path
        :return: Nothing.
        """
        assert output_base_dir.is_dir()
        for filename in self.files:
            self.extract_file(filename=filename, output_base_dir=output_base_dir)

    def __del__(self):
        if self._stream is not None:
            self._stream.close()

    def check_alignment_and_offset(self) -> None:
        """
        A sanity check if everything is as expected.

        :return: Nothing.
        """
        offset = self._header_size
        offsets_diffs = []
        offsets = []
        for file, data in self.files.items():
            file_offset = data.get("offset")
            self._stream.seek(offset)
            data_bytes = self._stream.read(file_offset - offset)
            assert sum(data_bytes) == 0  # assumption all fill bytes are 0
            offsets_diffs.append(file_offset - offset)
            offsets.append(file_offset)
            offset = file_offset + data.get("size")
        for offset in offsets:
            assert offset % 0x10 == 0  # assumption alignment to 0x10
