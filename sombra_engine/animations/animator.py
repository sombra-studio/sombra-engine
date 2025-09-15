from sombra_engine.animations import Animation, Pose
from sombra_engine.models import SkeletalMesh
from sombra_engine.primitives import Transform


class Animator:
    def __init__(self, mesh: SkeletalMesh):
        self.time = 0.0
        self.mesh = mesh
        self.animation: Animation | None = None
        self.is_paused = False
        self.keyframes_count = 0
        self.keyframe_duration = 0.0

    def load_animation(self, animation: Animation):
        self.time = 0.0
        self.animation = animation
        self.keyframes_count = len(self.animation.keyframes)
        self.keyframe_duration = self.animation.length / self.keyframes_count

    def update(self, dt: float):
        if not self.animation or self.is_paused:
            return

        self.time += dt
        if self.time > self.animation.length:
            self.time = self.time % self.animation.length

        # Get the poses in between
        t = self.time % self.keyframe_duration
        interpolated_pose = self.interpolate(t)
        self.mesh.set_pose(interpolated_pose)

    def pause(self):
        self.is_paused = True

    def play(self):
        self.is_paused = False

    def interpolate(self, t: float) -> Pose:
        idx = int(self.time // self.keyframe_duration)
        prev_pose = self.animation.keyframes[idx].pose
        next_idx = idx + 1 if idx < self.keyframes_count else 0
        next_pose = self.animation.keyframes[next_idx].pose

        # interpolate between the two poses
        bones_transforms = []
        n = len(prev_pose.bones_transforms)
        for i in range(n):
            transform = Transform.interpolate(
                prev_pose.bones_transforms[i],
                next_pose.bones_transforms[i],
                t
            )
            bones_transforms.append(transform)
        new_pose = Pose(bones_transforms)
        return new_pose
