from stuff_manager.models import Actions_Tags, Actions_RequiredContexts


async def tags_for_action(action_id: int):
    return [
        {"value": tag.tag.value, "id": tag.tag.id}
        async for tag
        in Actions_Tags.objects.filter(action_id=action_id).select_related("tag")
    ]


async def contexts_for_action(action_id: int):
    return [
        {"value": tag.tag.value, "id": tag.tag.id}
        async for tag
        in Actions_RequiredContexts.objects.filter(action_id=action_id).select_related("tag")
    ]
