""" module:: cryobf.cryobf
    :platform: Any
    :synopsis: Cryo BF format file object
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3

    ::

        The file format is:
        **********************
        HEADER
        **********************
        PAYLOAD / PACKED_FILES
        **********************
        TABLE_OF_CONTENTS
        **********************

        The header format is:

        ****************************
        ASCII @ 0x0
        FILE_FORMAT_VERSION_STRING
        ****************************
        0x10
        UNKNOWN_BLOCK
        ****************************
        UINT32LE @ 0x18
        ADDRESS_OF_TABLE_OF_CONTENTS
        UINT32LE @ 0x1C
        SIZE_OF_HEADER - always 0x20
        ****************************

        The table of contents is a file tree.
        It starts with a branch Node.

        The node format is:

        ******************************
        UINT32LE
        NUMBER_OF_SUB_ELEMENTS
        ******************************
        UINT32LE
        LENGTH_OF_THE_FOLLOWING_STRING
        ******************************
        ASCII
        THE_NAME_OF_THE_NODE
        ******************************
        UINT32LE
        THE_TYPE_OF_THE_NODE
        1 = directory / Branch Node
        2 = file / Leaf Node
        ******************************

        A branch node ends here while the leaf node continues with it's properties.

        ******************************
        UINT32LE
        FILE_SIZE
        ******************************
        UINT32LE
        UNKNOWN_VALUE, always 0
        ******************************
        UINT32LE
        FILE_OFFSET, from header!!!!!!
        ******************************

        A leaf node ends here.
"""

from enum import IntEnum
from stat import S_IRGRP, S_IROTH, S_IXUSR, S_IWUSR, S_IRUSR
from pathlib import Path
from typing import BinaryIO, Optional, Tuple


class ContentType(IntEnum):
    Directory = 1
    File = 2


def read_header(stream: BinaryIO, ) -> Tuple[str, int, int]:
    """
    Read the file header.

    :return: A tuple of (file_version, top_addr, header_size).
    :rtype: Tuple[str, int, int]
    """
    stream.seek(0)
    data = stream.read(0x20)
    file_version = data[:15].decode()
    top_addr = int.from_bytes(data[-8:-4], "little")
    header_size = int.from_bytes(data[-4:], "little")
    return file_version, top_addr, header_size


def read_binary_file_tree(stream: BinaryIO,
                          top_addr: Optional[int] = None,
                          header_size: int = 0x20,
                          relpath: Path = Path()) -> dict:
    """
    Read the binary file tree.

    This is a recursive function, called on each branch's root node.

    :param stream: The stream from which to read.
    :type stream: BinaryIO
    :param top_addr: The address of the table of contents. If it's not None, the stream seeks that position.
                     This parameter should be omitted when the function is called recursively.
                     This parameter should be set if the function is called the first time.
    :param header_size: The size of the file header. It is added to the file_offset of each file.
    :type header_size: int
    :param relpath: The joined relative path from the root node.
                    It is used to fill the rel_path dictionary entry for each file.
    :type relpath: Path
    :return: The items below the current tree node.
    :rtype: dict
    """
    if top_addr is not None:
        stream.seek(top_addr)
    elems = {}
    number_of_sub_items = int.from_bytes(stream.read(4), "little")
    for i in range(number_of_sub_items):
        str_len = int.from_bytes(stream.read(4), "little")
        file_name = stream.read(str_len).decode()

        type_ = ContentType(int.from_bytes(stream.read(4), "little"))

        if type_ == ContentType.File:
            size = int.from_bytes(stream.read(4), "little")
            number_of_sub_items = int.from_bytes(stream.read(4), "little")
            assert number_of_sub_items == 0
            file_offset = int.from_bytes(stream.read(4), "little") + header_size
            elem = {
                "file_name": file_name,
                "rel_path": str(relpath.joinpath(Path(file_name))),
                "size": size,
                "offset": file_offset,
            }
            elems.update({elem.pop("file_name"): elem})

        elif type_ == ContentType.Directory:
            sub_items = read_binary_file_tree(stream=stream, relpath=relpath.joinpath(file_name))
            elems.update(sub_items)
    return elems


class CryoBfFile:
    """
    A Cryo BF file.
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
        self._top_addr = None
        self._files = None
        self._stream = None
        if not filepath.exists():
            raise ValueError("Invalid filepath.")
        self.read_file_contents(filepath=filepath)

    @property
    def top_addr(self):
        return self._top_addr

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
        self._file_version, self._top_addr, self._header_size = read_header(stream=self._stream)
        self._files = read_binary_file_tree(stream=self._stream, top_addr=self.top_addr, header_size=self._header_size)

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

    def __del__(self):
        if self._stream is not None:
            self._stream.close()
