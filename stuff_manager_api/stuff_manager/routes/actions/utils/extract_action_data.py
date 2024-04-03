from stuff_manager.models import Action

def get_project_data(action):
    if not action.project_id:
        return { "project": None }

    return {
        "project": {
            "id": action.project_id,
            "name": action.project.name,
            "notes": action.project.notes,
        }
    }


def extract_action_data(action):
    return {
        "id": action.id,
        "user_id": action.user_id,
        "title": action.title,
        "description": action.description,
        "energy": action.energy,
        **get_project_data(action),
        "date": action.date,
        "created": action.created,
        "completed_date": action.completed_date,
        "completed": bool(action.completed_date),
        "unprocessed_id": action.unprocessed_id,
        "completion_notes": action.completion_notes if hasattr(action, "completion_notes") else None,
        "tags": [
            {"value": tag.tag.value, "id": tag.tag.id}
            for tag
            in action.actions_tags_set.all()
        ],
        "required_context": [
            {"value": tag.tag.value, "id": tag.tag.id}
            for tag
            in action.actions_requiredcontexts_set.all()
        ],
    }
