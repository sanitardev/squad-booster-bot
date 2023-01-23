from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

class IsAdminFilter(BoundFilter):
    """
    Filter that checks for admin rights existence
    """
    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin() == self.is_admin

class IsCallAdminFilter(BoundFilter):
    """
    Filter that checks for admin rights existence
    """
    key = "is_call_admin"

    def __init__(self, is_call_admin: bool):
        self.is_call_admin = is_call_admin

    async def check(self, call: types.CallbackQuery):
        member = await call.bot.get_chat_member(call.message.chat.id, call.from_user.id)
        return member.is_chat_admin() == self.is_call_admin


class IsBotRestrictFilter(BoundFilter):
    """
    Filter that checks for admin rights existence
    """
    key = "is_bot_restrict"

    def __init__(self, is_bot_restrict: bool):
        self.is_bot_restrict = is_bot_restrict

    async def check(self, message: types.Message):
        me = await message.bot.get_me()
        member = await message.bot.get_chat_member(message.chat.id, me.id)
        try:
            if member.can_restrict_members and member.can_delete_messages == True:
                admin = True
        except:
            admin = False
        return admin == self.is_bot_restrict


class IsBotAdminFilter(BoundFilter):
    """
    Filter that checks for admin rights existence
    """
    key = "is_bot_admin"

    def __init__(self, is_bot_admin: bool):
        self.is_bot_admin = is_bot_admin

    async def check(self, message: types.Message):
        me = await message.bot.get_me()
        member = await message.bot.get_chat_member(message.chat.id, me.id)
        return member.is_chat_admin() == self.is_bot_admin


class MemberCanRestrictFilter(BoundFilter):
    """
    Filter that checks member ability for restricting
    """
    key = 'member_can_restrict'

    def __init__(self, member_can_restrict: bool):
        self.member_can_restrict = member_can_restrict

    async def check(self, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)

        # I don't know why, but telegram thinks, if member is chat creator, he cant restrict member
        return (member.is_chat_creator() or member.can_restrict_members) == self.member_can_restrict