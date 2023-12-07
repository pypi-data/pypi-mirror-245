from pathlib import Path
import construct as cs
import fire

class DSKImage:
    """
    Represents a DSK (Disk) Image.

    Attributes:
        _dskFilePath (Path): The path to the DSK file.
        _fatType (str): The type of FAT (File Allocation Table) used in the DSK image.
        _DSKStruct (cs.Struct): The parsed structure of the DSK image.
        fatLinks (dict): A dictionary containing the FAT links for each cluster.
        files (dict): A dictionary containing the files and directories in the DSK image.

    Methods:
        parseFAT(): Parses the FAT entries in the DSK image.
        getBityesFromCluster(cluster_index: int, size: int = 0) -> bytearray: Retrieves the bytes from a specific cluster in the DSK image.
        getDirectoryStruct(cluster_index: int, size: int): Retrieves the directory structure from a specific cluster in the DSK image.
        parseFilesDirectory(directory: str, cluster_index: int): Parses the files and directories in a specific directory cluster.
        parseFiles(): Parses all the files and directories in the DSK image.
        parse(): Parses the entire DSK image.
        files(): Returns the files and directories in the DSK image.
    """

    def _BootSectorStruct(self) -> cs.Struct:
        """
        Returns a Struct object representing the structure of a boot sector.

        Returns:
            cs.Struct: The boot sector structure.
        """
        return cs.Struct(
            "8086JumpCode" / cs.Bytes(0x03),
            "OEMName" / cs.PaddedString(8, "ascii"),
            "SectorSize" / cs.Int16ul,
            "ClusterSize" / cs.Int8ul,
            "FATSector" / cs.Int16ul,
            "FATCount" / cs.Int8ul,
            "RootDirectoryEntries" / cs.Int16ul,
            "TotalSectors" / cs.Int16ul,
            "MediaID" / cs.Int8ul,
            "FATSize" / cs.Int16ul,
            "SectorsPerTrack" / cs.Int16ul,
            "HeadCount" / cs.Int16ul,
            "HiddenSectors" / cs.Int16ul,
            "MSXDOS2Boot" / cs.Byte,
            "JumpCode" / cs.Byte,
            "VOL_ID" / cs.PaddedString(6, "ascii"),
            "SystemUse" / cs.Byte,
            "VolumeID" / cs.Bytes(4),
            "Reserved" / cs.Padding(5),
        )

    def _RootDirectoryStruct(self, rootDirectoryEntries: int) -> cs.Struct:
        """
        Returns a Struct object representing the structure of the root directory entries.

        Args:
            rootDirectoryEntries (int): The number of root directory entries.

        Returns:
            cs.Struct: The structure of the root directory entries.
        """

        return cs.Struct(
            "Entries"
            / cs.Array(
                rootDirectoryEntries,
                cs.Struct(
                    "Identifier" / cs.Bytes(11),
                    "Deleted"
                    / cs.IfThenElse(
                        cs.this.Identifier[0] == 0xE5,
                        cs.Computed(True),
                        cs.Computed(False),
                    ),
                    "FileName"
                    / cs.IfThenElse(
                        cs.this.Deleted,
                        cs.Computed(cs.this.Identifier[1:7]),
                        cs.Computed(cs.this.Identifier[0:7]),
                    ),
                    "Extension" / cs.Computed(cs.this.Identifier[8:11]),
                    "Attribute"
                    / cs.BitStruct(
                        cs.Padding(2),
                        "Archive" / cs.Flag,
                        "Directory" / cs.Flag,
                        "VolumeLabel" / cs.Flag,
                        "System" / cs.Flag,
                        "Hidden" / cs.Flag,
                        "ReadOnly" / cs.Flag,
                    ),
                    cs.If(
                        cs.this.Attribute.VolumeLabel,
                        "VolumeLabel" / cs.Computed(cs.this.Identifier[0:7]),
                    ),
                    cs.Padding(1),
                    "Reserved" / cs.Bytes(9),
                    "Time"
                    / cs.Struct(
                        "Field" / cs.Int16ul,
                        "Hour" / cs.Computed(cs.this.Field >> 11),
                        "Minute" / cs.Computed((cs.this.Field >> 5) & 0x3F),
                        "Second" / cs.Computed((cs.this.Field & 0x1F) * 2),
                    ),
                    "Date"
                    / cs.Struct(
                        "Field" / cs.Int16ul,
                        "Year" / cs.Computed((cs.this.Field >> 9) + 1980),
                        "Month" / cs.Computed((cs.this.Field >> 5) & 0xF),
                        "Day" / cs.Computed(cs.this.Field & 0x1F),
                    ),
                    "FirstCluster" / cs.Int16ul,
                    "FileSize" / cs.Int32ul,
                ),
            )
        )

    def _FATStruct(
        self, fatType: str, fatSize: int, sectorSize: int, fatCount: int
    ) -> cs.Struct:
        """
        Create a Struct object for parsing FAT entries based on the FAT type.

        Args:
            fatType (str): The type of FAT (FAT12 or FAT16).
            fatSize (int): The size of each FAT entry in bytes.
            sectorSize (int): The size of each sector in bytes.
            fatCount (int): The number of FATs in the disk image.

        Returns:
            cs.Struct: The Struct object for parsing FAT entries.

        Raises:
            ValueError: If the FAT type is not supported.
        """

        if fatType == "FAT12":
            return cs.Struct(
                "FAT_ID" / cs.Byte,
                "Dummy" / cs.Bytes(2),
                "Entries" / cs.Bytes(fatSize * sectorSize * fatCount - 3),
            )
        elif fatType == "FAT16":
            return cs.Struct(
                "FAT_ID" / cs.Bytes(2),
                "Dummy" / cs.Bytes(2),
                "Entries" / cs.Bytes(fatSize * sectorSize * fatCount - 4),
            )
        else:
            raise ValueError("FAT Type Error")

    def _DATAClusterStruct(self, clusterSize: int, sectorSize: int) -> cs.Struct:
        """
        Create a data cluster structure.

        Args:
            clusterSize (int): The size of the cluster.
            sectorSize (int): The size of each sector.

        Returns:
            cs.Struct: The data cluster structure.

        """
        return cs.Struct(
            "ID" / cs.Computed(cs.this._index + 2),
            "Data" / cs.Bytes(clusterSize * sectorSize),
        )

    def _DSKImageStruct(
        self,
        sectorSize: int,
        clusterSize: int,
        fatType: str,
        fatSize: int,
        fatCount: int,
        rootDirectoryEntries: int,
        totalSectors: int,
    ) -> cs.Struct:
        """
        Creates a structured representation of a DSK image.

        Args:
            sectorSize (int): The size of each sector in bytes.
            clusterSize (int): The size of each cluster in sectors.
            fatType (str): The type of FAT (File Allocation Table) used.
            fatSize (int): The size of each FAT in sectors.
            fatCount (int): The number of FATs in the image.
            rootDirectoryEntries (int): The number of entries in the root directory.
            totalSectors (int): The total number of sectors in the image.

        Returns:
            cs.Struct: A structured representation of the DSK image.
        """
        return cs.AlignedStruct(
            sectorSize,
            "BootSector" / self._BootSectorStruct(),
            "FAT" / self._FATStruct(fatType, fatSize, sectorSize, fatCount),
            "RootDirectory" / self._RootDirectoryStruct(rootDirectoryEntries),
            "DATA"
            / cs.Array(
                (totalSectors - 1) // clusterSize - rootDirectoryEntries // clusterSize,
                self._DATAClusterStruct(clusterSize, sectorSize),
            ),
        )

    def __init__(self, dskFile: str, fatType: str = "FAT12"):
        self._dskFilePath: Path = Path(dskFile)
        self._fatType: str = fatType
        self._DSKStruct: cs.Struct = None
        self.fatLinks = {}
        self.files = {}
        if self._dskFilePath.exists() == False:
            raise FileNotFoundError("DSK File Not Found")

    def parseFAT(self):
        """
        Parses the File Allocation Table (FAT) entries and populates the `fatLinks` dictionary.

        Returns:
            None
        """
        if self._fatType == "FAT12":
            fatEntryStruct = cs.Struct(
                "entries" / cs.Bytes(3),
                "entry1"
                / cs.Computed(cs.this.entries[0] + (cs.this.entries[1] & 0x0F) * 0x100),
                "entry2"
                / cs.Computed(
                    (cs.this.entries[2] * 0x10) + ((cs.this.entries[1] & 0xF0) >> 4)
                ),
            )

            count = 0
            fatSize = (
                self._DSKStruct.BootSector.FATSize
                * self._DSKStruct.BootSector.SectorSize
            )
            fatEntries = self._DSKStruct.FAT.Entries
            entrlyList = []

            while count + 3 < fatSize:
                fatBytes = fatEntryStruct.parse(fatEntries[count : count + 3])
                entrlyList.append(fatBytes.entry1)
                entrlyList.append(fatBytes.entry2)
                count += 3

            cursor = 0
            while cursor < len(entrlyList):
                if entrlyList[cursor] == 0x00:
                    cursor += 1
                    continue
                key = cursor + 2
                self.fatLinks[key] = [key]
                if entrlyList[cursor] == 0xFFF:
                    cursor += 1
                    continue
                while entrlyList[cursor] != 0xFFF:
                    self.fatLinks[key].append(entrlyList[cursor])
                    cursor += 1
        elif self._fatType == "FAT16":
            fatEntryStruct = cs.Array(
                self._DSKStruct.BootSector.FATSize * self._DSKStruct.BootSector.SectorSize  // 2,
                "entry" / cs.Int16ul
            )
            fatBytes = fatEntryStruct.parse(self._DSKStruct.FAT.Entries)
            cursor = 0
            while cursor < len(fatBytes):
                if fatBytes[cursor] == 0x0000:
                    cursor += 1
                    continue
                key = cursor + 2
                self.fatLinks[key] = [key]
                if fatBytes[cursor] == 0xFFFF:
                    cursor += 1
                    continue
                linkCursor = cursor
                while fatBytes[linkCursor] != 0xFFFF:
                    self.fatLinks[key].append(fatBytes[linkCursor])
                    linkCursor = fatBytes[linkCursor]

    def getBityesFromCluster(self, cluster_index: int, size: int = 0) -> bytearray:
        """
        Retrieves the bytes from the specified cluster index.

        Args:
            cluster_index (int): The index of the cluster to retrieve the bytes from.
            size (int, optional): The maximum size of the retrieved bytes. Defaults to 0, which retrieves all bytes.

        Returns:
            bytearray: The retrieved bytes from the cluster.
        """
        if not cluster_index in self.fatLinks.keys():
            return None
        data: bytearray = bytearray()
        for cluster in self.fatLinks[cluster_index]:
            data += self._DSKStruct.DATA[cluster - 2].Data
        if size == 0:
            return data
        return data[:size]

    def getBityesFromFilePath(self, filePath: str) -> bytearray:
        """
        Retrieves the bytes from a file path.

        Args:
            filePath (str): The file path to retrieve the bytes from.

        Returns:
            bytearray: The retrieved bytes from the file path.
        """
        if filePath[0] != "/":
            filePath = "/" + filePath
        filePath = filePath.upper()
        print("get :" + filePath)
        for directory in self.files.keys():
            for file in self.files[directory]:
                if directory == "/":
                    if filePath == "/{}.{}".format(
                        (file.FileName).decode(encoding="ascii").rstrip(" "),
                        (file.Extension).decode(encoding="ascii").rstrip(" "),
                    ):
                        return self.getBityesFromCluster(
                            file.FirstCluster, file.FileSize
                        )
                else:
                    test = "{}/{}.{}".format(                      
                        directory.rstrip(" "),
                        (file.FileName).decode(encoding="ascii").rstrip(" "),
                        (file.Extension).decode(encoding="ascii").rstrip(" "),
                    )
                    if filePath == "{}/{}.{}".format(
                        directory.rstrip(" "),
                        (file.FileName).decode(encoding="ascii").rstrip(" "),
                        (file.Extension).decode(encoding="ascii").rstrip(" "),
                    ):
                        return self.getBityesFromCluster(
                            file.FirstCluster, file.FileSize
                        )
        return None

    def getDirectoryStruct(self, cluster_index: int, size: int):
        """
        Retrieve the directory structure from a given cluster index.

        Args:
            cluster_index (int): The index of the cluster.
            size (int): The size of the directory structure.

        Returns:
            RootDirectoryStruct: The parsed directory structure.
        """
        if not cluster_index in self.fatLinks.keys():
            return None
        data: bytearray = self.getBityesFromCluster(cluster_index, size)
        return self._RootDirectoryStruct(
            self._DSKStruct.BootSector.RootDirectoryEntries
        ).parse(data)

    def parseFilesDirectory(self, directory: str, cluster_index: int):
        """
        Recursively parses the files in a directory and stores them in the 'files' dictionary.

        Args:
            directory (str): The directory path.
            cluster_index (int): The cluster index.

        Returns:
            None
        """
        self.files[directory] = []
        clusterData = self.getBityesFromCluster(cluster_index, 0)
        if clusterData == None:
            return
        for file in (
            self._RootDirectoryStruct(len(clusterData) // 32).parse(clusterData).Entries
        ):
            if file.Identifier[0] == 0x00:
                continue
            if file.Identifier[0] == 0xE5:
                continue
            if file.Deleted:
                continue
            if file.Attribute.Directory:
                if file.FileName.decode("ascii").rstrip(" ") == ".":
                    continue
                if file.FileName.decode("ascii").rstrip(" ") == "..":
                    continue
                if cluster_index != file.FirstCluster and file.FirstCluster != 0:
                    self.parseFilesDirectory(
                        directory + "/" + file.FileName.decode("ascii"),
                        file.FirstCluster,
                    )
            else:
                self.files[directory].append(file)

    def parseFiles(self):
        """
        Parses the files in the DSKStruct.RootDirectory and stores them in the self.files dictionary.

        Returns:
            None
        """
        self.files["/"] = []
        for file in self._DSKStruct.RootDirectory.Entries:
            if file.Identifier[0] == 0x00:
                continue
            if file.Identifier[0] == 0xE5:
                continue
            if file.Deleted:
                continue
            if file.Attribute.Directory:
                self.parseFilesDirectory(
                    "/" + file.FileName.decode("ascii"), file.FirstCluster
                )
            else:
                self.files["/"].append(file)

    def parse(self):
        """
        Parses the DSK image file and extracts necessary information.
        """
        bootSector = self._BootSectorStruct().parse_file(self._dskFilePath.absolute())
        self._DSKStruct = self._DSKImageStruct(
            bootSector.SectorSize,
            bootSector.ClusterSize,
            self._fatType,
            bootSector.FATSize,
            bootSector.FATCount,
            bootSector.RootDirectoryEntries,
            bootSector.TotalSectors,
        ).parse_file(self._dskFilePath.absolute())
        self.parseFAT()
        self.parseFiles()

    def files(self):
        return self.files


class DSKtool(object):
    """
    DSKtool class provides methods for listing and retrieving files from a DSK image.
    """

    def list(self, dskFile: str, fattype: str = "FAT12"):
        """
        Lists all files in the DSK image.

        Parameters:
        - dskFile (str): The path to the DSK image file.
        - fattype (str): The FAT type of the DSK image. Default is "FAT12".
        """
        dskImage = DSKImage(dskFile, fatType=fattype)
        dskImage.parse()
        for directory in dskImage.files.keys():
            for file in dskImage.files[directory]:
                if directory == "/":
                    print(
                        "{}.{}".format(
                            (file.FileName).decode(encoding="ascii").rstrip(" "),
                            (file.Extension).decode(encoding="ascii").rstrip(" "),
                        ),
                    )
                else:
                    print(
                        "{}/{}.{}".format(
                            directory.rstrip(" "),
                            (file.FileName).decode(encoding="ascii").rstrip(" "),
                            (file.Extension).decode(encoding="ascii").rstrip(" "),
                        ),
                    )

    def get(self, dskFile: str, target: str, fattype: str = "FAT12"):
        """
        Retrieves a specific file from the DSK image.

        Parameters:
        - dskFile (str): The path to the DSK image file.
        - target (str): The name of the file to retrieve.
        - fattype (str): The FAT type of the DSK image. Default is "FAT12".
        """
        target = target.upper()
        dskImage = DSKImage(dskFile, fatType=fattype)
        dskImage.parse()
        for directory in dskImage.files.keys():
            for file in dskImage.files[directory]:
                if directory == "/":
                    if target == "{}.{}".format(
                        (file.FileName).decode(encoding="ascii").rstrip(" "),
                        (file.Extension).decode(encoding="ascii").rstrip(" "),
                    ):
                        print(
                            "{}.{} {}Byte".format(
                                (file.FileName).decode(encoding="ascii").rstrip(" "),
                                (file.Extension).decode(encoding="ascii").rstrip(" "),
                                file.FileSize,
                            ),
                        )

                        with open(
                            "{}.{}".format(
                                (file.FileName).decode(encoding="ascii").rstrip(" "),
                                (file.Extension).decode(encoding="ascii").rstrip(" "),
                            ),
                            "wb",
                        ) as f:
                            f.write(
                                dskImage.getBityesFromCluster(
                                    file.FirstCluster, file.FileSize
                                )
                            )

                else:
                    if target == "{}/{}.{} {}Byte".format(
                        directory.rstrip(" "),
                        (file.FileName).decode(encoding="ascii").rstrip(" "),
                        (file.Extension).decode(encoding="ascii").rstrip(" "),
                        file.FileSize,
                    ):
                        print(
                            "{}/{}.{}".format(
                                directory.rstrip(" "),
                                (file.FileName).decode(encoding="ascii").rstrip(" "),
                                (file.Extension).decode(encoding="ascii").rstrip(" "),
                            ),
                        )

                        with open(
                            "{}.{}".format(
                                (file.FileName).decode(encoding="ascii").rstrip(" "),
                                (file.Extension).decode(encoding="ascii").rstrip(" "),
                            ),
                            "wb",
                        ) as f:
                            f.write(
                                dskImage.getBityesFromCluster(
                                    file.FirstCluster, file.FileSize
                                )
                            )

if __name__ == "__main__":
    fire.Fire(DSKtool)
