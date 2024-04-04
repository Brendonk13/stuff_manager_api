from stuff_manager.models import Action
from stuff_manager.utils.get_tags_contexts_per_action import tags_for_action, contexts_for_action

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


# def extract_action_data(action):
#     return {
#         "id": action.id,
#         "user_id": action.user_id,
#         "title": action.title,
#         "description": action.description,
#         "energy": action.energy,
#         **get_project_data(action),
#         "date": action.date,
#         "created": action.created,
#         "completed_date": action.completed_date,
#         "completed": bool(action.completed_date),
#         "unprocessed_id": action.unprocessed_id,
#         "completion_notes": action.completion_notes if hasattr(action, "completion_notes") else None,
#         "tags": [
#             {"value": tag.tag.value, "id": tag.tag.id}
#             for tag
#             in action.actions_tags_set.all()
#         ],
#         "required_context": [
#             {"value": tag.tag.value, "id": tag.tag.id}
#             for tag
#             in action.actions_requiredcontexts_set.all()
#         ],
#     }


async def extract_action_data(action):
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
        "deleted_date": action.deleted_date,
        "completed": bool(action.completed_date),
        "unprocessed_id": action.unprocessed_id,
        "completion_notes": action.completion_notes if hasattr(action, "completion_notes") else None,
        "tags": await tags_for_action(action.id),
        "required_context": await contexts_for_action(action.id),
    }
