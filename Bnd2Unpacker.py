import os
import sys
import zlib
import struct

OutputNewFileType = True

ItemTypeDict = {"01_00_00_00": "Texture",
                "02_00_00_00": "Material",
                "03_00_00_00": "VertexDescriptor",
                "04_00_00_00": "VertexProgramState",
                "05_00_00_00": "Renderable",
                "06_00_00_00": "MaterialState",
                "07_00_00_00": "SamplerState",
                "08_00_00_00": "ShaderProgramBuffer",
                "12_00_00_00": "GenesysType.",
                "13_00_00_00": "GenesysObject",
                "14_00_00_00": "GenesysType.",
                "15_00_00_00": "GenesysObject",
                "30_00_00_00": "Font",
                "50_00_00_00": "InstanceList",
                "51_00_00_00": "Model",
                "52_00_00_00": "ColorCube",
                "53_00_00_00": "Shader",
                "60_00_00_00": "PolygonSoupList",
                "70_00_00_00": "TextFile",
                "74_00_00_00": "LuaData",
                "80_00_00_00": "Ginsu",
                "81_00_00_00": "Wave",
                "83_00_00_00": "GameplayLinkData",
                "84_00_00_00": "WaveDictionary",
                "86_00_00_00": "Reverb",
                "90_00_00_00": "ZoneList",
                "91_00_00_00": "WorldPaintMap",
                "B0_00_00_00": "AnimationList",
                "B2_00_00_00": "Skeleton",
                "B3_00_00_00": "Animation",
                "C0_00_00_00": "CgsVertexProgramState",
                "C1_00_00_00": "CgsProgramBuffer",
                "05_01_00_00": "VehicleList",
                "06_01_00_00": "GraphicsSpec",
                "00_02_00_00": "AIData",
                "01_02_00_00": "Language",
                "02_02_00_00": "TriggerData",
                "03_02_00_00": "RoadData",
                "04_02_00_00": "DynamicInstanceList",
                "05_02_00_00": "WorldObject",
                "06_02_00_00": "ZoneHeader",
                "07_02_00_00": "VehicleSound",
                "09_02_00_00": "CharacterSpec",
                "13_02_00_00": "LightInstanceList",
                "14_02_00_00": "GroundcoverInstances",
                "15_02_00_00": "CompoundObject",
                "16_02_00_00": "CompoundInstanceList",
                "17_02_00_00": "PropObject",
                "18_02_00_00": "PropInstanceList",
                "19_02_00_00": "ZoneAmbienceListDataType",
                "0D_02_00_00": "CameraTake",
                "0E_02_00_00": "CameraTakeList",
                "01_03_00_00": "BearEffect",
                "02_03_00_00": "BearGlobalParameters",
                "03_03_00_00": "ConvexHull",
                "01_05_00_00": "HSMData",
                "01_07_00_00": "TrafficData"}

Bnd2PathList = sys.argv[1:]
for Bnd2Path in Bnd2PathList:
    OutputPath = Bnd2Path[:Bnd2Path.find(".")]
    Bnd2 = open(Bnd2Path, "rb").read().hex()
    Byte = Bnd2[8:16]
    if Byte == "05000100":
        Game = "Need For Speed Most Wanted 2012"
        Platform = "PC"
    elif Byte == "00050002":
        Game = "Need For Speed Most Wanted 2012"
        Platform = "PS3"
    elif Byte == "03000000":
        Game = "Need For Speed Hot Pursuit 2010"
        Platform = "PC"
    else:
        Game = "Unknow"
        Platform = "Unknow"
        exit()

    if Game == "Need For Speed Most Wanted 2012" and Platform == "PC":
        ItemCount = struct.unpack("<L", bytes.fromhex(Bnd2[24:32]))[0]
        ItemInfoAreaOffset = struct.unpack("<L", bytes.fromhex(Bnd2[32:40]))[0]
        MainFileBlockAreaOffset = struct.unpack("<L", bytes.fromhex(Bnd2[40:48]))[0]
        SubBlockAreaOffset = struct.unpack("<L", bytes.fromhex(Bnd2[48:56]))[0]
        CompressionLevel = struct.unpack("<L", bytes.fromhex(Bnd2[72:80]))[0]
        for ItemNum in range(ItemCount):
            Offset = (ItemInfoAreaOffset + 72 * ItemNum) * 2
            ItemName = Bnd2[Offset:Offset + 8].upper()
            ItemName = '_'.join([ItemName[x:x + 2] for x in range(0, len(ItemName), 2)])
            ItemNameSuffix1 = struct.unpack("<B", bytes.fromhex(Bnd2[Offset + 8:Offset + 10]))[0]
            ItemNameSuffix2 = struct.unpack("<B", bytes.fromhex(Bnd2[Offset + 12:Offset + 14]))[0]
            if ItemNameSuffix1 != 0 and ItemNameSuffix2 != 0:
                ItemName += "_" + str(ItemNameSuffix1) + "_" + str(ItemNameSuffix2)
            elif ItemNameSuffix1 == 0 and ItemNameSuffix2 != 0:
                ItemName += "_0_" + str(ItemNameSuffix2)
            elif ItemNameSuffix1 != 0 and ItemNameSuffix2 == 0:
                ItemName += "_" + str(ItemNameSuffix1)
            MainFileDecompressionSize = struct.unpack("<L", bytes.fromhex(Bnd2[Offset + 16:Offset + 22] + "00"))[0]
            SubFileDecompressionSize = struct.unpack("<L", bytes.fromhex(Bnd2[Offset + 24:Offset + 30] + "00"))[0]
            MainFileCompressionSize = struct.unpack("<L", bytes.fromhex(Bnd2[Offset + 48:Offset + 56]))[0]
            SubFileCompressionSize = struct.unpack("<L", bytes.fromhex(Bnd2[Offset + 56:Offset + 64]))[0]
            MainFileBlockOffset = struct.unpack("<L", bytes.fromhex(Bnd2[Offset + 80:Offset + 88]))[0]
            SubFileBlockOffset = struct.unpack("<L", bytes.fromhex(Bnd2[Offset + 88:Offset + 96]))[0]
            ItemType = Bnd2[Offset + 120:Offset + 128].upper()
            ItemType = '_'.join([ItemType[x:x + 2] for x in range(0, len(ItemType), 2)])
            if OutputNewFileType == True:
                ItemType = ItemTypeDict[ItemType]
            CompressData1 = bytes.fromhex(Bnd2[(MainFileBlockAreaOffset + MainFileBlockOffset) * 2:(MainFileBlockAreaOffset + MainFileBlockOffset + MainFileCompressionSize) * 2])
            DecompressData1 = zlib.decompressobj().decompress(CompressData1)
            OutputTypePath = OutputPath + "\\" + ItemType
            if not os.path.exists(OutputTypePath):
                os.makedirs(OutputTypePath)
            Output = open(OutputTypePath + "\\" + ItemName + ".dat", "wb")
            Output.write(DecompressData1)
            Output.close()
            if SubFileDecompressionSize != 0:
                SubFileCompressData = bytes.fromhex(Bnd2[(SubBlockAreaOffset + SubFileBlockOffset) * 2:(SubBlockAreaOffset + SubFileBlockOffset + SubFileCompressionSize) * 2])
                SubFileDecompressData = zlib.decompressobj().decompress(SubFileCompressData)
                if ItemType == "05_00_00_00" or ItemType == "Renderable":
                    Output = open(OutputTypePath + "\\" + ItemName + "_model.dat", "wb")
                elif ItemType == "01_00_00_00" or ItemType == "Texture":
                    Output = open(OutputTypePath + "\\" + ItemName + "_texture.dat", "wb")
                else:
                    Output = open(OutputTypePath + "\\" + ItemName + "_unknow.dat", "wb")
                Output.write(SubFileDecompressData)
                Output.close()
        IDs = bytes.fromhex(Bnd2[:MainFileBlockAreaOffset * 2])
        Output = open(OutputPath + "\\" + "IDs.BIN", "wb")
        Output.write(IDs)
        Output.close()
    if Game == "Need For Speed Most Wanted 2012" and Platform == "PS3":
        ItemCount = struct.unpack(">L", bytes.fromhex(Bnd2[24:32]))[0]
        ItemInfoAreaOffset = struct.unpack(">L", bytes.fromhex(Bnd2[32:40]))[0]
        MainFileBlockAreaOffset = struct.unpack(">L", bytes.fromhex(Bnd2[40:48]))[0]
        SubBlockAreaOffset = struct.unpack(">L", bytes.fromhex(Bnd2[48:56]))[0]
        CompressionLevel = struct.unpack(">L", bytes.fromhex(Bnd2[72:80]))[0]
        for ItemNum in range(ItemCount):
            Offset = (ItemInfoAreaOffset + 72 * ItemNum) * 2
            ItemName = Bnd2[Offset + 8:Offset + 16].upper()
            ItemName = '_'.join([ItemName[x:x + 2] for x in range(0, len(ItemName), 2)])
            ItemNameSuffix1 = struct.unpack(">B", bytes.fromhex(Bnd2[Offset + 2:Offset + 4]))[0]
            ItemNameSuffix2 = struct.unpack(">B", bytes.fromhex(Bnd2[Offset + 6:Offset + 8]))[0]
            if ItemNameSuffix2 != 0 and ItemNameSuffix1 != 0:
                ItemName += "_" + str(ItemNameSuffix2) + "_" + str(ItemNameSuffix1)
            elif ItemNameSuffix2 == 0 and ItemNameSuffix1 != 0:
                ItemName += "_0_" + str(ItemNameSuffix1)
            elif ItemNameSuffix2 != 0 and ItemNameSuffix1 == 0:
                ItemName += "_" + str(ItemNameSuffix2)
            MainFileDecompressionSize = struct.unpack(">L", bytes.fromhex("00" + Bnd2[Offset + 18:Offset + 24]))[0]
            SubFileDecompressionSize = struct.unpack(">L", bytes.fromhex("00" + Bnd2[Offset + 34:Offset + 40]))[0]
            MainFileCompressionSize = struct.unpack(">L", bytes.fromhex(Bnd2[Offset + 48:Offset + 56]))[0]
            SubFileCompressionSize = struct.unpack(">L", bytes.fromhex(Bnd2[Offset + 64:Offset + 72]))[0]
            MainFileBlockOffset = struct.unpack(">L", bytes.fromhex(Bnd2[Offset + 80:Offset + 88]))[0]
            SubFileBlockOffset = struct.unpack(">L", bytes.fromhex(Bnd2[Offset + 96:Offset + 104]))[0]
            ItemType = Bnd2[Offset + 120:Offset + 128].upper()
            ItemType = '_'.join([ItemType[x:x + 2] for x in range(0, len(ItemType), 2)])
            if OutputNewFileType == True:
                ItemType = ItemTypeDict[ItemType[9:11] + "_" + ItemType[6:8] + "_" + ItemType[3:5] + "_" + ItemType[:2]]
            CompressData1 = bytes.fromhex(Bnd2[(MainFileBlockAreaOffset + MainFileBlockOffset) * 2:(MainFileBlockAreaOffset + MainFileBlockOffset + MainFileCompressionSize) * 2])
            DecompressData1 = zlib.decompressobj().decompress(CompressData1)
            OutputTypePath = OutputPath + "\\" + ItemType
            if not os.path.exists(OutputTypePath):
                os.makedirs(OutputTypePath)
            Output = open(OutputTypePath + "\\" + ItemName + ".dat", "wb")
            Output.write(DecompressData1)
            Output.close()
            if SubFileDecompressionSize != 0:
                SubFileCompressData = bytes.fromhex(Bnd2[(SubBlockAreaOffset + SubFileBlockOffset) * 2:(SubBlockAreaOffset + SubFileBlockOffset + SubFileCompressionSize) * 2])
                SubFileDecompressData = zlib.decompressobj().decompress(SubFileCompressData)
                if ItemType == "00_00_00_05" or ItemType == "Renderable":
                    Output = open(OutputTypePath + "\\" + ItemName + "_model.dat", "wb")
                elif ItemType == "00_00_00_01" or ItemType == "Texture":
                    Output = open(OutputTypePath + "\\" + ItemName + "_texture.dat", "wb")
                else:
                    Output = open(OutputTypePath + "\\" + ItemName + "_unknow.dat", "wb")
                Output.write(SubFileDecompressData)
                Output.close()
        IDs = bytes.fromhex(Bnd2[:MainFileBlockAreaOffset * 2])
        Output = open(OutputPath + "\\" + "IDs.BIN", "wb")
        Output.write(IDs)
        Output.close()
    elif Game == "Need For Speed Hot Pursuit 2010" and Platform == "PC":
        ItemCount = struct.unpack("<L", bytes.fromhex(Bnd2[32:40]))[0]
        ItemInfoAreaOffset = struct.unpack("<L", bytes.fromhex(Bnd2[40:48]))[0]
        MainFileBlockAreaOffset = struct.unpack("<L", bytes.fromhex(Bnd2[48:56]))[0]
        SubBlockAreaOffset = struct.unpack("<L", bytes.fromhex(Bnd2[56:64]))[0]
        Block3AreaOffset = struct.unpack("<L", bytes.fromhex(Bnd2[64:72]))[0]
        Block4AreaOffset = struct.unpack("<L", bytes.fromhex(Bnd2[72:80]))[0]
        CompressionLevel = struct.unpack("<L", bytes.fromhex(Bnd2[80:88]))[0]
        for ItemNum in range(ItemCount):
            Offset = (ItemInfoAreaOffset + 80 * ItemNum) * 2
            ItemName = Bnd2[Offset:Offset + 8].upper()
            ItemName = '_'.join([ItemName[x:x + 2] for x in range(0, len(ItemName), 2)])
            ItemNameSuffix1 = struct.unpack("<B", bytes.fromhex(Bnd2[Offset + 8:Offset + 10]))[0]
            ItemNameSuffix2 = struct.unpack("<B", bytes.fromhex(Bnd2[Offset + 12:Offset + 14]))[0]
            MainFileDecompressionSize = struct.unpack("<L", bytes.fromhex(Bnd2[Offset + 32:Offset + 38] + "00"))[0]
            SubFileDecompressionSize = struct.unpack("<L", bytes.fromhex(Bnd2[Offset + 40:Offset + 46] + "00"))[0]
            MainFileCompressionSize = struct.unpack("<L", bytes.fromhex(Bnd2[Offset + 64:Offset + 72]))[0]
            SubFileCompressionSize = struct.unpack("<L", bytes.fromhex(Bnd2[Offset + 72:Offset + 80]))[0]
            MainFileBlockOffset = struct.unpack("<L", bytes.fromhex(Bnd2[Offset + 96:Offset + 104]))[0]
            SubFileBlockOffset = struct.unpack("<L", bytes.fromhex(Bnd2[Offset + 104:Offset + 112]))[0]
            ItemType = Bnd2[Offset + 136:Offset + 144].upper()
            ItemType = '_'.join([ItemType[x:x + 2] for x in range(0, len(ItemType), 2)])
            if OutputNewFileType == True:
                ItemType = ItemTypeDict[ItemType]
            if ItemNameSuffix1 != 0 and ItemNameSuffix2 != 0:
                ItemName += "_" + str(ItemNameSuffix1) + "_" + str(ItemNameSuffix2)
            elif ItemNameSuffix1 == 0 and ItemNameSuffix2 != 0:
                ItemName += "_0_" + str(ItemNameSuffix2)
            elif ItemNameSuffix1 != 0 and ItemNameSuffix2 == 0:
                ItemName += "_" + str(ItemNameSuffix1)
            CompressData1 = bytes.fromhex(Bnd2[(MainFileBlockAreaOffset + MainFileBlockOffset) * 2:(MainFileBlockAreaOffset + MainFileBlockOffset + MainFileCompressionSize) * 2])
            DecompressData1 = zlib.decompressobj().decompress(CompressData1)
            OutputTypePath = OutputPath + "\\" + ItemType
            if not os.path.exists(OutputTypePath):
                os.makedirs(OutputTypePath)
            Output = open(OutputTypePath + "\\" + ItemName + ".dat", "wb")
            Output.write(DecompressData1)
            Output.close()
            if SubFileDecompressionSize != 0:
                SubFileCompressData = bytes.fromhex(Bnd2[(SubBlockAreaOffset + SubFileBlockOffset) * 2:(SubBlockAreaOffset + SubFileBlockOffset + SubFileCompressionSize) * 2])
                SubFileDecompressData = zlib.decompressobj().decompress(SubFileCompressData)
                if ItemType == "05_00_00_00" or ItemType == "Renderable":
                    Output = open(OutputTypePath + "\\" + ItemName + "_model.dat", "wb")
                elif ItemType == "01_00_00_00" or ItemType == "Texture":
                    Output = open(OutputTypePath + "\\" + ItemName + "_texture.dat", "wb")
                else:
                    Output = open(OutputTypePath + "\\" + ItemName + "_unknow.dat", "wb")
                Output.write(SubFileDecompressData)
                Output.close()
        IDs = bytes.fromhex(Bnd2[:MainFileBlockAreaOffset * 2])
        Output = open(OutputPath + "\\" + "IDs.BIN", "wb")
        Output.write(IDs)
        Output.close()
