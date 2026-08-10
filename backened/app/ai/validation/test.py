from ..schemas.scene import Scene
from .validation import validate_scene


valid_scene = Scene(
    scene_number=1,
    location="Factory",
    time_of_day="night",
)

print("Valid scene:", validate_scene(valid_scene))


invalid_scene = Scene(
    scene_number=-1,
    location="   ",
    time_of_day="banana",
)

print("Invalid scene:", validate_scene(invalid_scene))