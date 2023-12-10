"""
api的集合
"""
api_base = "https://bbs-api.miyoushe.com/"
api_static_base = 'https://bbs-api-static.miyoushe.com/'
api_takumi_base = 'https://api-takumi.mihoyo.com/'
api_account_base = 'https://webapi.account.mihoyo.com/'
api_passport_base = 'https://passport-api.mihoyo.com/'

# 本地模式
# api_base = "http://localhost:5000/"
# api_static_base = "http://localhost:5000/"
# api_takumi_base = "http://localhost:5000/"
# api_account_base = "http://localhost:5000/"
# api_passport_base = "http://localhost:5000/"


# Static
static_base = 'https://bbs-static.miyoushe.com/'
defaultAvatar = static_base + "avatar/avatarDefault.png"

# Gets
Cookie_url = api_account_base + "Api/cookie_accountinfo_by_loginticket?login_ticket={0}"
Cookie_url2 = api_takumi_base + "auth/api/getMultiTokenByLoginTicket?login_ticket={0}&token_types=3&uid={1}"
Cookie_url3 = api_takumi_base + 'auth/api/getCookieAccountInfoBySToken?stoken={0}&uid={1}'
mmt = api_account_base + "Api/create_mmt?scene_type=1&now={}"
getPostReplies = api_base + "post/api/getPostReplies?gids={0}&is_hot={1}&post_id={2}&size={3}&last_id={4}&order_type={5}&only_master={6}"
getSubReplies = api_base + "post/api/getSubReplies?post_id={0}&floor_id={1}&last_id={2}&size={3}"
getRootReplyInfo = api_base + 'post/api/getRootReplyInfo?post_id={0}&reply_id={1}'
webHome = api_base + "apihub/wapi/webHome?gids={0}&page={1}&page_size={2}"
getPostFull = api_base + "post/api/getPostFull?post_id={0}"
feedPosts = api_base + "post/api/feeds/posts?gids={0}&last_id=&fresh_action=1&is_first_initialize=true&filter="
emoticon_set = api_base + "misc/api/emoticon_set?gid={0}"
getNewsList = api_base + "post/wapi/getNewsList?gids={0}&type={1}&page_size={2}&last_id={3}"
searchPosts = api_base + "post/wapi/searchPosts?gids={0}&keyword={1}&last_id={2}&size={3}"
getUserFullInfo = api_base + "user/api/getUserFullInfo?uid={0}"
userPost = api_base + "post/wapi/userPost?offset={0}&size={1}&uid={2}"
userReply = api_base + "post/wapi/userReply?offset={0}&size={1}&uid={2}"
history = api_base + "painter/api/history/list?offset={0}"
getAllGamesForums = api_base + 'apihub/wapi/getAllGamesForums'
getGameList = api_base + 'apihub/api/getGameList'
getForumPostList = api_base + "post/wapi/getForumPostList?forum_id={0}&gids={1}&is_good={2}&is_hot={3}&page_size={4}&sort_type={5}&last_id={6}"
dailyNote_genshin_widget = 'https://api-takumi-record.mihoyo.com/game_record/app/genshin/aapi/widget/v2'
dailyNote_hkrpg_widget = 'https://api-takumi-record.mihoyo.com/game_record/app/hkrpg/aapi/widget'
createVerification = api_base + 'misc/api/createVerification?is_high=true'
notifySetting = api_base + "user/wapi/notify/settings?uid={0}"
getNotifies = api_base + "notification/wapi/getUserGameNotifications?category={0}&gids={1}&only_focus={2}&page_size={3}"

# Posts
login_pwd = api_account_base + 'Api/login_by_password'
login_sms = api_account_base + 'Api/login_by_mobilecaptcha'
follow = api_base + "timeline/api/follow"
unfollow = api_base + "timeline/api/unfollow"
upvotePost = api_base + "apihub/sapi/upvotePost"
collectPost = api_base + 'post/api/collectPost'
releaseReply = api_base + 'post/api/releaseReply'
deleteReply = api_base + 'post/api/deleteReply'
upvoteReply = api_base + "apihub/sapi/upvoteReply"
Cookie_url4 = api_passport_base + 'account/ma-cn-session/app/getTokenBySToken'
getFp = 'https://public-data-api.mihoyo.com/device-fp/api/getFp'
verifyVerification = api_base + 'misc/api/verifyVerification'
send_sms = api_account_base + 'Api/create_mobile_captcha'
