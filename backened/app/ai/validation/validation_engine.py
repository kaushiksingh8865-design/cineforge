


class ValidationEngine:
    @staticmethod

    def validate_result(issues: list,) -> dict:
        return { "valid": len(issues) == 0, "issues": issues,}

    
    def v_state_c( change:dict , rule:callable,): #  validate state change.
        if rule(change):
            return None

        return {
            "type": "state_change",
            "message": "state chnage failed validation.",
            "change": change ,
        }
    def v_character_c( character_change:list, rules: list[callable],):
        issues = []

        for change in character_change:

            for rule in rules:
                issue = ValidationEngine.v_state_c(change , rule,)
                if issue is not None:
                    issues.append(issue)
        return issues

    def v_prop_c ( prop_c:list , rules:list[callable],):
        issues =[]
        for change in prop_c:
            for rule in rules:
                issue = ValidationEngine.v_state_c(change , rule,)
                if issue is not None:
                    issues.append(issue)

        return issues


    def v_scene_t(previous_state,current_state,rules:list[callable],):
        issues =[]
        for rule in rules:
            issue = ValidationEngine.v_state_c({
                "previous": previous_state,
                "current": current_state,
            },
            rule,
            )
            if issue is not None:
                issues.append(issue)

        return issues

    def v_state_t(
            context: dict ,
            character_rules: list[callable]| None = None,
            prop_rules: list[callable] | None = None,
            scene_rules: list[callable]| None = None,
    ):
        character_rules = character_rules or []
        prop_rules = prop_rules or []
        scene_rules = scene_rules or []

        issue = []

        if context is None:
            return ValidationEngine.validate_result([
                {
                    
                    "type": "context",
                    "message":"continuity context is missing.",
                                    
                }
            ]
            )

        previous_state = context["previous_state"]
        current_state = context[ "current_state"]


        if current_state is None:
            return ValidationEngine.validate_result([
                {
                    "type": "context",
                    "message": "current film state is missing.",
                }
            ]
                
            )

        if previous_state is not None:
            character_changes = context["transition"]["characters"]["changed"]
            prop_changes = context["transition"]["props"]["changed"]

            issue.extend(ValidationEngine.v_character_c(
                character_changes,
                character_rules,
            ))

            issue.extend(ValidationEngine.v_prop_c(
                prop_changes,
                prop_rules,

            ))
            issue.extend(ValidationEngine.v_scene_t(
                previous_state,
                current_state,
                scene_rules,
            ))

        return ValidationEngine.build_validate_result(issue)