import vk_api
from vk_api.longpoll import VkLongPoll, VkChatEventType, VkEventType

from vk_tokens import group_token


session = vk_api.VkApi(token=group_token)
longpoll = VkLongPoll(session)


def is_member(group_id, user_id):
    """Возвращает True, если пользователь состоит в сообществе"""
    return bool(session.method("groups.isMember", {"group_id": group_id, "user_id": user_id}))

def is_chat(peer_id):
    """Возвращает True, если диалог является беседой"""
    return peer_id > 2000000000

def delete_message(message_id):
    """Удаляет сообщение с указанным message_id"""
    session.method("messages.delete", {"message_ids": message_id, "delete_for_all": True})


def main():
    group_id = session.method("groups.getById")[0]["id"]
    
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.user_id > 0:
                if is_chat(event.peer_id) and not is_member(group_id, event.user_id):
                    delete_message(event.message_id)


if __name__ == "__main__":
    main()
