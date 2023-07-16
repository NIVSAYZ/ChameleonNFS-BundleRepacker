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

InputPath = r"C:\Users\Administrator\Desktop\122699"
IDsPath = InputPath + "\\" + "IDs.BIN"
IDs = open(IDsPath, "rb").read().hex()
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

NewIDs = str()
Block1 = str()
Block2 = str()

ItemCount = (len(IDs) // 2 - 112) // 72
ItemInfoAreaOffset = struct.unpack("<L", bytes.fromhex(IDs[32:40]))[0]
Block1AreaOffset = struct.unpack("<L", bytes.fromhex(IDs[40:48]))[0]
#Block2AreaOffset = struct.unpack("<L", bytes.fromhex(IDs[48:56]))[0]
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
    #DecompressionSize1 = struct.unpack("<L", bytes.fromhex(IDs[Offset + 16:Offset + 22] + "00"))[0]
    #DecompressionSize2 = struct.unpack("<L", bytes.fromhex(IDs[Offset + 24:Offset + 30] + "00"))[0]
    #CompressionSize1 = struct.unpack("<L", bytes.fromhex(IDs[Offset + 48:Offset + 56]))[0]
    #CompressionSize2 = struct.unpack("<L", bytes.fromhex(IDs[Offset + 56:Offset + 64]))[0]
    #Offset1 = struct.unpack("<L", bytes.fromhex(IDs[Offset + 80:Offset + 88]))[0]
    #Offset2 = struct.unpack("<L", bytes.fromhex(IDs[Offset + 88:Offset + 96]))[0]
    ItemType = IDs[Offset + 120:Offset + 128].upper()
    ItemType = '_'.join([ItemType[x:x + 2] for x in range(0, len(ItemType), 2)])
    try:
        ItemType = ItemTypeDict[ItemType]
    except:
        pass
    ItemPath = InputPath + "\\" + ItemType + "\\" + ItemName + ".dat"
    Item = open(ItemPath, "rb").read()
    DecompressionSize1 = len(Item) // 2
    CompressData1 = zlib.compress(Item, CompressionLevel).hex()
    CompressionSize1 = len(CompressData1) // 2
    Block1 += CompressData1
    if ItemType == "Renderable":
        ItemPath = InputPath + "\\" + ItemType + "\\" + ItemName + "_model.dat"
        Item = open(ItemPath, "rb").read()
        DecompressionSize2 = len(Item) // 2
        CompressData2 = zlib.compress(Item, CompressionLevel).hex()
        CompressionSize2 = len(CompressData2) // 2
        Block2 += CompressData2
    elif ItemType == "Texture":
        ItemPath = InputPath + "\\" + ItemType + "\\" + ItemName + "_texture.dat"
        Item = open(ItemPath, "rb").read()
        DecompressionSize2 = len(Item) // 2
        CompressData2 = zlib.compress(Item, CompressionLevel).hex()
        CompressionSize2 = len(CompressData2) // 2
        Block2 += CompressData2
print(len(Block1) // 2)
print(len(Block2) // 2)
