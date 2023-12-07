""" module:: tests.test_sm2mpx
    :platform: Any
    :synopsis: Tests for sm2mpx
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import glob
from pathlib import Path

import pytest
from sm2mpx.sm2mpx import Sm2MpxFile, parse_header


@pytest.fixture()
def mock_header():
    debug_header_file = glob.glob("**/data/debug_header.bin", recursive=True)[0]
    with open(debug_header_file, "rb") as f:
        yield f


@pytest.fixture()
def mock_sm2mpx_file(tmp_path, mock_header):
    file_format_version, header_size, file_dict = parse_header(mock_header)
    last_item = file_dict.get(list(file_dict.keys())[-1])
    total_size = last_item.get("offset") + last_item.get("size")
    mock_header.seek(0)
    mock_sm2mpx_path = tmp_path.joinpath("fake.sm2mpx")
    with mock_sm2mpx_path.open("wb") as f:
        f.write(mock_header.read())
        f.write(bytearray(total_size - header_size))
    yield mock_sm2mpx_path


class TestStaticFunctions:
    def test_read_header(self, mock_header):
        file_format_version, header_size, file_dict = parse_header(mock_header)
        assert file_format_version == "SM2MPX10"
        assert header_size == 0x2F0
        assert len(file_dict) == 36


class TestSm2MpxFile:
    def test_sm2mpx_file(self, mock_sm2mpx_file, tmp_path):
        sm = Sm2MpxFile(mock_sm2mpx_file)
        assert sm.file_version
        assert sm.files
        sm.extract_all(output_base_dir=tmp_path)

        sm.check_alignment_and_offset()

        with pytest.raises(ValueError):
            Sm2MpxFile(Path("some_non_existing_path"))
