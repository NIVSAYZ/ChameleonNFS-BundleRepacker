import os
import sys
import zlib
import struct

OutputNewFileType = True

ResourceTypeDict = {"01_00_00_00": "Texture",
                    "02_00_00_00": "Material",
                    "03_00_00_00": "VertexDescriptor",
                    "04_00_00_00": "VertexProgramState",
                    "05_00_00_00": "Renderable",
                    "06_00_00_00": "MaterialState",
                    "07_00_00_00": "SamplerState",
                    "08_00_00_00": "ShaderProgramBuffer",
                    "10_00_00_00": "AttribSysSchema",
                    "11_00_00_00": "AttribSysVault",
                    "12_00_00_00": "GenesysType.",
                    "13_00_00_00": "GenesysObject",
                    "14_00_00_00": "GenesysType.",
                    "15_00_00_00": "GenesysObject",
                    "16_00_00_00": "BinaryFile",
                    "20_00_00_00": "EntryList",
                    "30_00_00_00": "Font",
                    "40_00_00_00": "LuaCode",
                    "50_00_00_00": "InstanceList",
                    "51_00_00_00": "Model",
                    "52_00_00_00": "ColorCube",
                    "53_00_00_00": "Shader",
                    "60_00_00_00": "PolygonSoupList",
                    "61_00_00_00": "PolygonSoupTree",
                    "68_00_00_00": "NavigationMesh",
                    "70_00_00_00": "TextFile",
                    "71_00_00_00": "TextFile",
                    "72_00_00_00": "ResourceHandleList",
                    "74_00_00_00": "LuaData",
                    "78_00_00_00": "AllocatorInPool",
                    "80_00_00_00": "Ginsu",
                    "81_00_00_00": "Wave",
                    "82_00_00_00": "WaveContainerTable",
                    "83_00_00_00": "GameplayLinkData",
                    "84_00_00_00": "WaveDictionary",
                    "85_00_00_00": "MicroMonoStream",
                    "86_00_00_00": "Reverb",
                    "90_00_00_00": "ZoneList",
                    "91_00_00_00": "WorldPaintMap",
                    "A0_00_00_00": "IceAnimDictionary",
                    "B0_00_00_00": "AnimationList",
                    "B1_00_00_00": "PathAnimation",
                    "B2_00_00_00": "AnimSkel",
                    "B3_00_00_00": "Animation",
                    "C0_00_00_00": "CgsVertexProgramState",
                    "C1_00_00_00": "CgsProgramBuffer",
                    "DE_00_00_00": "DeltaDeleted",
                    "05_01_00_00": "VehicleList",
                    "06_01_00_00": "VehicleGraphicsSpec",
                    "07_01_00_00": "VehiclePhysicsSpec",
                    "0A_01_00_00": "WheelGraphicsSpec",
                    "12_01_00_00": "EnvironmentKeyframe",
                    "13_01_00_00": "EnvironmentTimeLine",
                    "14_01_00_00": "EnvironmentDictionary",
                    "00_02_00_00": "AIData",
                    "01_02_00_00": "Language",
                    "02_02_00_00": "TriggerData",
                    "03_02_00_00": "RoadData",
                    "04_02_00_00": "DynamicInstanceList",
                    "05_02_00_00": "WorldObject",
                    "06_02_00_00": "ZoneHeader",
                    "07_02_00_00": "VehicleSound",
                    "08_02_00_00": "RoadMapDataResourceType",
                    "09_02_00_00": "CharacterSpec",
                    "0A_02_00_00": "CharacterList",
                    "0B_02_00_00": "SurfaceSounds",
                    "0C_02_00_00": "ReverbRoadData",
                    "0D_02_00_00": "CameraTake",
                    "0E_02_00_00": "CameraTakeList",
                    "0F_02_00_00": "GroundcoverCollection",
                    "10_02_00_00": "ControlMesh",
                    "11_02_00_00": "CutsceneData",
                    "12_02_00_00": "CutsceneList",
                    "13_02_00_00": "LightInstanceList",
                    "14_02_00_00": "GroundcoverInstances",
                    "15_02_00_00": "CompoundObject",
                    "16_02_00_00": "CompoundInstanceList",
                    "17_02_00_00": "PropObject",
                    "18_02_00_00": "PropInstanceList",
                    "19_02_00_00": "ZoneAmbienceList",
                    "01_03_00_00": "BearEffect",
                    "02_03_00_00": "BearGlobalParameters",
                    "03_03_00_00": "ConvexHull",
                    "01_05_00_00": "HSMData",
                    "01_07_00_00": "TrafficLaneData"}

BundlePathList = sys.argv[1:]
BundlePathList = [r"C:\Users\Administrator\Desktop\VEH_122672_FE.BNDL"]
for BundlePath in BundlePathList:
    ExportPath = BundlePath[:BundlePath.find(".")]
    Bundle = open(BundlePath, "rb").read().hex()

    MagicNumber = Bundle[:8]
    if MagicNumber != "626e6432":
        exit("E1")

    Version = Bundle[8:12]
    if Version == "0500" or Version == "0005":
        Game = "Need For Speed Most Wanted 2012"
    elif Version == "0300":
        Game = "Need For Speed Hot Pursuit 2010"
    else:
        exit("E2")

    if Game == "Need For Speed Most Wanted 2012":
        PlatformCode = Bundle[12:16]
        if PlatformCode == "0100":
            Platform = "PC"
        elif PlatformCode == "0002":
            Platform = "PS3"
        else:
            exit("E3")
    elif Game == "Need For Speed Hot Pursuit 2010":
        PlatformCode = Bundle[16:24]
        if PlatformCode == "01000000":
            Platform = "PC"
        else:
            exit("E3")
    else:
        exit("E3")

    if Game == "Need For Speed Most Wanted 2012" and Platform == "PC":
        DebugDataOffset = struct.unpack("<L", bytes.fromhex(Bundle[16:24]))[0]
        ResourceEntriesCount = struct.unpack("<L", bytes.fromhex(Bundle[24:32]))[0]
        ResourceEntriesOffset = struct.unpack("<L", bytes.fromhex(Bundle[32:40]))[0]
        ResourceDataOffset1 = struct.unpack("<L", bytes.fromhex(Bundle[40:48]))[0]
        ResourceDataOffset2 = struct.unpack("<L", bytes.fromhex(Bundle[48:56]))[0]
        ResourceDataOffset3 = struct.unpack("<L", bytes.fromhex(Bundle[56:64]))[0]
        ResourceDataOffset4 = struct.unpack("<L", bytes.fromhex(Bundle[64:72]))[0]
        Flags = struct.unpack("<L", bytes.fromhex(Bundle[72:80]))[0]
        DefaultResourceId = struct.unpack("<L", bytes.fromhex(Bundle[72:80]))[0]
        for ResourceEntriesNum in range(ResourceEntriesCount):
            Offset = (ResourceEntriesOffset + 72 * ResourceEntriesNum) * 2
            ResourceId = Bundle[Offset:Offset + 8].upper()
            ResourceId = '_'.join([ResourceId[x:x + 2] for x in range(0, len(ResourceId), 2)])
            ResourceIdSuffix1 = struct.unpack("<B", bytes.fromhex(Bundle[Offset + 8:Offset + 10]))[0]
            ResourceIdSuffix2 = struct.unpack("<B", bytes.fromhex(Bundle[Offset + 12:Offset + 14]))[0]
            if ResourceIdSuffix1 != 0 and ResourceIdSuffix2 != 0:
                ResourceId += "_" + str(ResourceIdSuffix1) + "_" + str(ResourceIdSuffix2)
            elif ResourceIdSuffix1 == 0 and ResourceIdSuffix2 != 0:
                ResourceId += "_0_" + str(ResourceIdSuffix2)
            elif ResourceIdSuffix1 != 0 and ResourceIdSuffix2 == 0:
                ResourceId += "_" + str(ResourceIdSuffix1)
            UncompressedSizeAndAlignment1 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 16:Offset + 22] + "00"))[0]
            UncompressedSizeAndAlignment2 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 24:Offset + 30] + "00"))[0]
            UncompressedSizeAndAlignment3 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 32:Offset + 38] + "00"))[0]
            UncompressedSizeAndAlignment4 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 40:Offset + 46] + "00"))[0]
            SizeAndAlignmentOnDisk1 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 48:Offset + 56]))[0]
            SizeAndAlignmentOnDisk2 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 56:Offset + 64]))[0]
            SizeAndAlignmentOnDisk3 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 64:Offset + 72]))[0]
            SizeAndAlignmentOnDisk4 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 72:Offset + 80]))[0]
            DiskOffset1 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 80:Offset + 88]))[0]
            DiskOffset2 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 88:Offset + 96]))[0]
            DiskOffset3 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 96:Offset + 104]))[0]
            DiskOffset4 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 104:Offset + 112]))[0]
            ImportOffset = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 112:Offset + 120]))[0]
            ResourceTypeId = Bundle[Offset + 120:Offset + 128].upper()
            ImportCount = struct.unpack("<H", bytes.fromhex(Bundle[Offset + 128:Offset + 132]))[0]
            Flags = struct.unpack("<B", bytes.fromhex(Bundle[Offset + 132:Offset + 134]))[0]
            StreamOffset = struct.unpack("<B", bytes.fromhex(Bundle[Offset + 134:Offset + 136]))[0]
            CompressedData1 = bytes.fromhex(Bundle[(ResourceDataOffset1 + DiskOffset1) * 2:(ResourceDataOffset1 + SizeAndAlignmentOnDisk1 + DiskOffset1) * 2])
            UncompressedData1 = zlib.decompressobj().decompress(CompressedData1)
            ResourceType = '_'.join([ResourceTypeId[x:x + 2] for x in range(0, len(ResourceTypeId), 2)])
            if OutputNewFileType == True:
                ResourceType = ResourceTypeDict[ResourceType]
            OutputTypePath = ExportPath + "\\" + ResourceType
            if not os.path.exists(OutputTypePath):
                os.makedirs(OutputTypePath)
            Output = open(OutputTypePath + "\\" + ResourceId + ".dat", "wb")
            Output.write(UncompressedData1)
            Output.close()
            if SizeAndAlignmentOnDisk2 != 0:
                CompressData2 = bytes.fromhex(Bundle[(ResourceDataOffset2 + DiskOffset2) * 2:(ResourceDataOffset2 + SizeAndAlignmentOnDisk2 + DiskOffset2) * 2])
                DecompressData2 = zlib.decompressobj().decompress(CompressData2)
                if ResourceType == "05_00_00_00" or ResourceType == "Renderable":
                    Output = open(OutputTypePath + "\\" + ResourceId + "_model.dat", "wb")
                elif ResourceType == "01_00_00_00" or ResourceType == "Texture":
                    Output = open(OutputTypePath + "\\" + ResourceId + "_texture.dat", "wb")
                else:
                    Output = open(OutputTypePath + "\\" + ResourceId + "_unknow.dat", "wb")
                Output.write(DecompressData2)
                Output.close()
        IDs = bytes.fromhex(Bundle[:(ResourceEntriesOffset + ResourceEntriesCount * 72) * 2])
        Output = open(ExportPath + "\\" + "IDs.BIN", "wb")
        Output.write(IDs)
        Output.close()
        if DebugDataOffset != 0:
            DebugDataList = list()
            DebugDataXml = open(ExportPath + "\\" + "ResourceStringTable.xml", "w")
            Length = len(Bundle) // 2 - DebugDataOffset
            for Offset in range(Length):
                Byte = Bundle[(DebugDataOffset + Offset) * 2:(DebugDataOffset + 1 + Offset) * 2]
                if Byte == "0a":
                    DebugDataList.append("\n")
                elif Byte == "09":
                    DebugDataList.append("	")
                else:
                    DebugDataList.append(chr(struct.unpack("<B", bytes.fromhex(Byte))[0]))
        DebugDataXml.write("".join(DebugDataList))
        DebugDataXml.close()
    elif Game == "Need For Speed Most Wanted 2012" and Platform == "PS3":
        DebugDataOffset = struct.unpack(">L", bytes.fromhex(Bundle[16:24]))[0]
        ResourceEntriesCount = struct.unpack(">L", bytes.fromhex(Bundle[24:32]))[0]
        ResourceEntriesOffset = struct.unpack(">L", bytes.fromhex(Bundle[32:40]))[0]
        ResourceDataOffset1 = struct.unpack(">L", bytes.fromhex(Bundle[40:48]))[0]
        ResourceDataOffset2 = struct.unpack(">L", bytes.fromhex(Bundle[48:56]))[0]
        ResourceDataOffset3 = struct.unpack(">L", bytes.fromhex(Bundle[56:64]))[0]
        ResourceDataOffset4 = struct.unpack(">L", bytes.fromhex(Bundle[64:72]))[0]
        Flags = struct.unpack(">L", bytes.fromhex(Bundle[72:80]))[0]
        DefaultResourceId = struct.unpack(">L", bytes.fromhex(Bundle[72:80]))[0]
        for ResourceEntriesNum in range(ResourceEntriesCount):
            Offset = (ResourceEntriesOffset + 72 * ResourceEntriesNum) * 2
            ResourceId = Bundle[Offset + 8:Offset + 16].upper()
            ResourceId = '_'.join([ResourceId[x:x + 2] for x in range(0, len(ResourceId), 2)])
            ResourceIdSuffix1 = struct.unpack(">B", bytes.fromhex(Bundle[Offset + 2:Offset + 4]))[0]
            ResourceIdSuffix2 = struct.unpack(">B", bytes.fromhex(Bundle[Offset + 6:Offset + 8]))[0]
            if ResourceIdSuffix2 != 0 and ResourceIdSuffix1 != 0:
                ResourceId += "_" + str(ResourceIdSuffix1) + "_" + str(ResourceIdSuffix1)
            elif ResourceIdSuffix2 == 0 and ResourceIdSuffix1 != 0:
                ResourceId += "_0_" + str(ResourceIdSuffix1)
            elif ResourceIdSuffix2 != 0 and ResourceIdSuffix1 == 0:
                ResourceId += "_" + str(ResourceIdSuffix2)
            UncompressedSizeAndAlignment1 = struct.unpack(">L", bytes.fromhex("00" + Bundle[Offset + 18:Offset + 24]))[0]
            UncompressedSizeAndAlignment2 = struct.unpack(">L", bytes.fromhex("00" + Bundle[Offset + 26:Offset + 32]))[0]
            UncompressedSizeAndAlignment3 = struct.unpack(">L", bytes.fromhex("00" + Bundle[Offset + 34:Offset + 40]))[0]
            UncompressedSizeAndAlignment4 = struct.unpack(">L", bytes.fromhex("00" + Bundle[Offset + 42:Offset + 48]))[0]
            #print(UncompressedSizeAndAlignment1, UncompressedSizeAndAlignment2, UncompressedSizeAndAlignment3, UncompressedSizeAndAlignment4)
            SizeAndAlignmentOnDisk1 = struct.unpack(">L", bytes.fromhex(Bundle[Offset + 48:Offset + 56]))[0]
            SizeAndAlignmentOnDisk2 = struct.unpack(">L", bytes.fromhex(Bundle[Offset + 56:Offset + 64]))[0]
            SizeAndAlignmentOnDisk3 = struct.unpack(">L", bytes.fromhex(Bundle[Offset + 64:Offset + 72]))[0]
            SizeAndAlignmentOnDisk4 = struct.unpack(">L", bytes.fromhex(Bundle[Offset + 72:Offset + 80]))[0]
            #print(SizeAndAlignmentOnDisk1, SizeAndAlignmentOnDisk2, SizeAndAlignmentOnDisk3, SizeAndAlignmentOnDisk4)
            DiskOffset1 = struct.unpack(">L", bytes.fromhex(Bundle[Offset + 80:Offset + 88]))[0]
            DiskOffset2 = struct.unpack(">L", bytes.fromhex(Bundle[Offset + 88:Offset + 96]))[0]
            DiskOffset3 = struct.unpack(">L", bytes.fromhex(Bundle[Offset + 96:Offset + 104]))[0]
            DiskOffset4 = struct.unpack(">L", bytes.fromhex(Bundle[Offset + 104:Offset + 112]))[0]
            #print(DiskOffset1, DiskOffset2, DiskOffset3, DiskOffset4)
            ImportOffset = struct.unpack(">L", bytes.fromhex(Bundle[Offset + 112:Offset + 120]))[0]
            ResourceTypeId = Bundle[Offset + 120:Offset + 128].upper()
            ImportCount = struct.unpack(">H", bytes.fromhex(Bundle[Offset + 128:Offset + 132]))[0]
            Flags = struct.unpack(">B", bytes.fromhex(Bundle[Offset + 132:Offset + 134]))[0]
            StreamOffset = struct.unpack(">B", bytes.fromhex(Bundle[Offset + 134:Offset + 136]))[0]
            CompressedData1 = bytes.fromhex(Bundle[(ResourceDataOffset1 + DiskOffset1) * 2:(ResourceDataOffset1 + SizeAndAlignmentOnDisk1 + DiskOffset1) * 2])
            UncompressedData1 = zlib.decompressobj().decompress(CompressedData1)
            ResourceType = '_'.join([ResourceTypeId[x:x + 2] for x in range(0, len(ResourceTypeId), 2)])
            if OutputNewFileType == True:
                ResourceTypeId = ResourceTypeId[6:] + ResourceTypeId[4:6] + ResourceTypeId[2:4] + ResourceTypeId[:2]
                ResourceType = '_'.join([ResourceTypeId[x:x + 2] for x in range(0, len(ResourceTypeId), 2)])
                ResourceType = ResourceTypeDict[ResourceType]
            OutputTypePath = ExportPath + "\\" + ResourceType
            if not os.path.exists(OutputTypePath):
                os.makedirs(OutputTypePath)
            Output = open(OutputTypePath + "\\" + ResourceId + ".dat", "wb")
            Output.write(UncompressedData1)
            Output.close()
            if SizeAndAlignmentOnDisk3 != 0:
                CompressData3 = bytes.fromhex(Bundle[(ResourceDataOffset3 + DiskOffset3) * 2:(ResourceDataOffset3 + SizeAndAlignmentOnDisk3 + DiskOffset3) * 2])
                DecompressData3 = zlib.decompressobj().decompress(CompressData3)
                if ResourceType == "05_00_00_00" or ResourceType == "Renderable":
                    Output = open(OutputTypePath + "\\" + ResourceId + "_model.dat", "wb")
                elif ResourceType == "01_00_00_00" or ResourceType == "Texture":
                    Output = open(OutputTypePath + "\\" + ResourceId + "_texture.dat", "wb")
                else:
                    Output = open(OutputTypePath + "\\" + ResourceId + "_unknow.dat", "wb")
                Output.write(DecompressData3)
                Output.close()
        IDs = bytes.fromhex(Bundle[:(ResourceEntriesOffset + ResourceEntriesCount * 72) * 2])
        Output = open(ExportPath + "\\" + "IDs.BIN", "wb")
        Output.write(IDs)
        Output.close()
        if DebugDataOffset != 0:
            DebugDataList = list()
            DebugDataXml = open(ExportPath + "\\" + "ResourceStringTable.xml", "w")
            Length = len(Bundle) // 2 - DebugDataOffset
            for Offset in range(Length):
                Byte = Bundle[(DebugDataOffset + Offset) * 2:(DebugDataOffset + 1 + Offset) * 2]
                if Byte == "0a":
                    DebugDataList.append("\n")
                elif Byte == "09":
                    DebugDataList.append("	")
                else:
                    DebugDataList.append(chr(struct.unpack("<B", bytes.fromhex(Byte))[0]))
        DebugDataXml.write("".join(DebugDataList))
        DebugDataXml.close()
    elif Game == "Need For Speed Hot Pursuit 2010" and Platform == "PC":
        DebugDataOffset = struct.unpack("<L", bytes.fromhex(Bundle[24:32]))[0]
        ResourceEntriesCount = struct.unpack("<L", bytes.fromhex(Bundle[32:40]))[0]
        ResourceEntriesOffset = struct.unpack("<L", bytes.fromhex(Bundle[40:48]))[0]
        ResourceDataOffset1 = struct.unpack("<L", bytes.fromhex(Bundle[48:56]))[0]
        ResourceDataOffset2 = struct.unpack("<L", bytes.fromhex(Bundle[56:64]))[0]
        ResourceDataOffset3 = struct.unpack("<L", bytes.fromhex(Bundle[64:72]))[0]
        ResourceDataOffset4 = struct.unpack("<L", bytes.fromhex(Bundle[72:80]))[0]
        Flags = struct.unpack(">L", bytes.fromhex(Bundle[80:88]))[0]
        for ResourceEntriesNum in range(ResourceEntriesCount):
            Offset = (ResourceEntriesOffset + 80 * ResourceEntriesNum) * 2
            ResourceId = Bundle[Offset:Offset + 8].upper()
            ResourceId = '_'.join([ResourceId[x:x + 2] for x in range(0, len(ResourceId), 2)])
            ResourceIdSuffix1 = struct.unpack("<B", bytes.fromhex(Bundle[Offset + 8:Offset + 10]))[0]
            ResourceIdSuffix2 = struct.unpack("<B", bytes.fromhex(Bundle[Offset + 12:Offset + 14]))[0]
            if ResourceIdSuffix1 != 0 and ResourceIdSuffix2 != 0:
                ResourceId += "_" + str(ResourceIdSuffix1) + "_" + str(ResourceIdSuffix2)
            elif ResourceIdSuffix1 == 0 and ResourceIdSuffix2 != 0:
                ResourceId += "_0_" + str(ResourceIdSuffix2)
            elif ResourceIdSuffix1 != 0 and ResourceIdSuffix2 == 0:
                ResourceId += "_" + str(ResourceIdSuffix1)
            ImportHash = Bundle[Offset + 16:Offset + 32]
            UncompressedSizeAndAlignment1 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 32:Offset + 38] + "00"))[0]
            UncompressedSizeAndAlignment2 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 40:Offset + 46] + "00"))[0]
            UncompressedSizeAndAlignment3 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 48:Offset + 54] + "00"))[0]
            UncompressedSizeAndAlignment4 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 56:Offset + 62] + "00"))[0]
            SizeAndAlignmentOnDisk1 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 64:Offset + 72]))[0]
            SizeAndAlignmentOnDisk2 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 72:Offset + 80]))[0]
            SizeAndAlignmentOnDisk3 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 80:Offset + 88]))[0]
            SizeAndAlignmentOnDisk4 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 88:Offset + 96]))[0]
            DiskOffset1 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 96:Offset + 104]))[0]
            DiskOffset2 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 104:Offset + 112]))[0]
            DiskOffset3 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 112:Offset + 120]))[0]
            DiskOffset4 = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 120:Offset + 128]))[0]
            ImportOffset = struct.unpack("<L", bytes.fromhex(Bundle[Offset + 128:Offset + 136]))[0]
            ResourceTypeId = Bundle[Offset + 136:Offset + 144].upper()
            ImportCount = struct.unpack("<H", bytes.fromhex(Bundle[Offset + 144:Offset + 148]))[0]
            Flags = struct.unpack("<B", bytes.fromhex(Bundle[Offset + 148:Offset + 150]))[0]
            StreamIndex = struct.unpack("<B", bytes.fromhex(Bundle[Offset + 150:Offset + 152]))[0]
            CompressedData1 = bytes.fromhex(Bundle[(ResourceDataOffset1 + DiskOffset1) * 2:(ResourceDataOffset1 + SizeAndAlignmentOnDisk1 + DiskOffset1) * 2])
            UncompressedData1 = zlib.decompressobj().decompress(CompressedData1)
            ResourceType = '_'.join([ResourceTypeId[x:x + 2] for x in range(0, len(ResourceTypeId), 2)])
            if OutputNewFileType == True:
                ResourceType = ResourceTypeDict[ResourceType]
            OutputTypePath = ExportPath + "\\" + ResourceType
            if not os.path.exists(OutputTypePath):
                os.makedirs(OutputTypePath)
            Output = open(OutputTypePath + "\\" + ResourceId + ".dat", "wb")
            Output.write(UncompressedData1)
            Output.close()
            if SizeAndAlignmentOnDisk2 != 0:
                CompressData2 = bytes.fromhex(Bundle[(ResourceDataOffset2 + DiskOffset2) * 2:(ResourceDataOffset2 + SizeAndAlignmentOnDisk2 + DiskOffset2) * 2])
                DecompressData2 = zlib.decompressobj().decompress(CompressData2)
                if ResourceType == "05_00_00_00" or ResourceType == "Renderable":
                    Output = open(OutputTypePath + "\\" + ResourceId + "_model.dat", "wb")
                elif ResourceType == "01_00_00_00" or ResourceType == "Texture":
                    Output = open(OutputTypePath + "\\" + ResourceId + "_texture.dat", "wb")
                else:
                    Output = open(OutputTypePath + "\\" + ResourceId + "_unknow.dat", "wb")
                Output.write(DecompressData2)
                Output.close()
        IDs = bytes.fromhex(Bundle[:(ResourceEntriesOffset + ResourceEntriesCount * 80) * 2])
        Output = open(ExportPath + "\\" + "IDs.BIN", "wb")
        Output.write(IDs)
        Output.close()
        if DebugDataOffset != 0:
            DebugDataList = list()
            DebugDataXml = open(ExportPath + "\\" + "ResourceStringTable.xml", "w")
            Length = len(Bundle) // 2 - DebugDataOffset
            for Offset in range(Length):
                Byte = Bundle[(DebugDataOffset + Offset) * 2:(DebugDataOffset + 1 + Offset) * 2]
                if Byte == "0a":
                    DebugDataList.append("\n")
                elif Byte == "09":
                    DebugDataList.append("	")
                else:
                    DebugDataList.append(chr(struct.unpack("<B", bytes.fromhex(Byte))[0]))
        DebugDataXml.write("".join(DebugDataList))
        DebugDataXml.close()
