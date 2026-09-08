from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.service.scene_service import SceneService


class FilmStateEngine:
    @staticmethod
    async def get_film_state(db:AsyncSession,scene_id:int,):
        scene = await SceneService.get_scene_with_relationships(db,scene_id,)
        if scene is None :
            return None
        return scene

    @staticmethod
    def compare_values(
        previous: dict,
        current: dict,
    )-> dict:
        changes = {}

        keys = set(previous) | set(current)

        for key in keys:
            previous_value= previous.get(key)
            current_value = current.get(key)

            if previous_value != current_value:
                changes[key] ={
                    "previous": previous_value,
                    "current": current_value,
                }
        return changes
        
    @staticmethod
    def assemble_scene_state(scene):
        return {
            "scene": scene,
            "scene_state": scene.state,
            "character_states":scene.character_states,
            "prop_states":scene.prop_states,
        }

    @staticmethod
    async def   get_adjacent_scene_states(db:AsyncSession , project_id:int ,scene_number:int,):
        previous_scene = await SceneService.get_previous_scene(db , project_id , scene_number,)
        current_scene = await SceneService.get_scene_by_number(db,project_id,scene_number,)

        if previous_scene is not None:
            previous_scene = await SceneService.get_scene_with_relationships(db,previous_scene.id,)

        if current_scene is not None:
            current_scene =await SceneService.get_scene_with_relationships(db,current_scene.id,)

        return {"previous": previous_scene ,
                "current":current_scene,}

    @staticmethod
    async def match_entities(previous_states:list,current_states:list, entity_id_field:str,):
        previous_map ={getattr(state, entity_id_field): state
                       for state in previous_states
                       }

        current_map ={
            getattr(state , entity_id_field):state
            for state in current_states
        }
        previous_ids = set(previous_map)
        current_ids = set(current_map)

        matched_ids = previous_ids & current_ids
        added_ids = current_ids - previous_ids
        removed_ids = previous_ids - current_ids


        return {
            "matched":[
                (previous_map[entity_id], current_map[entity_id])
                for entity_id in matched_ids
            ],
            "added":[
                current_map[entity_id]
                for entity_id in added_ids
            ],
            "removed":[
                previous_map[entity_id]
                for entity_id in removed_ids
            ],
        }


    @staticmethod
    def compare_states(previous_states, current_state):
        changes = {}
        for field in previous_states.__table__.columns.keys():
            column = previous_states.__table__.columns[field]

            #ignore idetity and metadata fields
            if column.primary_key:
                continue
            if column.foreign_keys:
                continue
            if field in {"created_at", "updated_at"}:
                continue

            previous_value = getattr(previous_states,field)
            current_value =getattr(current_state , field)

            if previous_value != current_value:
                changes[field]={
                    "previous":previous_value,
                    "current":current_value,
                }
        return changes
    
    @staticmethod
    def compare_entity_states(
        matched_entities: list[tuple],
    ):
        changes =[]
        for previous_state, current_state in matched_entities:
            state_changes = FilmStateEngine.compare_states(previous_state , current_state,)
            if state_changes:
                changes.append(
                    {
                        "entity_id": previous_state.character_id
                        if hasattr(previous_state,"character_id")
                        else previous_state.prop_id,
                        "changes": state_changes,
                    }
                )
        return changes

    @staticmethod
    def compare_film_states(
        previous_scene,
        current_scene,
    ):
        character_matches = FilmStateEngine.match_entities(
            previous_scene.character_states or [],
            current_scene.character_states,
            "character_id"
        )
        prop_matches = FilmStateEngine.match_entities(
            previous_scene.prop_states,
            current_scene.prop_states,
            "prop_id",

        )
        character_changes = FilmStateEngine.compare_entity_states(
            character_matches["matched"]
        )

        prop_changes = FilmStateEngine.compare_entity_states(
            prop_matches["matched"]

        )
        return {
            "characters" :{
            "changed": character_changes,
            "added": character_matches["added"],
            "removed": character_matches["removed"],
            },
            "props": {
                "changed": prop_changes,
                "added": prop_matches["added"],
                "removed": prop_matches["removed"],
            },

        }
    @staticmethod
    def calculate_state_transition(comparison):
        return {
            "characters": {
            "changed": comparison["characters"]["changed"],
            "added": comparison["characters"]["added"],
            "removed": comparison["characters"]["removed"],
        },
        "props": {
            "changed": comparison["props"]["changed"],
            "added": comparison["props"]["added"],
            "removed": comparison["props"]["removed"],
        },
        }


    @staticmethod
    async def get_continuity_context(db:AsyncSession , projec_id:int , scene_number:int,):
        scenes = await FilmStateEngine.get_adjacent_scene_states(db,projec_id, scene_number,)
        previous_scene = scenes["previous"]
        current_scene = scenes["current"]

        if current_scene is None:
            return None

        previous_state = (FilmStateEngine.assemble_scene_state(previous_scene)
                          if previous_scene is not None
                          else None)

        current_state = FilmStateEngine.assemble_scene_state(current_scene)
        comparison = None
        transition = None

        if previous_scene is not None:
            comparison = FilmStateEngine.compare_film_states(
                        previous_scene,
                        current_scene,
                    )
        

            transition = FilmStateEngine.calculate_state_transition(comparison)


        return {"previous_state": previous_state,
                "current_state": current_state,
                "transition": transition,
                

        }