from importlib.resources import files
from pyglet.enums import GeometryMode
from pyglet.graphics import Batch, Group, Shader, ShaderProgram
from pyglet.math import Mat4


from sombra_engine.animations import Animation, Skeleton
from sombra_engine.graphics import SkeletalMaterialGroup
from sombra_engine.models import Mesh
from sombra_engine.primitives import (
    Material, SceneObject, Transform, VertexGroup
)


class SkeletalMesh(Mesh):
    def __init__(
        self,
        name: str,
        vertex_groups: dict[str, VertexGroup] = None,
        materials: dict[str, Material] = None,
        skeleton: Skeleton = None,
        mode: GeometryMode = GeometryMode.TRIANGLES,
        batch: Batch = None,
        group: Group = None,
        program: ShaderProgram = None,
        transform: Transform = Transform(),
        parent: SceneObject | None = None
    ):
        if not program:
            vs_src = files('sombra_engine.shaders').joinpath(
                'skeletal.vert'
            ).read_text()
            vert_shader = Shader(vs_src, 'vertex')

            fs_src = files('sombra_engine.shaders').joinpath(
                'blinn_barycentric.frag'
                # 'normals.frag'
            ).read_text()
            frag_shader = Shader(fs_src, 'fragment')

            program = ShaderProgram(vert_shader, frag_shader)
        super().__init__(
            name=name,
            vertex_groups=vertex_groups,
            materials=materials,
            mode=mode,
            batch=batch,
            group=group,
            program=program,
            transform=transform,
            parent=parent
        )
        self.skeleton = skeleton
        self.time = 0.0
        self.animations: dict[str, Animation] = {}
        self.current_animation: Animation | None = None
        self.is_paused = False
        self.keyframes_count = 0
        self.keyframe_duration = 0.0

    def create_material_groups(self) -> dict[str, SkeletalMaterialGroup]:
        groups = {}
        for name, material in self.materials.items():
            new_group = SkeletalMaterialGroup(
                material, self.program, self.get_matrix(),
                order=0, parent=self.group
            )
            groups[name] = new_group
        return groups

    def create_vertex_lists(self):
        # first calculate normals
        self.calculate_normals()

        vlists = []

        for vg_name, vg in self.vertex_groups.items():
            (
                position_list, normal_list, tangent_list, tex_coords_list,
                bones_ids_list, weights_list
            ) = self.get_lists_for_vertex_group(vg_name)
            material_group = self.material_groups[vg.material.name]
            vl = self.program.vertex_list(
                len(vg.triangles) * 3, self.mode,
                batch=self.batch, group=material_group,
                position=('f', position_list),
                normal=('f', normal_list),
                tangent=('f', tangent_list),
                tex_coords=('f', tex_coords_list),
                bones_ids=('i', bones_ids_list),
                weights=('f', weights_list)
            )
            vlists.append(vl)
        return vlists

    def get_lists_for_vertex_group(self, vertex_group_name: str) -> tuple[
        list[float], list[float], list[float], list[float], list[int],
        list[float]
    ]:
        if vertex_group_name not in self.vertex_groups:
            raise KeyError(
                f"Couldn't find key {vertex_group_name} for vertex group in "
                f"mesh {self.name}"
            )
        position_list = []
        normal_list = []
        tangent_list = []
        tex_coords_list = []
        bones_ids_list = []
        weights_list = []

        for triangle in self.vertex_groups[vertex_group_name].triangles:
            for v in triangle.vertices:
                position_list += [v.position.x, v.position.y, v.position.z]
                normal_list += [v.normal.x, v.normal.y, v.normal.z]
                tangent_list += [v.tangent.x, v.tangent.y, v.tangent.z]
                tex_coords_list += [v.tex_coords.x, v.tex_coords.y]
                bones_ids_list += [*v.bones_ids]
                weights_list += [
                    v.weights.x, v.weights.y, v.weights.z, v.weights.w
                ]
        return (
            position_list, normal_list, tangent_list, tex_coords_list,
            bones_ids_list, weights_list
        )

    def set_bones_transforms(self, bones_transforms: list[Mat4]):
        # This is not convenient because it has a copy of all the transforms
        # for all material groups
        for mg in self.material_groups.values():
            mg.bones_transforms = bones_transforms

    def set_animation(self, name: str):
        if name in self.animations:
            self.time = 0.0
            self.current_animation = self.animations[name]
            self.keyframes_count = len(self.current_animation.keyframes)
            # Here we are using the same duration for every keyframe
            self.keyframe_duration = (
                self.current_animation.length / self.keyframes_count
            )

    def update(self, dt: float):
        if not self.current_animation or self.is_paused:
            return

        self.time += dt
        if self.time > self.current_animation.length:
            self.time = self.time % self.current_animation.length

        # Get the poses in between
        t = self.time % self.keyframe_duration
        bones_transforms = self.interpolate(t)
        self.set_bones_transforms(bones_transforms)

    def pause(self):
        self.is_paused = True

    def play(self):
        self.is_paused = False

    def interpolate(self, t: float) -> list[Mat4]:
        idx = int(self.time // self.keyframe_duration)
        prev_pose = self.current_animation.keyframes[idx].pose
        next_idx = idx + 1 if idx + 1 < self.keyframes_count else 0
        next_pose = self.current_animation.keyframes[next_idx].pose

        # interpolate between the two poses
        curr_pose_translations = (
            (1 - t) * prev_pose.translations + t * next_pose.translations
        )
        bones_transforms = [Mat4()]
        return bones_transforms
