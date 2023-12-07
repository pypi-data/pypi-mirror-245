""" module:: tests.test_cryobf
    :platform: Any
    :synopsis: Tests for cryobf
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import glob
from pathlib import Path

import pytest
from cryobf.cryobf import read_header, read_binary_file_tree, CryoBfFile


@pytest.fixture()
def mock_header():
    debug_header_file = glob.glob("**/data/debug_header.bin", recursive=True)[0]
    with open(debug_header_file, "rb") as f:
        yield f


@pytest.fixture()
def mock_file_tree():
    debug_header_file = glob.glob("**/data/debug_file_tree.bin", recursive=True)[0]
    with open(debug_header_file, "rb") as f:
        yield f


@pytest.fixture()
def mock_bf_file(tmp_path, mock_header, mock_file_tree):
    file_version, top_addr, header_size = read_header(mock_header)
    mock_header.seek(0)
    mock_bf_path = tmp_path.joinpath("fake.bf")
    with mock_bf_path.open("wb") as f:
        f.write(mock_header.read())
        f.write(bytearray(top_addr - header_size))
        f.write(mock_file_tree.read())
    yield mock_bf_path


class TestStaticFunctions:
    def test_read_header(self, mock_header):
        file_version, top_addr, header_size = read_header(mock_header)
        assert file_version == "CryoBF - 2.02.0"
        assert top_addr == 14948275
        assert header_size == 32

    def test_read_binary_file_tree(self, mock_file_tree):
        filetree = read_binary_file_tree(mock_file_tree)
        assert len(filetree) == 286


class TestCryoBfFile:

    def test_cryo_bf_file(self, mock_bf_file, tmp_path):
        bf = CryoBfFile(mock_bf_file)
        assert bf.top_addr
        assert bf.file_version
        assert bf.files
        bf.extract_all(output_base_dir=tmp_path)

        with pytest.raises(ValueError):
            CryoBfFile(Path("some_non_existing_path"))
