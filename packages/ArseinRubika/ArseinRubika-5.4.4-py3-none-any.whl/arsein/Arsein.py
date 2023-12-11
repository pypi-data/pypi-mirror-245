from arsein.Copyright import copyright
from arsein.PostData import method_Rubika,httpregister,_download,_download_with_server
from arsein.Error import AuthError,TypeMethodError
from arsein.Device import DeviceTelephone
from re import findall
from arsein.Clien import clien
from random import randint,choice
import datetime
from arsein.Encoder import encoderjson
from arsein.TypeText import TypeText
import asyncio


class Messenger:
    def __init__(self,Sh_account: str,keyAccount: str):
        self.Auth = str("".join(findall(r"\w",Sh_account)))
        self.prinet = copyright.CopyRight
        self.methods = method_Rubika(Sh_account,keyAccount)

        if self.Auth.__len__() < 32:
            raise AuthError("The Auth entered is incorrect")
        elif self.Auth.__len__() > 32:
            raise AuthError("The Auth entered is incorrect")

    def __repr__(self):
        return F"Auth your Account: {self.Auth}"

    def sendMessage(self, guid,text,Type = None,Guid_mention = None,message_id=None):
        if Type == "MentionText":
            if Guid_mention != None:
                return self.methods.methodsRubika("json",methode ="sendMessage",indata = {"object_guid":guid,"rnd":f"{randint(100000,999999999)}","text":text,"metadata":{"meta_data_parts":TypeText("MentionText",text,Guid_mention)},"reply_to_message_id":message_id},wn = clien.android)
        elif Type == "Mono":
            return self.methods.methodsRubika("json",methode ="sendMessage",indata = {"object_guid":guid,"rnd":f"{randint(100000,999999999)}","text":text,"metadata":{"meta_data_parts":TypeText("Mono",text = text)},"reply_to_message_id":message_id},wn = clien.web)
        elif Type == "Bold":
            return self.methods.methodsRubika("json",methode ="sendMessage",indata = {"object_guid":guid,"rnd":f"{randint(100000,999999999)}","text":text,"metadata":{"meta_data_parts":TypeText("Bold",text = text)},"reply_to_message_id":message_id},wn = clien.web)
        elif Type == "Italic":
            return self.methods.methodsRubika("json",methode ="sendMessage",indata = {"object_guid":guid,"rnd":f"{randint(100000,999999999)}","text":text,"metadata":{"meta_data_parts":TypeText("Italic",text = text)},"reply_to_message_id":message_id},wn = clien.web)
        elif Type == None:
            return self.methods.methodsRubika("json",methode ="sendMessage",indata = {"object_guid":guid,"rnd":f"{randint(100000,999999999)}","text":text,"reply_to_message_id":message_id},wn = clien.web)

    def editMessage(self, guid, new, message_id):
        return self.methods.methodsRubika("json",methode ="editMessage",indata = {"message_id":message_id,"object_guid":guid,"text":new},wn = clien.web)

    def deleteMessages(self, guid, message_ids):
        return self.methods.methodsRubika("json",methode ="deleteMessages",indata = {"object_guid":guid,"message_ids":message_ids,"type":"Global"},wn = clien.android)

    def getMessagefilter(self, guid, filter_whith):
        return self.methods.methodsRubika("json",methode ="getMessages",indata = {"filter_type":filter_whith,"max_id":"NaN","object_guid":guid,"sort":"FromMax"},wn = clien.web).get("data").get("messages")

    def getMessages(self, guid, min_id):
        return self.methods.methodsRubika("json",methode ="getMessagesInterval",indata = {"object_guid":guid,"middle_message_id":min_id},wn = clien.web).get("data").get("messages")

    def getMessagesbySort(self, guid, message_id,Type):
        if Type == 'max':
            return self.methods.methodsRubika("json",methode ="getMessagesInterval",indata = {"object_guid":guid,"sort":"FromMax","max_id":message_id},wn = clien.web)
        elif Type == 'min':
            return self.methods.methodsRubika("json",methode ="getMessagesInterval",indata = {"object_guid":guid,"sort":"FromMin","min_id":message_id},wn = clien.web)

    def searchMessages(self,guid, text,Type):
        return self.methods.methodsRubika("json",methode ="searchChatMessages",indata = {"search_text":text,"type":Type,"object_guid":guid},wn = clien.web) #Hashtag #Text.....

    def getChats(self, start_id=None):
        return self.methods.methodsRubika("json",methode ="getChats",indata = {"start_id":start_id},wn = clien.web).get("data").get("chats")

    def getMapView(self, latitude,longitude):
        return self.methods.methodsRubika("json",methode ="getMapView",indata = {"location":{"latitude":latitude,"longitude":longitude}},wn = clien.web)

    def sendMap(self, guid,latitude,longitude):
        return self.methods.methodsRubika("json",methode ="sendMessage",indata = {"object_guid":guid,"rnd":randint(100000,999999999),"location":{"latitude":latitude,"longitude":longitude}},wn = clien.web)

    def getMessagesUpdates(self,guid): 
        state = str(round(datetime.datetime.today().timestamp()) - 200)
        return self.methods.methodsRubika("json",methode ="getMessagesUpdates",indata = {"object_guid":guid,"state":state},wn = clien.web)

    @property
    def getChatsUpdate(self):
        state = str(round(datetime.datetime.today().timestamp()) - 200)
        return self.methods.methodsRubika("json",methode ="getChatsUpdates",indata = {"state":state},wn = clien.web).get("data").get("chats")

    def deleteUserChat(self, user_guid, last_message):
        return self.methods.methodsRubika("json",methode ="deleteUserChat",indata = {"last_deleted_message_id":last_message,"user_guid":user_guid},wn = clien.web)

    def sendChatActivity(self, user_guid):
        return self.methods.methodsRubika("json",methode ="sendChatActivity",indata = {"object_guid":user_guid,"activity":'Typing'},wn = clien.web)

    def getInfoByUsername(self, username):
        return self.methods.methodsRubika("json",methode ="getObjectByUsername",indata = {"username":username},wn = clien.web)

    def banGroupMember(self, guid_gap, user_id):
        return self.methods.methodsRubika("json",methode ="banGroupMember",indata = {"group_guid": guid_gap,"member_guid": user_id,"action":"Set"},wn = clien.android)

    def unbanGroupMember(self, guid_gap, user_id):
        return self.methods.methodsRubika("json",methode ="banGroupMember",indata = {"group_guid": guid_gap,"member_guid": user_id,"action":"Unset"},wn = clien.android)

    def banChannelMember(self, guid_channel, user_id):
        return self.methods.methodsRubika("json",methode ="banChannelMember",indata = {"channel_guid": guid_channel,"member_guid": user_id,"action":"Set"},wn = clien.android)

    def unbanChannelMember(self, guid_channel, user_id):
        return self.methods.methodsRubika("json",methode ="banChannelMember",indata = {"channel_guid": guid_channel,"member_guid": user_id,"action":"Unset"},wn = clien.android)

    def getbanGroupUsers(self, guid_group, start_id = None):
        return self.methods.methodsRubika("json",methode ="getBannedGroupMembers",indata = {"group_guid": guid_group,"start_id":start_id},wn = clien.android)

    def getbanChannelUsers(self, guid_channel, start_id = None):
        return self.methods.methodsRubika("json",methode ="getBannedChannelMembers",indata = {"channel_guid": guid_channel,"start_id":start_id},wn = clien.android)

    def getGroupInfo(self, guid_gap):
        return self.methods.methodsRubika("json",methode ="getGroupInfo",indata = {"group_guid": guid_gap},wn = clien.web)

    def getChannelInfo(self, guid_channel):
        return self.methods.methodsRubika("json",methode ="getChannelInfo",indata = {"channel_guid": guid_channel},wn = clien.web)

    def addMemberGroup(self, guid_gap, user_ids):
        return self.methods.methodsRubika("json",methode ="addGroupMembers",indata = {"group_guid": guid_gap,"member_guids": user_ids},wn = clien.web)

    def addMemberChannel(self, guid_channel, user_ids):
        return self.methods.methodsRubika("json",methode ="addChannelMembers",indata = {"channel_guid": guid_channel,"member_guids": user_ids},wn = clien.web)

    def getGroupAdmins(self, guid_gap):
        return self.methods.methodsRubika("json",methode ="getGroupAdminMembers",indata = {"group_guid":guid_gap},wn = clien.web)

    def getChannelAdmins(self, guid_channel):
        return self.methods.methodsRubika("json",methode ="getChannelAdminMembers",indata = {"channel_guid":guid_channel},wn = clien.web)

    def AddNumberPhone(self, first_num, last_num, numberPhone):
        return self.methods.methodsRubika("json",methode ="addAddressBook",indata = {"phone":numberPhone,"first_name":first_num,"last_name":last_num},wn = clien.web)

    def getMessagesInfo(self, guid, message_ids):
        return self.methods.methodsRubika("json",methode ="getMessagesByID",indata = {"object_guid":guid,"message_ids": message_ids},wn = clien.web)

    def getGroupMembers(self, guid_gap, start_id=None):
        return self.methods.methodsRubika("json",methode ="getGroupAllMembers",indata = {"group_guid": guid_gap,"start_id": start_id},wn = clien.web)

    def SearchMemberToBlacklist(self, guid_gap, text):
        return self.methods.methodsRubika("json",methode ="getGroupAllMembers",indata = {"group_guid":guid_gap,"search_text":text},wn = clien.web)

    def getChannelMembers(self, channel_guid, text=None, start_id=None):
        return self.methods.methodsRubika("json",methode ="getChannelAllMembers",indata = {"channel_guid":channel_guid,"search_text":text,"start_id":start_id},wn = clien.android)

    def lockGroup(self, guid_gap):
        return self.methods.methodsRubika("json",methode ="setGroupDefaultAccess",indata = {"access_list": ["AddMember"],"group_guid": guid_gap},wn = clien.android)

    def unlockGroup(self, guid_gap):
        return self.methods.methodsRubika("json",methode ="setGroupDefaultAccess",indata = {"access_list": ["SendMessages", "AddMember"],"group_guid": guid_gap},wn = clien.android)

    def getGroupLink(self, guid_gap):
        return self.methods.methodsRubika("json",methode ="getGroupLink",indata = {"group_guid": guid_gap},wn = clien.web).get("data").get("join_link")

    def getChannelLink(self, guid_channel):
        return self.methods.methodsRubika("json",methode ="getChannelLink",indata = {"channel_guid": guid_channel},wn = clien.web).get("data").get("join_link")

    def changeGroupLink(self, guid_gap):
        return self.methods.methodsRubika("json",methode ="setGroupLink",indata = {"group_guid": guid_gap},wn = clien.web).get("data").get("join_link")

    def changeChannelLink(self, guid_channel):
        return self.methods.methodsRubika("json",methode ="setChannelLink",indata = {"channel_guid": guid_channel},wn = clien.web).get("data").get("join_link")

    def setGroupTimer(self, guid_gap, time):
        return self.methods.methodsRubika("json",methode ="editGroupInfo",indata = {"group_guid": guid_gap,"slow_mode": time,"updated_parameters":["slow_mode"]},wn = clien.android)

    def setGroupAdmin(self, guid_gap, guid_member,access_admin = None):
        if access_admin == None: access_admin = ["ChangeInfo","SetJoinLink","SetAdmin","BanMember","DeleteGlobalAllMessages","PinMessages","SetMemberAccess"] if access_admin == None else access_admin
        return self.methods.methodsRubika("json",methode ="setGroupAdmin",indata = {"group_guid": guid_gap,"access_list":access_admin,"action": "SetAdmin","member_guid": guid_member},wn = clien.android)

    def deleteGroupAdmin(self,guid_gap,guid_admin):
        return self.methods.methodsRubika("json",methode ="setGroupAdmin",indata = {"group_guid": guid_gap,"action": "UnsetAdmin","member_guid": guid_admin},wn = clien.android)

    def deleteGroup(self,guid_gap):
        return self.methods.methodsRubika("json",methode ="removeGroup",indata = {"group_guid": guid_gap},wn = clien.web)

    def setChannelAdmin(self, guid_channel, guid_member,access_admin = None):
        if access_admin == None: access_admin = ["SetAdmin","SetJoinLink","AddMember","DeleteGlobalAllMessages","EditAllMessages","SendMessages","PinMessages","ViewAdmins","ViewMembers","ChangeInfo"] if access_admin == None else access_admin
        return self.methods.methodsRubika("json",methode ="setChannelAdmin",indata = {"channel_guid": guid_channel,"access_list":access_admin,"action": "SetAdmin","member_guid": guid_member},wn = clien.android)

    def deleteChannelAdmin(self,guid_channel,guid_admin):
        return self.methods.methodsRubika("json",methode ="setChannelAdmin",indata = {"channel_guid": guid_channel,"action": "UnsetAdmin","member_guid": guid_admin},wn = clien.android)

    def getStickersByEmoji(self,emojee):
        return self.methods.methodsRubika("json",methode ="getStickersByEmoji",indata = {"emoji_character": emojee,"suggest_by": "All"},wn = clien.web).get("data").get("stickers")

    def searchStickerSets(self,text,start_id = None):
        return self.methods.methodsRubika("json",methode ="searchStickerSets",indata = {"search_text": text,"start_id": start_id},wn = clien.web)

    def getTrendStickerSets(self,start_id = None):
        return self.methods.methodsRubika("json",methode ="getTrendStickerSets",indata = {"start_id": start_id},wn = clien.web)

    def getStickerSetByID(self,sticker_set_id = None):
        return self.methods.methodsRubika("json",methode ="getStickerSetByID",indata = {"sticker_set_id": sticker_set_id},wn = clien.web)

    def actionStickerSet(self,action,sticker_set_id = None):
        return self.methods.methodsRubika("json",methode ="actionOnStickerSet",indata = {"sticker_set_id": sticker_set_id,"action":action},wn = clien.web)

    def activenotification(self,guid):
        return self.methods.methodsRubika("json",methode ="setActionChat",indata = {"action": "Unmute","object_guid": guid},wn = clien.web)

    def offnotification(self,guid):
        return self.methods.methodsRubika("json",methode ="setActionChat",indata = {"action": "Mute","object_guid": guid},wn = clien.web)

    def sendPoll(self,guid,question,options:list):
        return self.methods.methodsRubika("json",methode ="createPoll",indata = {"object_guid":guid,"options":options,"rnd":f"{randint(100000,999999999)}","question":question,"type":"Regular","is_anonymous":false,"allows_multiple_answers":true},wn = clien.web)

    def sendPollExam(self,guid,question,options:list,explanation):
        return self.methods.methodsRubika("json",methode ="createPoll",indata = {"object_guid":guid,"options":options,"rnd":f"{randint(100000,999999999)}","question":question,"type":"Quiz","is_anonymous":false,"allows_multiple_answers":false,"explanation":explanation,"correct_option_index":1},wn = clien.web)

    def getPollStatus(self,poll_id):
        return self.methods.methodsRubika("json",methode ="getPollStatus",indata = {"poll_id":poll_id},wn = clien.web)

    def getVoters(self,poll_id):
        return self.methods.methodsRubika("json",methode ="getPollOptionVoters",indata = {"poll_id":poll_id,"selection_index":1},wn = clien.web)

    def votePoll(self,poll_id):
        return self.methods.methodsRubika("json",methode ="votePoll",indata = {"poll_id":poll_id,"selection_index":1},wn = clien.web)

    def forwardMessages(self, From, message_ids, to):
        return self.methods.methodsRubika("json",methode ="forwardMessages",indata = {"from_object_guid": From,"message_ids": message_ids,"rnd": f"{randint(100000,999999999)}","to_object_guid": to},wn = clien.web)

    def VisitChatGroup(self,guid_gap,visiblemsg):
        return self.methods.methodsRubika("json",methode ="editGroupInfo",indata = {"chat_history_for_new_members": "Visible","group_guid": guid_gap,"updated_parameters": visiblemsg},wn = clien.web)

    def HideChatGroup(self,guid,hiddenmsg):
        return self.methods.methodsRubika("json",methode ="editGroupInfo",indata = {"chat_history_for_new_members": "Hidden","group_guid": guid_gap,"updated_parameters": hiddenmsg},wn = clien.web)

    def pin(self, guid, message_id):
        return self.methods.methodsRubika("json",methode ="setPinMessage",indata = {"action":"Pin","message_id": message_id,"object_guid": guid},wn = clien.web)

    def unpin(self,guid,message_id):
        return self.methods.methodsRubika("json",methode ="setPinMessage",indata = {"action":"Unpin","message_id": message_id,"object_guid": guid},wn = clien.web)

    @property
    def logout(self):
        return self.methods.methodsRubika("json",methode ="logout",indata = {},wn = clien.web)

    def joinGroup(self,link):
        hashLink = link.split("/")[-1]
        return self.methods.methodsRubika("json",methode ="joinGroup",indata = {"hash_link": hashLink},wn = clien.web)

    def joinChannelAll(self,guid):
        if ("https://" or "http://") in guid:
            link = guid.split("/")[-1]
            return self.methods.methodsRubika("json",methode ="joinChannelByLink",indata = {"hash_link": link},wn = clien.android)
        elif "@" in guid:
            IDE = ide.split("@")[-1]
            guid = self.getInfoByUsername(IDE)["data"]["channel"]["channel_guid"] 
            return self.methods.methodsRubika("json",methode ="joinChannelAction",indata = {"action": "Join","channel_guid": guid},wn = clien.web)
        else:
            guid = guid
            return self.methods.methodsRubika("json",methode ="joinChannelAction",indata = {"action": "Join","channel_guid": guid},wn = clien.web)

    def joinChannelByLink(self,link):
        hashLink = link.split("/")[-1]
        return self.methods.methodsRubika("json",methode ="joinChannelByLink",indata = {"hash_link": hashLink},wn = clien.android)

    def joinChannelByID(self,ide):
        IDE = ide.split("@")[-1]
        GUID = self.getInfoByUsername(IDE)["data"]["channel"]["channel_guid"]
        return self.methods.methodsRubika("json",methode ="joinChannelAction",indata = {"action": "Join","channel_guid": GUID},wn = clien.web)

    def joinChannelByGuid(self,guid):
        return self.methods.methodsRubika("json",methode ="joinChannelAction",indata = {"action": "Join","channel_guid": guid},wn = clien.web)

    def leaveGroup(self,guid_gap):
        if "https://" in guid_gap:
            guid_gap = self.joinGroup(guid_gap)["data"]["group"]["group_guid"]
        else:
            guid_gap = guid_gap
        return self.methods.methodsRubika("json",methode ="leaveGroup",indata = {"group_guid": guid_gap},wn = clien.web)

    def leaveChannel(self,guid_channel):
        if "https://" in guid_channel:
            guid_channel = self.joinChannelByLink(guid_channel)["data"]["chat_update"]["object_guid"]
        elif "@" in guid_channel:
            guid_channel = self.joinChannelByID(guid_channel)["data"]["chat_update"]["object_guid"]
        else:
            guid_channel = guid_channel
        return self.methods.methodsRubika("json",methode ="joinChannelAction",indata = {"action": "Leave","channel_guid": guid_channel},wn = clien.web)

    def EditNameGroup(self,groupgu,namegp,biogp=None):
        return self.methods.methodsRubika("json",methode ="editGroupInfo",indata = {"description": biogp,"group_guid": groupgu,"title":namegp,"updated_parameters":["title","description"]},wn = clien.web)

    def EditBioGroup(self,groupgu,biogp,namegp=None):
        return self.methods.methodsRubika("json",methode ="editGroupInfo",indata = {"description": biogp,"group_guid": groupgu,"title":namegp,"updated_parameters":["title","description"]},wn = clien.web)

    def block(self, guid_user):
        return self.methods.methodsRubika("json",methode ="setBlockUser",indata = {"action": "Block","user_guid": guid_user},wn = clien.web)

    def unblock(self, guid_user):
        return self.methods.methodsRubika("json",methode ="setBlockUser",indata = {"action": "Unblock","user_guid": guid_user},wn = clien.web)

    def startVoiceChat(self, guid):
        return self.methods.methodsRubika("json",methode ="createGroupVoiceChat",indata = {"chat_guid":guid},wn = clien.web)

    def addUserContact(self, guid):
        return self.methods.methodsRubika("json",methode ="setAskSpamAction",indata = {"object_guid":guid,"action":"AddToContact"},wn = clien.web)

    def getGroupVoiceChat(self, guid_gap):
        voice_chat_id = self.getGroupInfo(guid_gap)["data"]["chat"]["group_voice_chat_id"]
        return self.methods.methodsRubika("json",methode ="getGroupVoiceChat",indata = {"voice_chat_id":voice_chat_id,"chat_guid":guid_gap},wn = clien.web)

    def getGroupVoiceChatParticipants(self, guid_gap,start_id = None):
        voice_chat_id = self.getGroupInfo(guid_gap)["data"]["chat"]["group_voice_chat_id"]
        return self.methods.methodsRubika("json",methode ="getGroupVoiceChatParticipants",indata = {"chat_guid":guid_gap,"voice_chat_id":voice_chat_id,"start_id":start_id},wn = clien.web)

    def editVoiceChat(self,guid,voice_chat_id,bol):
        return self.methods.methodsRubika("json",methode ="setGroupVoiceChatSetting",indata = {"chat_guid":guid,"voice_chat_id":voice_chat_id,"join_muted":bol,"updated_parameters":["join_muted"]},wn = clien.web)

    def changeTitleVoiceChat(self,guid,title,voice_chat_id):
        return self.methods.methodsRubika("json",methode ="setGroupVoiceChatSetting",indata = {"chat_guid":guid,"voice_chat_id":voice_chat_id,"title":title,"updated_parameters":["title"]},wn = clien.web)

    def finishVoiceChat(self, guid):
        voice_chat_id = self.getGroupInfo(guid)["data"]["chat"]["group_voice_chat_id"]
        return self.methods.methodsRubika("json",methode ="discardGroupVoiceChat",indata = {"chat_guid":guid,"voice_chat_id" : voice_chat_id},wn = clien.web)

    def leaveGroupVoiceChat(self, guid):
        voice_chat_id = self.getGroupInfo(guid)["data"]["chat"]["group_voice_chat_id"]
        return self.methods.methodsRubika("json",methode ="leaveGroupVoiceChat",indata = {"chat_guid":guid,"voice_chat_id" : voice_chat_id},wn = clien.web)

    def getDisplayAsInGroupVoiceChat(self,guid_gap,start_id = None):
        return self.methods.methodsRubika("json",methode ="getDisplayAsInGroupVoiceChat",indata = {"chat_guid":guid_gap,"start_id":start_id},wn = clien.web)

    def sendGroupVoiceChatActivity(self,guid_gap,model):
        return self.methods.methodsRubika("json",methode ="sendGroupVoiceChatActivity",indata = {"try_count":guid_gap,"model" : model},wn = clien.web)

    def getUserInfo(self, guid_user):
        return self.methods.methodsRubika("json",methode ="getUserInfo",indata = {"user_guid":guid_user},wn = clien.web)

    def getUserInfoByIDE(self, IDE_user):
        guiduser = self.getInfoByUsername(IDE_user.replace("@",""))["data"]["user"]["user_guid"]
        return self.methods.methodsRubika("json",methode ="getUserInfo",indata = {"user_guid":guiduser},wn = clien.web)

    def seeGroupbyLink(self,link_gap):
        link = link_gap.split("https://rubika.ir/joing/")[-1]
        return self.methods.methodsRubika("json",methode ="groupPreviewByJoinLink",indata = {"hash_link": link},wn = clien.web).get("data")

    def seeChannelbyLink(self,link_channel):
        link = link_channel.split("https://rubika.ir/joinc/")[-1]
        return self.methods.methodsRubika("json",methode ="channelPreviewByJoinLink",indata = {"hash_link": link},wn = clien.web).get("data")

    def __getImageSize(self,image_bytes:bytes):
        bytimg = PIL.Image.open(io.BytesIO(image_bytes))
        width, height = bytimg.size
        return [width , height]

    def getAvatars(self,guid):
        return self.methods.methodsRubika("json",methode ="getAvatars",indata = {"object_guid":guid},wn = clien.web)

    def uploadAvatar_replay(self,guid,files_ide):
        return self.methods.methodsRubika("json",methode ="uploadAvatar",indata = {"object_guid":guid,"thumbnail_file_id":files_ide,"main_file_id":files_ide},wn = clien.web)

    def uploadAvatar(self,guid,main,thumbnail=None):
        mainID = str(self.Upload.uploadFile(main)[0]["id"])
        thumbnailID = str(self.Upload.uploadFile(thumbnail or main)[0]["id"])
        return self.methods.methodsRubika("json",methode ="uploadAvatar",indata = {"object_guid":guid,"thumbnail_file_id":thumbnailID,"main_file_id":mainID},wn = clien.web)

    def removeAvatar(self,guid):
        avatar_id = self.getAvatars(guid)['data']['avatars'][0]['avatar_id']
        return self.methods.methodsRubika("json",methode ="deleteAvatar",indata = {"object_guid":guid,"avatar_id":avatar_id},wn = clien.web)

    def removeAllAvatars(self,guid):
        while 1:
            try:
                avatar = self.getAvatars(guid)['data']['avatars']
                if avatar != []:
                    avatar_id = self.getAvatars(guid)['data']['avatars'][0]['avatar_id']
                    self.methods.methodsRubika("json",methode ="deleteAvatar",indata = {"object_guid":guid,"avatar_id":avatar_id},wn = clien.web)
                else:
                    return 'Ok remove Avatars'
                    break
            except:
                continue

    @property
    def Devicesrubika(self):
        return self.methods.methodsRubika("json",methode ="getMySessions",indata = {},wn = clien.web)

    def deleteChatHistory(self,guid,last_message_id):
        return self.methods.methodsRubika("json",methode ="deleteChatHistory",indata = {"last_message_id": last_message_id,"object_guid": guid},wn = clien.web)

    def addFolder(self, Name = "Arsein", include_chat = None,include_object = None ,exclude_chat = None,exclude_object = None):
        return self.methods.methodsRubika("json",methode ="addFolder",indata = {"exclude_chat_types": exclude_chat,"exclude_object_guids": exclude_object,"include_chat_types": include_chat,"include_object_guids": include_object,"is_add_to_top":True,"name": Name},wn = clien.web)

    def deleteFolder(self,folder_id):
        return self.methods.methodsRubika("json",methode ="deleteFolder",indata = {"folder_id": folder_id},wn = clien.web)

    def addGroup(self,title,guidsUser:list):
        return self.methods.methodsRubika("json",methode ="addGroup",indata = {"title":title,"member_guids":guidsUser},wn = clien.web)

    def deleteGroup(self,guid_group):
        return self.methods.methodsRubika("json",methode ="deleteNoAccessGroupChat",indata = {"group_guid": guid_group},wn = clien.web)

    def addChannel(self,Type,title,typeChannell,bio,guidsUser:list):
        return self.methods.methodsRubika("json",methode ="addChannel",indata = {"title":title,"description":bio,"channel_type":Type,"member_guids":guidsUser},wn = clien.web)

    def breturn(self,start_id = None):
        return self.methods.methodsRubika("json",methode ="getBreturnUsers",indata = {"start_id": start_id},wn = clien.web)

    def editUser(self,first_name = None,last_name = None,bio = None):
        return self.methods.methodsRubika("json",methode ="updateProfile",indata = {"bio": bio,"first_name": first_name,"last_name": last_name,"updated_parameters":["first_name","last_name","bio"]},wn = clien.web)

    def editusername(self,username):
        ide = username.split("@")[-1]
        return self.methods.methodsRubika("json",methode ="updateUsername",indata = {"username": ide},wn = clien.web)

    def Postion(self,guid,guiduser):
        return self.methods.methodsRubika("json",methode ="requestChangeObjectOwner",indata = {"object_guid": guid,"new_owner_user_guid": guiduser},wn = clien.android)

    def getPostion(self,guid):
        return self.methods.methodsRubika("json",methode ="getPendingObjectOwner",indata = {"object_guid": guid},wn = clien.android)

    def sendLive(self,guid,titlelive):
        return self.methods.methodsRubika("json",methode ="sendLive",indata = {"object_guid":guid,"title":titlelive,"device_type":"Software","thumb_inline":"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","rnd":randint(100000,999999)},wn = clien.web)

    @property
    def ClearAccounts(self):
        return self.methods.methodsRubika("json",methode ="terminateOtherSessions",indata = {},wn = clien.web)

    def HidePhone(self,**kwargs):
        return self.methods.methodsRubika("json",methode ="setSetting",indata = {"settings": kwargs,"update_parameters":["show_my_phone_number"]},wn = clien.web)

    def HideOnline(self,**kwargs):
        return self.methods.methodsRubika("json",methode ="setSetting",indata = {"settings": kwargs,"update_parameters":["show_my_last_online"]},wn = clien.web)

    def search_inaccount(self,text):
        return self.methods.methodsRubika("json",methode ="searchGlobalMessages",indata = {"search_text": text,"start_id":None,"type": "Text"},wn = clien.web).get("data").get("messages")

    def search_inrubika(self,text):
        return self.methods.methodsRubika("json",methode ="searchGlobalObjects",indata = {"search_text": text},wn = clien.web).get("data").get('objects')

    def getAbsObjects(self,guid):
        return self.methods.methodsRubika("json",methode ="getAbsObjects",indata = {"objects_guids": guid},wn = clien.web)

    def Infolinkpost(self,linkpost):
        return self.methods.methodsRubika("json",methode ="getLinkFromAppUrl",indata = {"app_url": linkpost},wn = clien.web)

    def addToMyGifSet(self,guid,message_id):
        return self.methods.methodsRubika("json",methode ="addToMyGifSet",indata = {"message_id":message_id,"object_guid":guid},wn = clien.web)

    def getContactsLastOnline(self,user_guids:list):
        return self.methods.methodsRubika("json",methode ="getContactsLastOnline",indata = {"user_guids": user_guids},wn = clien.web)

    def SignMessageChannel(self,guid_channel,sign:bool):
        return self.methods.methodsRubika("json",methode ="editChannelInfo",indata = { "channel_guid": guid_channel,"sign_messages": sign,"updated_parameters": ["sign_messages"]},wn = clien.web)

    @property
    def ActiveContectJoin(self):
        return self.methods.methodsRubika("json",methode ="setSetting",indata = {"settings":{"can_join_chat_by":"MyContacts"},"update_parameters":["can_join_chat_by"]},wn = clien.web)

    @property
    def ActiveEverybodyJoin(self):
        return self.methods.methodsRubika("json",methode ="setSetting",indata = {"settings":{"can_join_chat_by":"Everybody"},"update_parameters":["can_join_chat_by"]},wn = clien.web)

    def CalledBy(self,typeCall:str):
        return self.methods.methodsRubika("json",methode ="setSetting",indata = {"settings": {"can_called_by": typeCall}, "update_parameters": ["can_called_by"]},wn = clien.android)

    def changeChannelID(self,guid_channel,username):
        return self.methods.methodsRubika("json",methode ="updateChannelUsername",indata = {"channel_guid": guid_channel,"username": username},wn = clien.web)

    def getMessageShareUrl(self,guid,messageId):
        return self.methods.methodsRubika("json",methode ="getMessageShareUrl",indata = {"object_guid": guid,"messageId": messageId},wn = clien.web)

    @property
    def getBlockedUsers(self):
        return self.methods.methodsRubika("json",methode ="getBlockedUsers",indata = {},wn = clien.web)

    def deleteContact(self,guid_user):
        return self.methods.methodsRubika("json",methode ="deleteContact",indata = {"user_guid":guid_user},wn = clien.web)

    def checkUserUsername(self,username):
        return self.methods.methodsRubika("json",methode ="checkUserUsername",indata = {"username":username},wn = clien.web)

    def checkChannelUsername(self,username):
        return self.methods.methodsRubika("json",methode ="checkChannelUsername",indata = {"username":username},wn = clien.web)

    @property
    def getContacts(self):
        return self.methods.methodsRubika("json",methode ="getContacts",indata = {},wn = clien.web).get("data").get("users")

    def getLiveStatus(self,live_id,token_live):
        return self.methods.methodsRubika("json",methode ="getLiveStatus",indata = {"live_id":live_id,"access_token":token_live},wn = clien.web)

    @property
    def getdatabaseReaction(self):
        return self.methods.methodsRubika("json",methode ="getAvailableReactions",indata = {},wn = clien.web)

    def Reaction(self,guid,typeReaction,reaction,message_id):
        if typeReaction == "add":
            return self.methods.methodsRubika("json",methode ="actionOnMessageReaction",indata = {"action":"Add","reaction_id":reaction,"message_id":message_id,"object_guid":guid},wn = clien.web)
        elif typeReaction == "remove":
            return self.methods.methodsRubika("json",methode ="actionOnMessageReaction",indata = {"action":"Remove","reaction_id":reaction,"message_id":message_id,"object_guid":guid},wn = clien.web)

    def commonGroup(self,guid_user):
        IDE = guid_user.split("@")[-1]
        GUID = self.getInfoByUsername(IDE)["data"]["user"]["user_guid"]
        return self.methods.methodsRubika("json",methode ="getCommonGroups",indata = {"user_guid": GUID},wn = clien.android)

    def setTypeChannel(self,guid_channel,type_Channel):
        if type_Channel == "Private":
            return self.methods.methodsRubika("json",methode ="editChannelInfo",indata = {"channel_guid":guid_channel,"channel_type":"Private","updated_parameters":["channel_type"]},wn = clien.web)
        else:
            if type_Channel == "Public":
                return self.methods.methodsRubika("json",methode ="editChannelInfo",indata = {"settings":{"channel_guid":guid_channel,"channel_type":"Public","updated_parameters":["channel_type"]}},wn = clien.web)

    def getChatAds(self,user_guids:list):
        state = str(round(datetime.datetime.today().timestamp()) - 200)
        return self.methods.methodsRubika("json",methode ="getChatAds",indata = {"state": state},wn = clien.web)

    def clickMessageUrl(self,guid,message_id,link):
        return self.methods.methodsRubika("json",methode ="clickMessageUrl",indata = {"object_guid": guid,"message_id": message_id,"link_url": link},wn = clien.web)

    def seenChat(self,guid,message_id):
        return self.methods.methodsRubika("json",methode ="seenChat",indata = {"seen_list":{f"{guid}":f"{message_id}"}},wn = clien.web)

    @property
    def getContactsUpdates(self):
        state = str(round(datetime.datetime.today().timestamp()) - 200)
        return self.methods.methodsRubika("json",methode ="getContactsUpdates",indata = {"state": state},wn = clien.web)

    def sendSticker(self,guid,emoji,w_h_rati,sticker_id,file_id,access_hash,set_id):
        return self.methods.methodsRubika("json",methode ="sendMessage",indata = {"object_guid": guid,"rnd": f"{randint(100000,999999999)}","sticker": {"emoji_character": emoji,"w_h_ratio": w_h_rati,"sticker_id": sticker_id,"file": {"file_id": file_id,"mime": "png","dc_id": 32,"access_hash_rec": access_hash,"file_name": "sticker.png"},"sticker_set_id": set_id}},wn = clien.web)

    def twolocks(self,ramz,hide):
        locked =  self.methods.methodsRubika("json",methode ="setupTwoStepVerification",indata = {"hint": hide,"password": ramz},wn = clien.web)
        if locked["status"] == 'ERROR_GENERIC':
            return locked["client_show_message"]["link"]["alert_data"]["message"]
        else:return locked

    def deletetwolocks(self,password):
        return self.methods.methodsRubika("json",methode ="turnOffTwoStep",indata = {"password": password},wn = clien.web)

    def passwordChange(self,password):
        return self.methods.methodsRubika("json",methode ="resendCodeRecoveryEmail",indata = {"password": password},wn = clien.web)

    def loginforgetPassword(self,emailCode,password,phone_number):
        return self.methods.methodsRubika("json",methode ="loginDisableTwoStep",indata = {"email_code": emailCode,"forget_password_code_hash": password,"phone_number": phone_number},wn = clien.web)

    def ProfileEdit(self,first_name = None,last_name = None,bio = None,username = None):
        while 1:
            try:
                self.editUser(first_name = first_name,last_name = last_name,bio = bio)
                self.editusername(username)
                return "Profile edited"
                break
            except:continue

    def getChatGroup(self,guid_gap):
        while 1:
            try:
                lastmessages = self.getGroupInfo(guid_gap)["data"]["chat"]["last_message_id"]
                messages = self.getMessages(guid_gap, lastmessages)
                return messages
                break
            except:continue

    def getChatChannel(self,guid_channel):
        while 1:
            try:
                lastmessages = self.getChannelInfo(guid_channel)["data"]["chat"]["last_message_id"]
                messages = self.getMessages(guid_channel, lastmessages)
                return messages
                break
            except:continue

    def getChatUser(self,guid_User):
        while 1:
            try:
                lastmessages = self.getUserInfo(guid_User)["data"]["chat"]["last_message_id"]
                messages = self.getMessages(guid_User, lastmessages)
                return messages
                break
            except:continue
    @property
    def Authrandom(self):
        auth = ""
        meghdar = "qwertyuiopasdfghjklzxcvbnm0123456789"
        for string in range(32):
            auth += choice(meghdar)
        return auth

    def SendCodeSMS(self,phonenumber):
        tmp = self.Authrandom()
        enc = encoderjson(tmp)
        return self.methods.methodsRubika("json",methode ="sendCode",indata = {"phone_number":f"98{phonenumber[1:]}","send_type":"SMS"},wn = clien.web)

    def SendCodeWhithPassword(self,phone_number:str,pass_you):
        tmp = self.Authrandom()
        enc = encoderjson(tmp)
        return self.methods.methodsRubika("json",methode ="sendCode",indata = {"pass_key":pass_you,"phone_number":f"98{phonenumber[1:]}","send_type":"SMS"},wn = clien.web)

    def signIn(self,phone_number,phone_code_hash,phone_code):
        tmp = self.Authrandom()
        enc = encoderjson(tmp)
        return self.methods.methodsRubika("json",methode ="signIn",indata = {"phone_number":f"98{phone_number[1:]}","phone_code_hash":phone_code_hash,"phone_code":phone_code},wn = clien.web)

    def registerDevice(self,auth):
        enc = encoderjson(auth)
        while 1:
            try:
                loop = asyncio.get_event_loop()
                ersal = loads(enc.decrypt(loads(loop.run_until_complete(httpregister(auth)))))
                return ersal
                break
            except:
                continue

    def Auth(self,readfile):
        while 1:
            try:
                with open(f"{readfile}", "r") as file:
                    jget = json.load(file)
                    s = jget["data"]["auth"]
                    regs = self.registerDevice(s)
                    return regs
            except:continue

class Robot_Rubika(Messenger):
    ...
