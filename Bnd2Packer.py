import os
import sys
import zlib
import struct

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


InputPathList = sys.argv[1:]
for InputPath in InputPathList:
    IDsPath = InputPath + "\\" + "IDs.BIN"
    IDs = open(IDsPath, "rb").read().hex()
    ItemInfoArea = IDs[224:]
    Byte = IDs[8:16]
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

    IDsHeader = str()
    NewItemInfoArea = str()
    MainFileBlock = str()
    SubFileBlock = str()

    ItemCount = len(ItemInfoArea) // 144
    ItemInfoAreaOffset = struct.unpack("<L", bytes.fromhex(IDs[32:40]))[0]
    MainFileBlockAreaOffset = struct.unpack("<L", bytes.fromhex(IDs[40:48]))[0]
    CompressionLevel = struct.unpack("<L", bytes.fromhex(IDs[72:80]))[0]
    for ItemNum in range(ItemCount):
        Offset = (ItemInfoAreaOffset + 72 * ItemNum) * 2
        ItemName = IDs[Offset:Offset + 8].upper()
        ItemName = '_'.join([ItemName[x:x + 2] for x in range(0, len(ItemName), 2)])
        ItemNameSuffix1 = struct.unpack("<B", bytes.fromhex(IDs[Offset + 8:Offset + 10]))[0]
        ItemNameSuffix2 = struct.unpack("<B", bytes.fromhex(IDs[Offset + 12:Offset + 14]))[0]
        if ItemNameSuffix1 != 0 and ItemNameSuffix2 != 0:
            ItemName += "_" + str(ItemNameSuffix1) + "_" + str(ItemNameSuffix2)
        elif ItemNameSuffix1 == 0 and ItemNameSuffix2 != 0:
            ItemName += "_0_" + str(ItemNameSuffix2)
        elif ItemNameSuffix1 != 0 and ItemNameSuffix2 == 0:
            ItemName += "_" + str(ItemNameSuffix1)
        ItemType = IDs[Offset + 120:Offset + 128].upper()
        ItemType = '_'.join([ItemType[x:x + 2] for x in range(0, len(ItemType), 2)])
        try:
            ItemType = ItemTypeDict[ItemType]
        except:
            pass
        ItemPath = InputPath + "\\" + ItemType + "\\" + ItemName + ".dat"
        Item = open(ItemPath, "rb").read()
        MainFileDecompressionSize = len(Item)
        MainFileCompressData = zlib.compress(Item, CompressionLevel).hex()
        MainFileCompressionSize = len(MainFileCompressData) // 2
        MainFileBlockOffset = len(MainFileBlock) // 2
        MainFileBlock += MainFileCompressData
        if ItemType == "Renderable":
            ItemPath = InputPath + "\\" + ItemType + "\\" + ItemName + "_model.dat"
            Item = open(ItemPath, "rb").read()
            SubFileDecompressionSize = len(Item)
            SubFileCompressData = zlib.compress(Item, CompressionLevel).hex()
            SubFileCompressionSize = len(SubFileCompressData) // 2
            SubFileBlockOffset = len(SubFileBlock) // 2
            NewItemInfoArea += ItemInfoArea[ItemNum * 144:ItemNum * 144 + 16] + struct.pack("<L", MainFileDecompressionSize).hex() + struct.pack("<L", SubFileDecompressionSize).hex() + ItemInfoArea[ItemNum * 144 + 32:ItemNum * 144 + 48] + struct.pack("<L", MainFileCompressionSize).hex() + struct.pack("<L", SubFileCompressionSize).hex() + ItemInfoArea[ItemNum * 144 + 64:ItemNum * 144 + 80] + struct.pack("<L", MainFileBlockOffset).hex() + struct.pack("<L", SubFileBlockOffset).hex() + ItemInfoArea[ItemNum * 144 + 96:ItemNum * 144 + 144]
            SubFileBlock += SubFileCompressData
        elif ItemType == "Texture":
            ItemPath = InputPath + "\\" + ItemType + "\\" + ItemName + "_texture.dat"
            Item = open(ItemPath, "rb").read()
            SubFileDecompressionSize = len(Item)
            SubFileCompressData = zlib.compress(Item, CompressionLevel).hex()
            SubFileCompressionSize = len(SubFileCompressData) // 2
            SubFileBlockOffset = len(SubFileBlock) // 2
            NewItemInfoArea += ItemInfoArea[ItemNum * 144:ItemNum * 144 + 16] + struct.pack("<L", MainFileDecompressionSize).hex() + struct.pack("<L", SubFileDecompressionSize).hex() + ItemInfoArea[ItemNum * 144 + 32:ItemNum * 144 + 48] + struct.pack("<L", MainFileCompressionSize).hex() + struct.pack("<L", SubFileCompressionSize).hex() + ItemInfoArea[ItemNum * 144 + 64:ItemNum * 144 + 80] + struct.pack("<L", MainFileBlockOffset).hex() + struct.pack("<L", SubFileBlockOffset).hex() + ItemInfoArea[ItemNum * 144 + 96:ItemNum * 144 + 144]
            SubFileBlock += SubFileCompressData
        else:
            SubFileDecompressionSize = "00000000"
            SubFileBlockOffset = "00000000"
            NewItemInfoArea += ItemInfoArea[ItemNum * 144:ItemNum * 144 + 16] + struct.pack("<L", MainFileDecompressionSize).hex() + ItemInfoArea[ItemNum * 144 + 24:ItemNum * 144 + 48] + struct.pack("<L", MainFileCompressionSize).hex() + ItemInfoArea[ItemNum * 144 + 56:ItemNum * 144 + 80] + struct.pack("<L", MainFileBlockOffset).hex() + ItemInfoArea[ItemNum * 144 + 88:ItemNum * 144 + 144]
    IDsHeader = IDs[:24] + struct.pack("<L", ItemCount).hex() + IDs[32:40] + struct.pack("<L", len(NewItemInfoArea) // 2 + 112).hex() + struct.pack("<L", len(NewItemInfoArea + MainFileBlock) // 2 + 112).hex() + struct.pack("<L", len(NewItemInfoArea + MainFileBlock + SubFileBlock) // 2 + 112).hex() + struct.pack("<L", len(NewItemInfoArea + MainFileBlock + SubFileBlock) // 2 + 112).hex() + IDs[72:224]
    BndlName = os.path.basename(os.path.dirname(IDsPath))
    BndlOutputPath = os.path.dirname(os.path.dirname(IDsPath)) + "\\" + BndlName + ".BNDL"
    Bndl = open(BndlOutputPath, "wb")
    Bndl.write(bytes.fromhex(IDsHeader + NewItemInfoArea + MainFileBlock + SubFileBlock))
    Bndl.close()
