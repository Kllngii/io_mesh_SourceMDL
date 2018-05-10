import random
import time
from enum import Enum, IntEnum
from pprint import pformat

from typing import List, Tuple

try:
    from .ByteIO import ByteIO
    from .GLOBALS import SourceVector, SourceQuaternion, SourceFloat16bits
    from . import VTX, VVD
    from . import math_utilities

except ImportError:
    from ByteIO import ByteIO
    from GLOBALS import SourceVector, SourceQuaternion, SourceFloat16bits
    import VTX
    import VVD
    import math_utilities


class SourceMdlAnimationDesc:
    def __init__(self):
        self.theName = ''


class SourceMdlFileData:
    def __init__(self):
        self.id = ''
        self.version = 0
        self.checksum = 0
        self.name = ''
        self.file_size = 0
        self.eye_position = SourceVector()
        self.illumination_position = SourceVector()
        self.hull_min_position = SourceVector()
        self.hull_max_position = SourceVector()
        self.view_bounding_box_min_position = SourceVector()
        self.view_bounding_box_max_position = SourceVector()

        self.flags = 0
        self.bone_count = 0
        self.bone_offset = 0
        self.bone_controller_count = 0
        self.bone_controller_offset = 0
        self.hitbox_set_count = 0
        self.hitbox_set_offset = 0
        self.local_animation_count = 0
        self.local_animation_offset = 0
        self.local_sequence_count = 0
        self.local_sequence_offset = 0
        self.sequence_group_count = 0
        self.sequence_group_offset = 0
        self.activity_list_version = 0
        self.events_indexed = 0
        self.texture_count = 0
        self.texture_offset = 0
        self.texture_path_count = 0
        self.texture_path_offset = 0
        self.skin_reference_count = 0
        self.skin_family_count = 0
        self.skin_family_offset = 0
        self.body_part_count = 0
        self.body_part_offset = 0
        self.local_attachment_count = 0
        self.local_attachment_offset = 0
        self.sound_table = 0
        self.sound_index = 0
        self.sound_groups = 0
        self.sound_group_offset = 0
        self.local_node_count = 0
        self.local_node_offset = 0
        self.local_node_name_offset = 0
        self.flex_desc_count = 0
        self.flex_desc_offset = 0
        self.flex_controller_count = 0
        self.flex_controller_offset = 0
        self.flex_rule_count = 0
        self.flex_rule_offset = 0
        self.ik_chain_count = 0
        self.ik_chain_offset = 0
        self.mouth_count = 0
        self.mouth_offset = 0
        self.local_pose_paramater_count = 0
        self.local_pose_parameter_offset = 0
        self.surface_prop_offset = 0
        self.key_value_offset = 0
        self.key_value_size = 0
        self.local_ik_auto_play_lock_count = 0
        self.local_ik_auto_play_lock_offset = 0
        self.mass = 0.0
        self.contents = 0
        self.include_model_count = 0
        self.include_model_offset = 0
        self.virtual_model_pointer = 0
        self.anim_block_name_offset = 0
        self.anim_block_count = 0
        self.anim_block_offset = 0
        self.anim_block_model_pointer = 0
        self.bone_table_by_name_offset = 0
        self.vertex_base_pointer = 0
        self.index_base_pointer = 0
        self.directional_light_dot = 0
        self.root_lod = 0
        self.allowed_root_lod_count = 0
        self.unused = 0
        self.unused4 = 0
        self.flex_controller_ui_count = 0
        self.flex_controller_ui_offset = 0
        self.vert_anim_fixed_point_scale = 0
        self.surface_prop_lookup = 0
        self.unused3 = []
        self.studio_header2_offset = 0
        self.bone_flex_driver_count = 0
        self.unused2 = 0
        self.source_bone_transform_count = 0
        self.source_bone_transform_offset = 0
        self.bone_flex_driver_offset = 0
        self.illum_position_attachment_index = 0
        self.max_eye_deflection = 0
        self.linear_bone_offset = 0
        # self.reserved = [None] * 56
        self.animation_descs = []
        self.anim_blocks = []
        self.anim_block_relative_path_file_name = ""
        self.attachments = []  # type: List[SourceMdlAttachment]
        self.body_parts = []  # type: List[SourceMdlBodyPart]
        self.bones = []  # type: List[SourceMdlBone]
        self.bone_controllers = []  # type: List[SourceMdlBoneController]
        self.bone_table_by_name = []
        self.flex_descs = []  # type: List[SourceMdlFlexDesc]
        self.flex_controllers = []  # type: List[SourceMdlFlexController]
        self.flex_rules = []  # type: List[SourceMdlFlexRule]
        self.hitbox_sets = []
        self.ik_chains = []
        self.ik_locks = []
        self.key_values_text = ""
        self.local_node_names = []
        self.mouths = []  # type: List[SourceMdlMouth]
        self.pose_param_descs = []
        self.sequence_descs = []
        self.skin_families = []  # type: List[List[int]]
        self.surface_prop_name = ""
        self.texture_paths = []  # type: List[str]
        self.textures = []  # type: List[SourceMdlTexture]
        self.section_frame_count = 0
        self.section_frame_min_frame_count = 0
        self.actual_file_size = 0
        self.flex_frames = []  # type: List[FlexFrame]
        self.bone_flex_drivers = []  # type: List[SourceBoneFlexDriver]
        self.flex_controllers_ui = []  # type: List[SourceFlexControllerUI]
        self.eyelid_flex_frame_indexes = []
        self.first_animation_desc = None
        self.first_animation_desc_frame_lines = {}
        self.mdl_file_only_has_animations = False
        self.procedural_bones_command_is_used = False
        self.weight_lists = []
        self.name_offset = 0
        self.bodypart_frames = []  # type: List[List[Tuple[int,SourceMdlBodyPart]]]

    def read(self, reader: ByteIO):
        self.read_header00(reader)
        self.read_header01(reader)
        self.read_header02(reader)

    def read_header00(self, reader: ByteIO):
        self.id = ''.join(list([chr(reader.read_uint8()) for _ in range(4)]))
        self.version = reader.read_uint32()
        self.checksum = reader.read_uint32()
        self.name = reader.read_ascii_string(64)
        self.file_size = reader.read_uint32()

    def read_header01(self, reader: ByteIO):
        self.eye_position.read(reader)

        self.illumination_position.read(reader)

        self.hull_min_position.read(reader)

        self.hull_max_position.read(reader)

        self.view_bounding_box_min_position.read(reader)

        self.view_bounding_box_max_position.read(reader)

        self.flags = reader.read_uint32()

        self.bone_count = reader.read_uint32()
        self.bone_offset = reader.read_uint32()

        self.bone_controller_count = reader.read_uint32()
        self.bone_controller_offset = reader.read_uint32()

        self.hitbox_set_count = reader.read_uint32()
        self.hitbox_set_offset = reader.read_uint32()

        self.local_animation_count = reader.read_uint32()
        self.local_animation_offset = reader.read_uint32()

        self.local_sequence_count = reader.read_uint32()
        self.local_sequence_offset = reader.read_uint32()

        self.activity_list_version = reader.read_uint32()
        self.events_indexed = reader.read_uint32()

        self.texture_count = reader.read_uint32()
        self.texture_offset = reader.read_uint32()
        self.texture_path_count = reader.read_uint32()
        self.texture_path_offset = reader.read_uint32()

        self.skin_reference_count = reader.read_uint32()
        self.skin_family_count = reader.read_uint32()
        self.skin_family_offset = reader.read_uint32()

        self.body_part_count = reader.read_uint32()
        self.body_part_offset = reader.read_uint32()

        self.local_attachment_count = reader.read_uint32()
        self.local_attachment_offset = reader.read_uint32()

        self.local_node_count = reader.read_uint32()
        self.local_node_offset = reader.read_uint32()
        self.local_node_name_offset = reader.read_uint32()

        self.flex_desc_count = reader.read_uint32()
        self.flex_desc_offset = reader.read_uint32()

        self.flex_controller_count = reader.read_uint32()
        self.flex_controller_offset = reader.read_uint32()

        self.flex_rule_count = reader.read_uint32()
        self.flex_rule_offset = reader.read_uint32()

        self.ik_chain_count = reader.read_uint32()
        self.ik_chain_offset = reader.read_uint32()

        self.mouth_count = reader.read_uint32()
        self.mouth_offset = reader.read_uint32()

        self.local_pose_paramater_count = reader.read_uint32()
        self.local_pose_parameter_offset = reader.read_uint32()

        self.surface_prop_offset = reader.read_uint32()

        if self.surface_prop_offset > 0:
            self.surface_prop_name = reader.read_from_offset(self.surface_prop_offset, reader.read_ascii_string)

        self.key_value_offset = reader.read_uint32()
        self.key_value_size = reader.read_uint32()

        self.local_ik_auto_play_lock_offset = reader.read_uint32()
        self.local_ik_auto_play_lock_count = reader.read_uint32()

        self.mass = reader.read_float()
        self.contents = reader.read_uint32()

        self.include_model_count = reader.read_uint32()
        self.include_model_offset = reader.read_uint32()

        self.virtual_model_pointer = reader.read_uint32()

        self.anim_block_name_offset = reader.read_uint32()
        self.anim_block_count = reader.read_uint32()
        self.anim_block_offset = reader.read_uint32()
        self.anim_block_model_pointer = reader.read_uint32()

        if self.anim_block_count > 0:
            if self.anim_block_name_offset > 0:
                self.anim_block_relative_path_file_name = reader.read_from_offset(
                    reader.tell() + self.anim_block_name_offset, reader.read_ascii_string)

        if self.anim_block_offset > 0:
            with reader.save_current_pos():
                reader.seek(self.anim_block_offset, 0)
                for offset in range(self.anim_block_count):
                    anim_block = SourceMdlAnimBlock()
                    anim_block.read(reader)
                    self.anim_blocks.append(anim_block)

        self.bone_table_by_name_offset = reader.read_uint32()

        self.vertex_base_pointer = reader.read_uint32()
        self.index_base_pointer = reader.read_uint32()

        self.directional_light_dot = reader.read_uint8()

        self.root_lod = reader.read_uint8()

        self.allowed_root_lod_count = reader.read_uint8()

        self.unused = reader.read_uint8()

        self.unused4 = reader.read_uint32()

        self.flex_controller_ui_count = reader.read_uint32()
        self.flex_controller_ui_offset = reader.read_uint32()

        self.vert_anim_fixed_point_scale = reader.read_float()
        self.surface_prop_offset = reader.read_uint32()

        self.studio_header2_offset = reader.read_uint32()

        self.unused2 = reader.read_uint32()

        if self.body_part_count == 0 and self.local_sequence_count > 0:
            self.mdl_file_only_has_animations = True

    def read_header02(self, reader: ByteIO):

        self.source_bone_transform_count = reader.read_uint32()
        self.source_bone_transform_offset = reader.read_uint32()
        self.illum_position_attachment_index = reader.read_uint32()
        self.max_eye_deflection = reader.read_float()
        self.linear_bone_offset = reader.read_uint32()

        self.name_offset = reader.read_uint32()
        self.bone_flex_driver_count = reader.read_uint32()
        self.bone_flex_driver_offset = reader.read_uint32()
        [reader.read_uint32() for _ in range(56)]
        # self.reserved = list([reader.read_uint32() for _ in range(56)])

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)


class SourceMdlFileDataV53(SourceMdlFileData):
    def __init__(self):
        super().__init__()
        self.name_copy_offset = 0
        self.vtx_offset = 0
        self.vvd_offset = 0
        self.vtx = None
        self.vvd = None

    def read(self, reader: ByteIO):
        self.read_header00(reader)
        self.read_header01(reader)
        self.read_header02(reader)

    def read_header00(self, reader: ByteIO):
        self.id = ''.join(list([chr(reader.read_uint8()) for _ in range(4)]))
        self.version = reader.read_uint32()
        self.checksum = reader.read_uint32()

        self.name_copy_offset = reader.read_uint32()

        self.name = reader.read_ascii_string(64)
        self.file_size = reader.read_uint32()

    def read_header01(self, reader: ByteIO):
        self.eye_position.read(reader)

        self.illumination_position.read(reader)

        self.hull_min_position.read(reader)

        self.hull_max_position.read(reader)

        self.view_bounding_box_min_position.read(reader)

        self.view_bounding_box_max_position.read(reader)

        self.flags = reader.read_uint32()

        self.bone_count = reader.read_uint32()
        self.bone_offset = reader.read_uint32()

        self.bone_controller_count = reader.read_uint32()
        self.bone_controller_offset = reader.read_uint32()

        self.hitbox_set_count = reader.read_uint32()
        self.hitbox_set_offset = reader.read_uint32()

        self.local_animation_count = reader.read_uint32()
        self.local_animation_offset = reader.read_uint32()

        self.local_sequence_count = reader.read_uint32()
        self.local_sequence_offset = reader.read_uint32()

        self.activity_list_version = reader.read_uint32()
        self.events_indexed = reader.read_uint32()

        self.texture_count = reader.read_uint32()
        self.texture_offset = reader.read_uint32()
        self.texture_path_count = reader.read_uint32()
        self.texture_path_offset = reader.read_uint32()

        self.skin_reference_count = reader.read_uint32()
        self.skin_family_count = reader.read_uint32()
        self.skin_family_offset = reader.read_uint32()

        self.body_part_count = reader.read_uint32()
        self.body_part_offset = reader.read_uint32()

        self.local_attachment_count = reader.read_uint32()
        self.local_attachment_offset = reader.read_uint32()

        self.local_node_count = reader.read_uint32()
        self.local_node_offset = reader.read_uint32()

        self.local_node_name_offset = reader.read_uint32()

        self.flex_desc_count = reader.read_uint32()
        self.flex_desc_offset = reader.read_uint32()

        self.flex_controller_count = reader.read_uint32()
        self.flex_controller_offset = reader.read_uint32()

        self.flex_rule_count = reader.read_uint32()
        self.flex_rule_offset = reader.read_uint32()

        self.ik_chain_count = reader.read_uint32()
        self.ik_chain_offset = reader.read_uint32()

        self.mouth_count = reader.read_uint32()
        self.mouth_offset = reader.read_uint32()

        self.local_pose_paramater_count = reader.read_uint32()
        self.local_pose_parameter_offset = reader.read_uint32()

        self.surface_prop_offset = reader.read_uint32()

        if self.surface_prop_offset > 0:
            self.surface_prop_name = reader.read_from_offset(self.surface_prop_offset, reader.read_ascii_string)

        self.key_value_offset = reader.read_uint32()
        self.key_value_size = reader.read_uint32()

        self.local_ik_auto_play_lock_offset = reader.read_uint32()
        self.local_ik_auto_play_lock_count = reader.read_uint32()

        self.mass = reader.read_float()
        self.contents = reader.read_uint32()

        self.include_model_count = reader.read_uint32()
        self.include_model_offset = reader.read_uint32()

        self.virtual_model_pointer = reader.read_uint32()

        self.anim_block_name_offset = reader.read_uint32()
        self.anim_block_count = reader.read_uint32()
        self.anim_block_offset = reader.read_uint32()
        self.anim_block_model_pointer = reader.read_uint32()

        if self.anim_block_count > 0:
            if self.anim_block_name_offset > 0:
                self.anim_block_relative_path_file_name = reader.read_from_offset(
                    reader.tell() + self.anim_block_name_offset, reader.read_ascii_string)

        if self.anim_block_offset > 0:
            with reader.save_current_pos():
                reader.seek(self.anim_block_offset, 0)
                for offset in range(self.anim_block_count):
                    anim_block = SourceMdlAnimBlock()
                    anim_block.read(reader)
                    self.anim_blocks.append(anim_block)

        self.bone_table_by_name_offset = reader.read_uint32()

        self.vertex_base_pointer = reader.read_uint32()
        self.index_base_pointer = reader.read_uint32()

        self.directional_light_dot = reader.read_uint8()

        self.root_lod = reader.read_uint8()

        self.allowed_root_lod_count = reader.read_uint8()

        self.unused = reader.read_uint8()

        self.unused4 = reader.read_uint32()

        self.flex_controller_ui_count = reader.read_uint32()
        self.flex_controller_ui_offset = reader.read_uint32()

        self.vert_anim_fixed_point_scale = reader.read_float()
        self.surface_prop_offset = reader.read_uint32()

        self.studio_header2_offset = reader.read_uint32()

        self.unused2 = reader.read_uint32()

        reader.skip(16)
        self.vtx_offset = reader.read_uint32()
        self.vvd_offset = reader.read_uint32()
        # print('Found VTX:{} and VVD:{}'.format(self.vtx_offset, self.vvd_offset))
        if self.vvd_offset != 0 and self.vtx_offset != 0:
            with reader.save_current_pos():
                reader.seek(self.vtx_offset)
                self.vtx = VTX.SourceVtxFile49(file=ByteIO(byte_object=reader.read_bytes(-1)))
                reader.seek(self.vvd_offset)
                self.vvd = VVD.SourceVvdFile49(file=ByteIO(byte_object=reader.read_bytes(-1)))

        if self.body_part_count == 0 and self.local_sequence_count > 0:
            self.mdl_file_only_has_animations = True

    def read_header02(self, reader: ByteIO):

        self.source_bone_transform_count = reader.read_uint32()
        self.source_bone_transform_offset = reader.read_uint32()
        self.illum_position_attachment_index = reader.read_uint32()
        self.max_eye_deflection = reader.read_float()
        self.linear_bone_offset = reader.read_uint32()

        self.name_offset = reader.read_uint32()
        self.bone_flex_driver_count = reader.read_uint32()
        self.bone_table_by_name_offset = reader.read_uint32()
        self.reserved = list([reader.read_uint32() for _ in range(56)])


class SourceMdlBone:
    # BONE_SCREEN_ALIGN_SPHERE = 0x8
    # BONE_SCREEN_ALIGN_CYLINDER = 0x10
    # BONE_USED_BY_VERTEX_LOD0 = 0x400
    # BONE_USED_BY_VERTEX_LOD1 = 0x800
    # BONE_USED_BY_VERTEX_LOD2 = 0x1000
    # BONE_USED_BY_VERTEX_LOD3 = 0x2000
    # BONE_USED_BY_VERTEX_LOD4 = 0x4000
    # BONE_USED_BY_VERTEX_LOD5 = 0x8000
    # BONE_USED_BY_VERTEX_LOD6 = 0x10000
    # BONE_USED_BY_VERTEX_LOD7 = 0x20000
    # BONE_USED_BY_BONE_MERGE = 0x40000
    # BONE_FIXED_ALIGNMENT = 0x100000
    # BONE_HAS_SAVEFRAME_POS = 0x200000
    # BONE_HAS_SAVEFRAME_ROT = 0x400000

    class CONTENTS:
        SOLID = 0x1
        GRATE = 0x8
        MONSTER = 0x2000000
        LADDER = 0x20000000

        @classmethod
        def get_flags(cls, flag):
            flags = []
            for name, val in vars(cls).items():
                if name.isupper():
                    if (flag & val) > 0:
                        flags.append(name)
            return flags

    def __init__(self):

        self.boneOffset = 0
        self.name = ""
        self.boneControllerIndex = []
        self.nameOffset = 0
        self.parentBoneIndex = 0
        self.scale = 0
        self.position = SourceVector()
        self.quat = SourceQuaternion()
        self.animChannels = 0
        self.rotation = SourceVector()
        self.positionScale = SourceVector()
        self.rotationScale = SourceVector()
        self.poseToBoneColumn0 = SourceVector()
        self.poseToBoneColumn1 = SourceVector()
        self.poseToBoneColumn2 = SourceVector()
        self.poseToBoneColumn3 = SourceVector()
        self.qAlignment = SourceQuaternion()
        self.flags = 0
        self.proceduralRuleType = 0
        self.proceduralRuleOffset = 0
        self.physicsBoneIndex = 0
        self.surfacePropNameOffset = 0
        self.contents = 0
        self.unused = []
        self.theAxisInterpBone = None  # type: SourceMdlAxisInterpBone
        self.theQuatInterpBone = None  # type: SourceMdlQuatInterpBone
        self.theJiggleBone = None  # type: SourceMdlJiggleBone
        self.theSurfacePropName = ''
        self.STUDIO_PROC_AXISINTERP = 1
        self.STUDIO_PROC_QUATINTERP = 2
        self.STUDIO_PROC_AIMATBONE = 3
        self.STUDIO_PROC_AIMATATTACH = 4
        self.STUDIO_PROC_JIGGLE = 5

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        self.boneOffset = reader.tell()
        self.nameOffset = reader.read_uint32()
        self.parentBoneIndex = reader.read_int32()
        self.boneControllerIndex = [reader.read_int32() for _ in range(6)]
        self.position.read(reader)
        self.quat.read(reader)
        self.rotation.read(reader)
        self.positionScale.read(reader)
        self.rotationScale.read(reader)

        self.poseToBoneColumn0.x, self.poseToBoneColumn1.x, self.poseToBoneColumn2.x, self.poseToBoneColumn3.x = \
            reader.read_float(), reader.read_float(), reader.read_float(), reader.read_float()
        self.poseToBoneColumn0.y, self.poseToBoneColumn1.y, self.poseToBoneColumn2.y, self.poseToBoneColumn3.y = \
            reader.read_float(), reader.read_float(), reader.read_float(), reader.read_float()
        self.poseToBoneColumn0.z, self.poseToBoneColumn1.z, self.poseToBoneColumn2.z, self.poseToBoneColumn3.z = \
            reader.read_float(), reader.read_float(), reader.read_float(), reader.read_float()

        self.qAlignment.read(reader)
        self.flags = reader.read_uint32()
        self.proceduralRuleType = reader.read_uint32()
        self.proceduralRuleOffset = reader.read_uint32()
        self.physicsBoneIndex = reader.read_uint32()
        self.surfacePropNameOffset = reader.read_uint32()
        self.contents = reader.read_uint32()
        if mdl.version >= 48:
            _ = [reader.read_uint32() for _ in range(8)]
        if mdl.version >= 53:
            reader.skip(4 * 7)
        if self.nameOffset != 0:
            self.name = reader.read_from_offset(self.boneOffset + self.nameOffset, reader.read_ascii_string).encode(
                "ascii", 'ignore').decode('ascii')
        # print(self.boneOffset, self)
        # print(self.proceduralRuleType, self.proceduralRuleOffset)
        if self.proceduralRuleType != 0 and self.proceduralRuleOffset != 0:
            if self.proceduralRuleType == self.STUDIO_PROC_AXISINTERP:
                with reader.save_current_pos():
                    reader.seek(self.boneOffset + self.proceduralRuleOffset)
                    self.theAxisInterpBone = SourceMdlAxisInterpBone().read(reader)
            if self.proceduralRuleType == self.STUDIO_PROC_QUATINTERP:
                with reader.save_current_pos():
                    reader.seek(self.boneOffset + self.proceduralRuleOffset)
                    self.theQuatInterpBone = SourceMdlQuatInterpBone().read(reader)
            if self.proceduralRuleType == self.STUDIO_PROC_JIGGLE:
                with reader.save_current_pos():
                    reader.seek(self.boneOffset + self.proceduralRuleOffset)
                    self.theJiggleBone = SourceMdlJiggleBone().read(reader)
        if self.surfacePropNameOffset != 0:
            self.theSurfacePropName = reader.read_from_offset(self.boneOffset + self.surfacePropNameOffset,
                                                              reader.read_ascii_string)

        mdl.bones.append(self)

    def __repr__(self):
        return '<Bone "{}" pos:{} rot: {} parent index: {}>'.format(self.name, self.position.as_string,
                                                                    self.rotation.as_string, self.parentBoneIndex)


class SourceMdlJiggleBone:
    class JIGGLE:
        IS_FLEXIBLE = 0x01
        IS_RIGID = 0x02
        HAS_YAW_CONSTRAINT = 0x04
        HAS_PITCH_CONSTRAINT = 0x08
        HAS_ANGLE_CONSTRAINT = 0x10
        HAS_LENGTH_CONSTRAINT = 0x20
        HAS_BASE_SPRING = 0x40

        def __init__(self, value):
            self.value = value

        def get_flags(self):
            d_flags = []

            vars_ = {var: self.__class__.__dict__[var] for var in vars(self.__class__) if
                     not var.startswith('_') and var.isupper()}
            for var, int_ in vars_.items():
                if (self.value & int_) > 0:
                    d_flags.append(var)
            return d_flags

        def __repr__(self):
            return '<Flags:{}>'.format(self.get_flags())

        def __contains__(self, item):
            return item & self.value

    # define JIGGLE_IS_FLEXIBLE				0x01
    # define JIGGLE_IS_RIGID					0x02
    # define JIGGLE_HAS_YAW_CONSTRAINT		0x04
    # define JIGGLE_HAS_PITCH_CONSTRAINT		0x08
    # define JIGGLE_HAS_ANGLE_CONSTRAINT		0x10
    # define JIGGLE_HAS_LENGTH_CONSTRAINT	0x20
    # define JIGGLE_HAS_BASE_SPRING			0x40

    def __init__(self):
        self.flags = 0
        self.length = 0.0
        self.tipMass = 0.0
        self.yawStiffness = 0.0
        self.yawDamping = 0.0
        self.pitchStiffness = 0.0
        self.pitchDamping = 0.0
        self.alongStiffness = 0.0
        self.alongDamping = 0.0
        self.angleLimit = 0.0
        self.minYaw = 0.0
        self.maxYaw = 0.0
        self.yawFriction = 0.0
        self.yawBounce = 0.0
        self.minPitch = 0.0
        self.maxPitch = 0.0
        self.pitchBounce = 0.0
        self.pitchFriction = 0.0
        self.baseMass = 0.0
        self.baseStiffness = 0.0
        self.baseDamping = 0.0
        self.baseMinLeft = 0.0
        self.baseMaxLeft = 0.0
        self.baseLeftFriction = 0.0
        self.baseMinUp = 0.0
        self.baseMaxUp = 0.0
        self.baseUpFriction = 0.0
        self.baseMinForward = 0.0
        self.baseMaxForward = 0.0
        self.baseForwardFriction = 0.0

    def read(self, reader: ByteIO):
        self.flags = self.JIGGLE(reader.read_int32())
        self.length = reader.read_float()
        self.tipMass = reader.read_float()
        self.yawStiffness = reader.read_float()
        self.yawDamping = reader.read_float()
        self.pitchStiffness = reader.read_float()
        self.pitchDamping = reader.read_float()
        self.alongStiffness = reader.read_float()
        self.alongDamping = reader.read_float()
        self.angleLimit = reader.read_float()
        self.minYaw = reader.read_float()
        self.maxYaw = reader.read_float()
        self.yawFriction = reader.read_float()
        self.yawBounce = reader.read_float()
        self.minPitch = reader.read_float()
        self.maxPitch = reader.read_float()
        self.pitchFriction = reader.read_float()
        self.pitchBounce = reader.read_float()
        self.baseMass = reader.read_float()
        self.baseMinLeft = reader.read_float()
        self.baseMaxLeft = reader.read_float()
        self.baseLeftFriction = reader.read_float()
        self.baseMinUp = reader.read_float()
        self.baseMaxUp = reader.read_float()
        self.baseUpFriction = reader.read_float()
        self.baseMinForward = reader.read_float()
        self.baseMaxForward = reader.read_float()
        self.baseForwardFriction = reader.read_float()
        return self

    def __repr__(self):
        return '<JiggleBone flags:{0.flags} mass:{0.tipMass} length:{0.length}>'.format(self)


class SourceMdlAxisInterpBone:
    def __init__(self):
        self.control = 0
        self.axis = 0
        self.pos = []
        self.quat = []

    def read(self, reader: ByteIO):
        self.control = reader.read_uint32()
        self.pos = [SourceVector().read(reader) for _ in range(6)]
        self.quat = [SourceQuaternion().read(reader) for _ in range(6)]
        return self

    def __str__(self):
        return '<AxisInterpBone control:{}>'.format(self.control)

    def __repr__(self):
        return '<AxisInterpBone control:{}>'.format(self.control)


class SourceMdlQuatInterpBone:
    def __init__(self):
        self.controlBoneIndex = 0
        self.triggerCount = 0
        self.triggerOffset = 0
        self.theTriggers = []

    def read(self, reader: ByteIO):
        self.controlBoneIndex = reader.read_uint32()
        self.triggerCount = reader.read_uint32()
        self.triggerOffset = reader.read_uint32()
        if self.triggerCount > 0 and self.triggerOffset != 0:
            self.theTriggers = [SourceMdlQuatInterpBoneInfo().read(reader) for _ in range(self.triggerCount)]
        return self

    def __str__(self):
        return '<QuatInterpBone control bone index:{}>'.format(self.controlBoneIndex)

    def __repr__(self):
        return '<QuatInterpBone control index:{}>'.format(self.controlBoneIndex)


class SourceMdlQuatInterpBoneInfo:
    def __init__(self):
        self.inverseToleranceAngle = 0
        self.trigger = SourceQuaternion()
        self.pos = SourceVector()
        self.quat = SourceQuaternion()

    def read(self, reader: ByteIO):
        self.inverseToleranceAngle = reader.read_float()
        self.trigger.read(reader)
        self.pos.read(reader)
        self.quat.read(reader)
        return self


class SourceMdlBoneController:
    def __init__(self):
        self.boneIndex = 0
        self.type = 0
        self.startBlah = 0
        self.endBlah = 0
        self.restIndex = 0
        self.inputField = 0
        self.unused = []

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        self.boneIndex = reader.read_uint32()
        self.type = reader.read_uint32()
        self.startBlah = reader.read_uint32()
        self.endBlah = reader.read_uint32()
        self.restIndex = reader.read_uint32()
        self.inputField = reader.read_uint32()
        if mdl.version > 10:
            self.unused = [reader.read_uint32() for _ in range(8)]
        mdl.bone_controllers.append(self)
        return self

    def __str__(self):
        return '<BoneController bone index:{}>'.format(self.boneIndex)

    def __repr__(self):
        return '<BoneController bone index:{}>'.format(self.boneIndex)


class SourceMdlFlexDesc:
    def __init__(self):
        self.name_offset = 0
        self.name = ''
        self.desc_used_by_flex = False
        self.desc_used_by_flex_rule = False
        self.desc_used_by_eyelid = False

    def read(self, reader: ByteIO):
        entry = reader.tell()
        self.name_offset = reader.read_uint32()
        if self.name_offset != 0:
            self.name = reader.read_from_offset(entry + self.name_offset, reader.read_ascii_string)
        pass

    def __repr__(self):
        return '<FlexDesc name:"{}">'.format(self.name)


class SourceMdlFlexController:
    def __init__(self):
        self.typeOffset = 0
        self.nameOffset = 0
        self.localToGlobal = 0
        self.min = 0.0
        self.max = 0.0
        self.theName = ''
        self.theType = ''

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        entry = reader.tell()
        self.typeOffset = reader.read_uint32()
        self.nameOffset = reader.read_uint32()
        self.localToGlobal = reader.read_int32()
        self.min = reader.read_float()
        self.max = reader.read_float()
        if self.typeOffset != 0:
            self.theType = reader.read_from_offset(entry + self.typeOffset, reader.read_ascii_string)
        else:
            self.theType = ''
        if self.nameOffset != 0:
            self.theName = reader.read_from_offset(entry + self.nameOffset, reader.read_ascii_string)
        else:
            self.theName = 'blank_name_' + str(len(mdl.flex_descs))

        if mdl.flex_controllers.__len__() > 0:
            mdl.model_command_is_used = True
        mdl.flex_controllers.append(self)

    def __repr__(self):
        return '<FlexController name:"{}" type:{} min/max:{}/{} localToGlobal:{}>'.format(self.theName, self.theType,
                                                                                          self.min, self.max,
                                                                                          self.localToGlobal)


class SourceMdlFlexRule:
    def __init__(self):
        self.flex_index = 0
        self.op_count = 0
        self.op_offset = 0
        self.mdl = None  # type: SourceMdlFileData
        self.flex_ops = []

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        self.mdl = mdl
        entry = reader.tell()
        self.flex_index = reader.read_uint32()
        self.op_count = reader.read_uint32()
        self.op_offset = reader.read_uint32()
        with reader.save_current_pos():
            if self.op_count > 0 and self.op_offset != 0:
                reader.seek(entry + self.op_offset)
                for _ in range(self.op_count):
                    flex_op = SourceMdlFlexOp()
                    flex_op.read(reader, mdl)
                    self.flex_ops.append(flex_op)
            mdl.flex_descs[self.flex_index].desc_used_by_flex_rule = True
            mdl.flex_rules.append(self)

    def __repr__(self):
        return '<Flex rule "{}" op count:{}>'.format(self.mdl.flex_descs[self.flex_index].name, self.op_count)


class FlexOpType(Enum):
    STUDIO_CONST = 1
    STUDIO_FETCH1 = 2
    STUDIO_FETCH2 = 3
    STUDIO_ADD = 4
    STUDIO_SUB = 5
    STUDIO_MUL = 6
    STUDIO_DIV = 7
    STUDIO_NEG = 8
    STUDIO_EXP = 9
    STUDIO_OPEN = 10
    STUDIO_CLOSE = 11
    STUDIO_COMMA = 12
    STUDIO_MAX = 13
    STUDIO_MIN = 14
    STUDIO_2WAY_0 = 15
    STUDIO_2WAY_1 = 16
    STUDIO_NWAY = 17
    STUDIO_COMBO = 18
    STUDIO_DOMINATE = 19
    STUDIO_DME_LOWER_EYELID = 20
    STUDIO_DME_UPPER_EYELID = 21


class SourceMdlFlexOp:

    def __init__(self):
        self.op = FlexOpType
        self.index = 0
        self.value = 0
        self.mdl = None  # type: SourceMdlFileData

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        self.mdl = mdl
        self.op = FlexOpType(reader.read_uint32())
        if self.op == FlexOpType.STUDIO_CONST:
            self.value = reader.read_float()
        else:
            self.index = reader.read_uint32()
            if self.op == FlexOpType.STUDIO_FETCH2:
                mdl.flex_descs[self.index].desc_used_by_flex_rule = True

    def __repr__(self):

        if self.op == FlexOpType.STUDIO_CONST:
            return '<FlexOp op:{} value:{}>'.format(self.op.name, self.value)
        else:
            return '<FlexOp op:{} for "{}">'.format(self.op.name, self.mdl.flex_descs[self.index].name)


class SourceMdlAttachment:
    def __init__(self):
        self.name = ""
        self.type = 0
        self.attachmentPoint = SourceVector
        self.vectors = []
        self.nameOffset = 0
        self.flags = 0
        self.localBoneIndex = 0
        self.parent_bone = None  # type: SourceMdlBone
        self.localM11 = 0.0
        self.localM12 = 0.0
        self.localM13 = 0.0
        self.localM14 = 0.0
        self.localM21 = 0.0
        self.localM22 = 0.0
        self.localM23 = 0.0
        self.localM24 = 0.0
        self.localM31 = 0.0
        self.localM32 = 0.0
        self.localM33 = 0.0
        self.localM34 = 0.0
        self.rot = SourceVector()
        self.pos = SourceVector()
        self.unused = []

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        entry = reader.tell()
        if mdl.version == 10:
            self.name = reader.read_ascii_string(64)
        else:
            self.nameOffset = reader.read_uint32()
            self.name = reader.read_from_offset(self.nameOffset + entry, reader.read_ascii_string)
            self.flags = reader.read_uint32()
            self.localBoneIndex = reader.read_uint32()
            try:
                self.parent_bone = mdl.bones[self.localBoneIndex]
            except IndexError:
                self.parent_bone = SourceMdlBone()
            self.localM11 = reader.read_float()
            self.localM12 = reader.read_float()
            self.localM13 = reader.read_float()
            self.localM14 = reader.read_float()
            self.localM21 = reader.read_float()
            self.localM22 = reader.read_float()
            self.localM23 = reader.read_float()
            self.localM24 = reader.read_float()
            self.localM31 = reader.read_float()
            self.localM32 = reader.read_float()
            self.localM33 = reader.read_float()
            self.localM34 = reader.read_float()
            self.unused = [reader.read_uint32() for _ in range(8)]
            self.rot.x, self.rot.y, self.rot.z = math_utilities.convert_rotation_matrix_to_degrees(self.localM11,
                                                                                                   self.localM21,
                                                                                                   self.localM31,
                                                                                                   self.localM12,
                                                                                                   self.localM22,
                                                                                                   self.localM32,
                                                                                                   self.localM33)
            self.pos.y = round(self.localM24, 3)
            self.pos.z = round(self.localM34, 3)
            self.pos.x = round(self.localM14, 3)

        mdl.attachments.append(self)

    def __repr__(self):
        return '<Attachment name:"{}" parent bone: {} loc:{} rot:{}>'.format(self.name, self.parent_bone,
                                                                             self.pos.as_string,
                                                                             self.rot.to_degrees().as_string)


class SourceMdlBodyPart:
    def __init__(self):
        self.name_offset = 0
        self.model_count = 0
        self.base = 0
        self.model_offset = 0
        self.name = ""
        self.models = []  # type: List[SourceMdlModel]
        self.flex_frames = []  # type: List[FlexFrame]
        self.mdl = None  # type: SourceMdlFileData

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        self.mdl = mdl
        entry = reader.tell()
        self.name_offset = reader.read_uint32()
        self.name = reader.read_from_offset(entry + self.name_offset,
                                            reader.read_ascii_string) if self.name_offset != 0 else "no-name{}".format(
            len(mdl.body_parts))
        self.model_count = reader.read_uint32()
        self.base = reader.read_uint32()
        self.model_offset = reader.read_uint32()
        entry2 = reader.tell()
        if self.model_count > 0:
            reader.seek(entry + self.model_offset)
            for _ in range(self.model_count):
                SourceMdlModel().read(reader, self)
        reader.seek(entry2)
        mdl.body_parts.append(self)

    def __repr__(self):
        return '<BodyPart name:"{}" model_path count:{} >'.format(self.name, self.model_count)


class SourceMdlModel:
    def __init__(self):
        self.name = ''
        self.type = 0
        self.bounding_radius = 0.0
        self.mesh_count = 0
        self.mesh_offset = 0
        self.vertex_count = 0
        self.vertex_offset = 0
        self.tangent_offset = 0
        self.attachment_count = 0
        self.attachment_offset = 0
        self.eyeball_count = 0
        self.eyeball_offset = 0
        self.vertex_data = SourceMdlModelVertexData()
        self.unused = []
        self.meshes = []  # type: List[SourceMdlMesh]
        self.eyeballs = []  # type: List[SourceMdlEyeball]
        self.flex_frames = []  # type: List[FlexFrame]
        self.body_part = None  # type: SourceMdlBodyPart

    @property
    def flex_count(self):
        acc = 0
        for mesh in self.meshes:
            acc +=mesh.flex_count
        return acc

    def read(self, reader: ByteIO, body_part: SourceMdlBodyPart):
        self.body_part = body_part
        entry = reader.tell()
        self.name = reader.read_ascii_string(64)
        if not self.name:
            self.name = "blank"

        self.type = reader.read_uint32()
        self.bounding_radius = reader.read_float()
        self.mesh_count = reader.read_uint32()
        self.mesh_offset = reader.read_uint32()
        self.vertex_count = reader.read_uint32()
        self.vertex_offset = reader.read_uint32()
        self.tangent_offset = reader.read_uint32()
        self.attachment_count = reader.read_uint32()
        self.attachment_offset = reader.read_uint32()
        self.eyeball_count = reader.read_uint32()
        self.eyeball_offset = reader.read_uint32()
        self.vertex_data.read(reader)
        self.unused = [reader.read_uint32() for _ in range(8)]
        entry2 = reader.tell()
        reader.seek(entry + self.eyeball_offset, 0)
        for _ in range(self.eyeball_count):
            SourceMdlEyeball().read(reader, self)
        reader.seek(entry + self.mesh_offset, 0)
        for _ in range(self.mesh_count):
            SourceMdlMesh().read(reader, self)

        reader.seek(entry2, 0)
        body_part.models.append(self)

    def __repr__(self):
        return '<Model name:"{}" type:{} mesh_data count:{} meshes:{} eyeballs:{}>'.format(self.name, self.type,
                                                                                           self.mesh_count,
                                                                                           self.meshes,
                                                                                           self.eyeballs)


class SourceMdlModelVertexData:
    def __init__(self):
        self.vertex_data_pointer = 0
        self.tangent_data_pointer = 0

    def read(self, reader: ByteIO):
        self.vertex_data_pointer = reader.read_uint32()
        self.tangent_data_pointer = reader.read_uint32()

    def __str__(self):
        return '<ModelVertexData vertex pointer:{} tangent pointer:{}>'.format(self.vertex_data_pointer,
                                                                               self.tangent_data_pointer)

    def __repr__(self):
        return '<ModelVertexData vertex pointer:{} tangent pointer:{}>'.format(self.vertex_data_pointer,
                                                                               self.tangent_data_pointer)


class SourceMdlEyeball:
    def __init__(self):
        self.name_offset = 0
        self.bone_index = 0
        self.org = SourceVector()
        self.z_offset = 0.0
        self.radius = 0.0
        self.up = SourceVector()
        self.forward = SourceVector()
        self.texture = 0

        self.unused1 = 0
        self.iris_scale = 0.0
        self.unused2 = 0
        self.upper_flex_desc = []
        self.lower_flex_desc = []
        self.upper_target = []
        self.lower_target = []

        self.upper_lid_flex_desc = 0
        self.lower_lid_flex_desc = 0
        self.unused = []
        self.eyeball_is_non_facs = b'\x00'
        self.unused3 = ''
        self.unused4 = []

        self.name = ''
        self.texture_index = 0

    def read(self, reader: ByteIO, model: SourceMdlModel):
        entry = reader.tell()
        self.name_offset = reader.read_uint32()
        self.name = reader.read_from_offset(entry + self.name_offset, reader.read_ascii_string)
        self.bone_index = reader.read_uint32()
        self.org.read(reader)
        self.z_offset = reader.read_float()
        self.radius = reader.read_float()
        self.up.read(reader)
        self.forward.read(reader)
        self.texture = reader.read_int32()
        self.unused1 = reader.read_uint32()
        self.iris_scale = reader.read_float()
        self.unused2 = reader.read_uint32()
        self.upper_flex_desc = [reader.read_uint32() for _ in range(3)]
        self.lower_flex_desc = [reader.read_uint32() for _ in range(3)]
        self.upper_target = [reader.read_float() for _ in range(3)]
        self.lower_target = [reader.read_float() for _ in range(3)]
        self.upper_lid_flex_desc = reader.read_uint32()
        self.lower_lid_flex_desc = reader.read_uint32()
        self.unused = [reader.read_float() for _ in range(4)]
        self.eyeball_is_non_facs = reader.read_uint8()
        self.unused3 = reader.read_ascii_string(3)
        self.unused4 = [reader.read_uint32() for _ in range(7)]
        model.eyeballs.append(self)

    def __str__(self):
        return '<Eyeball name:"{}" bone:{} xyz:{}>'.format(self.name, self.bone_index, self.org.as_string)

    def __repr__(self):
        return '<Eyeball name:"{}" bone:{} xyz:{}>'.format(self.name, self.bone_index, self.org.as_string)


class SourceMdlMesh:
    def __init__(self):
        self.material_index = 0
        self.model_offset = 0
        self.vertex_count = 0
        self.vertex_index_start = 0
        self.flex_count = 0
        self.flex_offset = 0
        self.material_type = 0
        self.material_param = 0
        self.id = 0
        self.center = SourceVector()

        self.vertexData = SourceMdlMeshVertexData()
        self.unused = []  # 8
        self.flexes = []  # type: List[SourceMdlFlex]
        self.model = None  # type: SourceMdlModel

    def read(self, reader: ByteIO, model: SourceMdlModel):
        self.model = model
        entry = reader.tell()

        self.material_index, self.model_offset, self.vertex_count, self.vertex_index_start = reader.read_fmt('4I')
        self.flex_count, self.flex_offset, self.material_type, self.material_param, self.id = reader.read_fmt('5I')
        self.center.read(reader)
        self.vertexData.read(reader)
        self.unused = [reader.read_uint32() for _ in range(8)]
        if self.material_type == 1:
            model.eyeballs[self.material_param].texture_index = self.material_index
        entry2 = reader.tell()
        if self.flex_count > 0 and self.flex_offset != 0:
            reader.seek(entry + self.flex_offset, 0)
            for _ in range(self.flex_count):
                t = time.time()
                temp = SourceMdlFlex().read(reader, self)
                # print('Reading of "{}" flex took'.format(model.body_part.mdl.flex_descs[temp.flex_desc_index].name),
                #       time.time() - t, 'sec')
        reader.seek(entry2, 0)
        model.meshes.append(self)

    def __repr__(self):
        return '<Mesh material inxes:{} vertex count:{} flex count:{}>'.format(self.material_index,
                                                                               self.vertex_count,
                                                                               self.flex_count,
                                                                               self.flexes)


class SourceMdlMeshVertexData:
    def __init__(self):
        self.model_vertex_data_pointer = 0
        self.lod_vertex_count = []

    def read(self, reader: ByteIO):
        self.model_vertex_data_pointer = reader.read_uint32()
        self.lod_vertex_count = [reader.read_uint32() for _ in range(8)]

    def __str__(self):
        return '<MeshVertexData vertex pointer:{}, LODs vertex count:{}>'.format(self.model_vertex_data_pointer,
                                                                                 self.lod_vertex_count)

    def __repr__(self):
        return '<MeshVertexData vertex pointer:{}, LODs vertex count:{}>'.format(self.model_vertex_data_pointer,
                                                                                 self.lod_vertex_count)


class SourceMdlFlex:
    def __init__(self):
        self.flex_desc_index = 0
        self.target0 = 0.0
        self.target1 = 0.0
        self.target2 = 0.0
        self.target3 = 0.0
        self.vert_count = 0
        self.vert_offset = 0
        self.flex_desc_partner_index = 0
        self.vert_anim_type = 0
        self.unused_char = []  # 3
        self.unused = []  # 6
        self.the_vert_anims = []
        self.STUDIO_VERT_ANIM_NORMAL = 0
        self.STUDIO_VERT_ANIM_WRINKLE = 1

    def read(self, reader: ByteIO, mesh: SourceMdlMesh):
        entry = reader.tell()
        self.flex_desc_index, self.target0, self.target1, self.target2, self.target3 = reader.read_fmt('I4f')
        self.vert_count, self.vert_offset, self.flex_desc_partner_index = reader.read_fmt('3I')
        # print('Reading', mesh.model.body_part.mdl.flex_descs[self.flex_desc_index].name, 'flex')
        self.vert_anim_type = reader.read_uint8()
        self.unused_char = reader.read_fmt('3B')
        self.unused = reader.read_fmt('6I')

        if self.vert_count > 0 and self.vert_offset != 0:
            with reader.save_current_pos():
                reader.seek(entry + self.vert_offset)
                if self.vert_anim_type == self.STUDIO_VERT_ANIM_WRINKLE:
                    vert_anim_type = SourceMdlVertAnimWrinkle
                else:
                    vert_anim_type = SourceMdlVertAnim
                for _ in range(self.vert_count):
                    self.the_vert_anims.append(vert_anim_type().read(reader, self))

        mesh.flexes.append(self)
        return self

    def __repr__(self):
        return '<Flex Desc index:{} anim type:{}, vertex count:{} vertex offset:{}>'.format(self.flex_desc_index,
                                                                                            self.vert_anim_type,
                                                                                            self.vert_count,
                                                                                            self.vert_offset)


class SourceMdlVertAnim:
    vert_anim_fixed_point_scale = 1 / 4096

    def __init__(self):
        self.index = 0
        self.speed = 0
        self.side = 0
        self.the_delta = []  # 3
        self.the_n_delta = []  # 3

    def read(self, reader: ByteIO, flex: SourceMdlFlex):
        self.index, self.speed, self.side = reader.read_fmt('hBB')
        self.the_delta = [SourceFloat16bits().read(reader).float_value for _ in range(3)]
        self.the_n_delta = [SourceFloat16bits().read(reader).float_value for _ in range(3)]
        return self

    def __repr__(self):
        return '<Vertex Animation index:{} speed:{} side:{} delta:{}>'.format(self.index, self.speed, self.side,
                                                                              self.the_delta)


class SourceMdlVertAnimWrinkle(SourceMdlVertAnim):
    def __init__(self):
        super().__init__()
        self.wrinkle_delta = 0

    def read(self, reader: ByteIO, flex: SourceMdlFlex):
        super().read(reader, flex)
        self.wrinkle_delta = reader.read_uint16()
        return self


class SourceMdlTexture:
    def __init__(self):
        self.name_offset = 0
        self.flags = 0
        self.used = 0
        self.unused1 = 0
        self.material_pointer = 0
        self.client_material_pointer = 0
        self.unused = []  # len 10
        self.path_file_name = 'texture' + pformat(random.randint(0, 256))

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        entry = reader.tell()
        self.name_offset = reader.read_uint32()
        self.flags = reader.read_uint32()
        self.used = reader.read_uint32()
        self.unused1 = reader.read_uint32()
        self.material_pointer = reader.read_uint32()
        self.client_material_pointer = reader.read_uint32()
        self.unused = [reader.read_uint32() for _ in range(10 if mdl.version < 53 else 5)]
        with reader.save_current_pos():
            if self.name_offset != 0:
                self.path_file_name = reader.read_from_offset(entry + self.name_offset, reader.read_ascii_string)
        mdl.textures.append(self)

    def __repr__(self):
        return '<Texture name:"{}">'.format(self.path_file_name)


class SourceMdlAnimBlock:
    """FROM: SourceEngineXXXX_source\public\studio.h
    // used for piecewise loading of animation data
    struct mstudioanimblock_t
    {
       DECLARE_BYTESWAP_DATADESC();
       int					datastart;
       int					dataend;
    };"""

    def __init__(self):
        self.data_start = 0
        self.data_end = 0

    def read(self, reader: ByteIO):
        self.data_start = reader.read_uint32()
        self.data_end = reader.read_uint32()

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)


class SourceMdlMouth:

    def __init__(self):
        self.bone = 0
        self.forward = SourceVector()
        self.flex_desc_index = 0

    def read(self, reader: ByteIO):
        self.bone = reader.read_int32()
        self.forward.read(reader)
        self.flex_desc_index = reader.read_int32()
        return self

    def __repr__(self):
        return '<SourceMdlMouth bone:{} flex:{}  {}>'.format(self.bone, self.flex_desc_index, self.forward)


class SourceBoneFlexDriver:

    def __init__(self):
        self.bone_index = 0
        self.controller_count = 0
        self.controller_offset = 0
        self.controllers = []  # type: List[SourceBoneFlexController]
        self.mdl = None  # type:SourceMdlFileData

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        self.mdl = mdl
        self.bone_index, self.controller_count = reader.read_fmt('2i')
        entry = reader.tell()
        self.controller_offset = reader.read_int32()
        with reader.save_current_pos():
            reader.seek(entry + self.controller_offset)
            for _ in range(self.controller_count):
                controller = SourceBoneFlexController().read(reader, mdl)
                self.controllers.append(controller)

        return self

    def __repr__(self):
        return '<BoneFlexDriver bone:"{}" controller count:{}>'.format(self.mdl.bones[self.bone_index].name,
                                                                       self.controller_count)


class SourceBoneFlexController:

    def __init__(self):
        self.bone_component = 0
        self.flex_index = 0
        self.min = 0
        self.max = 0
        self.mdl = None  # type:SourceMdlFileData

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        self.mdl = mdl
        self.bone_component, self.flex_index = reader.read_fmt('2i')
        self.min, self.max = reader.read_fmt('2f')
        return self

    def __repr__(self):
        return '<BoneFlexController bone component:{} flex"{}" min\max:{}\{}>'.format(self.bone_component,
                                                                                      self.mdl.flex_descs[
                                                                                          self.flex_index].name,
                                                                                      self.min, self.max)


class FlexControllerRemapType(IntEnum):
    FLEXCONTROLLER_REMAP_PASSTHRU = 0
    FLEXCONTROLLER_REMAP_2WAY = 1  # Control 0 -> ramps from 1-0 from 0->0.5. Control 1 -> ramps from 0-1 from 0.5->1
    FLEXCONTROLLER_REMAP_NWAY = 2  # StepSize = 1 / (control count-1) Control n -> ramps from 0-1-0 from (n-1)*StepSize to n*StepSize to (n+1)*StepSize. A second control is needed to specify amount to use
    FLEXCONTROLLER_REMAP_EYELID = 2


class SourceFlexControllerUI:
    def __init__(self):
        self.name_offset = 0
        self.name = 0
        self.index1 = 0
        self.index2 = 0
        self.index3 = 0
        self.remap_type = 0
        self.stereo = False
        self.unused = []

    def read(self, reader: ByteIO):
        entry = reader.tell()
        self.name_offset = reader.read_int32()
        self.name = reader.read_from_offset(entry + self.name_offset, reader.read_ascii_string)
        self.index1, self.index2, self.index3 = reader.read_fmt('3i')
        self.stereo = reader.read_uint8()
        self.remap_type = FlexControllerRemapType(reader.read_uint8())
        self.unused = reader.read_fmt('2b')

    def __repr__(self):
        return '<SourceFlexControllerUI "{}" remap:{} indexes:{} {} {}>'.format(self.name, self.remap_type.name,
                                                                                self.index1,
                                                                                self.index2, self.index3)


class FlexFrame:
    def __init__(self):
        self.flex_name = ""
        self.flex_description = ""
        self.has_partner = False
        self.partner = None
        self.flex_split = 0.0
        self.vertex_offsets = []  # type: List[int]
        self.flexes = []  # type: List[SourceMdlFlex]

    def __repr__(self):
        return '<FlexFrame {} flexes:{} mesh_data inds:{}>'.format(self.flex_name, self.flexes, self.vertex_offsets)
