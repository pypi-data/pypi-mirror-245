import datetime

import requests
import json
from jsonpath import jsonpath
import time
import random
import hmac
from hashlib import sha1
import random


platform = "FACEBOOK"
def create_general_post(data):
    """创建普通贴文销售，返回响应和贴文销售ID
    sc_common_interface
    platform："FACEBOOK"、"INSTAGRAM"、"FB_GROUP"
    patternModel:
    INCLUDE_MATCH：模式1-留言包含 关键字 或 关键字+数量
    WITH_QTY_MATCH：模式2-留言包含 关键字+数量
    EXACT_MATCH：模式3-留言只有 关键字 或 关键字+数量
    WITH_SPU_MATCH:模式4-留言包含 商品编号+规
    title 不是必填
    """
    env = data["env"]
    headers = data["headers"]
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    patternModel = "INCLUDE_MATCH"
    if "patternModel" in data:
        patternModel = data["patternModel"]
    headers = data["headers"]
    title = "接口自动化创建的普通贴文%d"%int(time.time())
    if "title" in data:
        title = data["title"]
    url = "%s/api/posts/post/sales/create"%env
    body = {
      "platform": platform,
      "type": 1,
      "platforms": [
          platform
      ],
      "title": title,
      "patternModel": patternModel
         }

    while True:
        try:
            response = requests.post(url,headers=headers,json=body)
            # print("响应码",response.status_code)
            if response.status_code==200:
                break
        except Exception as e:
            time.sleep(1)
    response = response.json()
    print("创建贴文返回",response)
    sales_id = response["data"]["id"]
    return response,sales_id

def create_commerce_post(data):
    """创建留言串销售贴文，返回响应和贴文销售ID
    platform："FACEBOOK"、"INSTAGRAM"、"FB_GROUP"
    patternModel:
    INCLUDE_MATCH：模式1-留言包含 关键字 或 关键字+数量
    WITH_QTY_MATCH：模式2-留言包含 关键字+数量
    EXACT_MATCH：模式3-留言只有 关键字 或 关键字+数量
    WITH_SPU_MATCH:模式4-留言包含 商品编号+规
    title 不是必填
    """

    env = data["env"]
    headers = data["headers"]
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    # platform = data["platform"]
    patternModel = "INCLUDE_MATCH"
    if "patternModel" in data:
        patternModel = data["patternModel"]
    title = "接口自动化创建的留言串销售贴文%d" % int(time.time())
    if "title" in data:
        title = data["title"]
    url = "%s/api/posts/post/sales/create"%env
    body = {
      "platform": platform,
      "type": 1,
      "platforms": [
          platform
      ],
      "title": title,
      "patternModel": patternModel,
      "postSubType": "COMMERCE_STACK"
         }
    while True:
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            time.sleep(1)
    response = response.json()
    # print(response)
    sales_id = response["data"]["id"]
    return response,sales_id


def change_dict_into_hump(json_data):
    if isinstance(json_data, dict):
        new_data = {}
        for key, value in json_data.items():
            components = key.split('_')
            new_key = components[0] + ''.join(x.title() for x in components[1:])
            # new_key = key.replace('_', ' ')
            # new_key = new_key.title().replace(' ', '')
            new_data[change_dict_into_hump(new_key)] = change_dict_into_hump(value)
        return new_data
    elif isinstance(json_data, list):
        return [change_dict_into_hump(item) for item in json_data]
    else:
        return json_data



def search_oa_gift(data):
    """
    查询oa赠品，命名转为驼峰和返回第一个赠品的信息
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/gifts"%env
    params = {"page":1}
    response = requests.get(url,headers=headers,params=params).json()
    items = response["data"]["items"]

    if items == []:
        # 新增赠品
        body = {"unlimited_quantity": True, "title_translations": {"zh-cn": "接口自动化新增的赠品%s" % int(time.time())},
                "media_ids": "610d2865ca92cf00264c563c"}
        requests.post(url, headers=headers, json=body).json()
        time.sleep(5)
        #新增后去查询
        response = requests.get(url, headers=headers, params=params).json()
        items = response["data"]["items"]

    # 返回第一个赠品
    gift_info = items[0]
    # 下划线命名转变为驼峰命名
    change_dict_into_hump(gift_info)

    return gift_info,response


def search_oa_product(data):
    """
    查询OA的商品，并返回响应，和第一个商品信息，并转为驼峰命名
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/products?page=1&per_page=4" %env
    response = requests.get(url, headers=headers).json()
    return response

def create_post_lucky_draw(data):
    """
    创建抽奖活动
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    title = "接口自动化创建的抽奖活动%d"%int(time.time())
    if "title" in data:
        title = data["title"]
    body = {"title":title,"activityType":"LUCKY_DRAW","platforms":
        [platform],"timeZone":"Asia/Shanghai"}
    url = "%s/api/posts/post/activity/sales/create"%env
    while True:
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            time.sleep(1)
    response = response.json()
    sales_id = response["data"]["id"]
    return sales_id,response

def modify_lucky_draw(data):
    """
    编辑post投票活动
    :param data:
    activityInfo:
    留言指定文字:keyword 写指定文字，若不选择则为空字符串""
    留言任意文字内容并按赞贴文：taskTypes: ["LIKED_POST", "COMMENT"]
    留言任意文字内容并建立过订单：taskTypes: ["HAD_ORDER", "COMMENT"]
    标记好友：标记好友就必须留言指定文字，tagFriendsNum：1，好友个数
    message:
    若开关关闭则传：
    winComment：""
    winMessage：""
    winReplyComment：""
    days:
    从当前日前算起，要间隔的天数
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    prize_type = ""
    reward = {"reward": None, "rewardType": None}
    if "prize_type" in data:
        prize_type = data["prize_type"]
    if prize_type=="gift":
        gift_info,__ = search_oa_gift(data)
        spuId = gift_info["id"]
        reward = {"reward": {"productDetail":gift_info,"spuId":spuId}, "rewardType": "GIFT"}
    elif prize_type=="product":
        product = search_oa_product(data)["data"]["items"][0]
        product_info = change_dict_into_hump(product)
        spuId = product["id"]
        product_info["productId"] = spuId
        variations= product_info["variations"]
        skuId = ""
        if variations!=[]:
            skuId = variations[0]["id"]
            product_info["variationInfo"] = variations[0]
        product_info["variations"] = []
        reward = {"reward": {"productDetail": product_info, "spuId": spuId,"skuId":skuId}, "rewardType": "PRODUCT"}
    elif prize_type=="discount":
        amount = 1
        if "amount" in data:
            amount = data["amount"]
        reward = {"reward":  {"amount": amount}, "rewardType": "COUPON"}
    keyword = ""
    if "keyword" in data:
        keyword= data["keyword"]
    autoAward = True
    if "autoAward" in data:
        autoAward = data["autoAward"]
    tagFriendsNum = 0
    if "tagFriendsNum" in data:
        tagFriendsNum = data["tagFriendsNum"]
    taskTypes = ["COMMENT"]
    if "taskTypes" in data:
        if "taskTypes" =="order":
            taskTypes = ["HAD_ORDER", "COMMENT"]
        elif "taskTypes" == "like":
            taskTypes = ["LIKED_POST", "COMMENT"]
    activityInfo = {"keyword": keyword, "autoAward": autoAward, "tagFriendsNum": tagFriendsNum, "taskTypes": taskTypes}
    winReplyComment = "🎁 恭喜您中奖！请与小编联系确认领奖细节！"
    if "winReplyComment" in data:
        winReplyComment = data["winReplyComment"]
    winComment = "恭喜 {@winner} 中奖 👏，请与小编联系确认领奖细节！"
    if "winComment" in data:
        winComment = data["winComment"]
    winMessage = "🎁 恭喜您中奖！请与小编联系确认领奖细节！"
    if "winMessage" in data:
        winMessage = data["winMessage"]
    message = {
        "winReplyComment":winReplyComment,
        "winComment":winComment,
        "winMessage":winMessage
    }
    totalWinner = 2
    if "winner" in data:
        totalWinner = data["winner"]
    days = 5
    if "days" in data:
        days = data["days"]
    today = datetime.datetime.now()
    start_time = int(time.mktime(time.strptime(today.strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S')) * 1000)
    end_time = int(time.mktime(
        time.strptime((today + datetime.timedelta(days=days)).strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S')) * 1000)
    if "start_time" in data:
        start_time = data["start_time"]
    if "end_time" in data:
        end_time = data["end_time"]
    body = {"activityType":"LUCKY_DRAW","startTime":start_time,"endTime":end_time,
            "totalWinner":totalWinner,"activityInfo":activityInfo,"message":message,"reward":reward}
    if "sales_id" in data:
        sales_id = data["sales_id"]
    else:
        sales_id,__ = create_post_lucky_draw(data)
    url = "%s/api/posts/activity/post/%s"%(env, sales_id)
    response = requests.put(url,headers=headers,json=body).json()
    return sales_id,response

def get_channel_info(data):
    """
    获取串接的渠道信息
    :param data:   platform："FACEBOOK"、"INSTAGRAM"、"FB_GROUP"
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    # platform = data["platform"]
    url = "%s/api/posts/post/sales/channels?platform=%s"%(env,platform)
    res = requests.get(url, headers=headers).json()
    page_id = res["data"][0]["platformChannelId"]
    page_name = res["data"][0]["platformChannelName"]
    group_id = res["data"][0]["groupId"]
    return page_id,page_name,group_id

def get_page_post(data):
    """
    查询串接的贴文
    :param data:
    since：
    最近7天传：1699027200
    最近30天传：1697040000
    最近90天传：1691856000
    最近180天传：1684080000
    fb group:
    今天：1699545600
    最近3天：1699372800
    type:
    faceboook和ig:POST
    fb group:GROUP_POST
    :return:响应
    """
    env = data["env"]
    headers = data["headers"]
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    if "page_id" in data:
        page_id = data["page_id"]
    else:
        page_id, page_name, group_id = get_channel_info(data)
        if platform=="FB_GROUP":
            page_id = group_id
    type = "POST"
    if "type" in data:
        type = data["type"]
    since = 1699027200
    if "since" in data:
        since = data["since"]
    page_size = 50
    if "page_size" in data:
        page_size = data
    params = {"page_size":page_size,"type":type,"since":since,"party_channel_id":page_id,"platform":platform}
    url = "%s/api/posts/post"%env
    response =requests.get(url,headers=headers,params=params).json()
    return response

def relate_post(data):
    """
    链接贴文，只链接返回的第一个可链接的贴文
    :param data:
    :return:
    """
    global platform
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    if "platform" in data:
        platform = data["platform"].upper()
    response = get_page_post(data)
    available_post_list = []
    related_sales = jsonpath(response,"$..related_sales")
    print("查询到的贴文信息",related_sales)
    for index,value in enumerate(related_sales):
        if value==False:
            available_post_list.append(response["data"]["data"][index])
    url = "%s/api/posts/post/sales/%s/addPost"%(env,sales_id)
    # platform = "FACEBOOK"
    # print(available_post_list[0])
    page_id = jsonpath(available_post_list[0],"$..from.id")[0]
    page_name = jsonpath(available_post_list[0],"$..from.name")[0]
    post_id = jsonpath(available_post_list[0],"$.id")[0]
    message = jsonpath(available_post_list[0],"$.message")[0]
    permalink_url = jsonpath(available_post_list[0],"$.permalink_url")[0]
    status_type = jsonpath(available_post_list[0],"$.status_type")[0]
    picture = jsonpath(available_post_list[0],"$.picture")[0]
    body = {"pageId": page_id, "pageName": page_name, "platform": platform,
        "postList": [{"postId": post_id, "postTitle": page_name,
                      "postDescription": message, "postImageUrl": picture,
                      "permalinkUrl": permalink_url,
                      "statusType": status_type}]}
    response = requests.post(url,headers=headers,json=body).json()
    return response


def create_fb_text_post(data):
    """
    创建fb、fb group纯文本贴文
    :param data: fb group 创建贴文时，pageId为group_id
    :return:post_pid 为贴文在post数据库的ID，取消和编辑贴文时会使用到
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    #获取page信息
    page_id, page_name, group_id = get_channel_info(data)
    postDescription = "一天天工作这么忙，烦死了%d"%int(time.time())
    if "postDescription" in data:
        postDescription = data["postDescription"]
    if platform == "FB_GROUP":
        page_id = group_id
    url = "%s/api/posts/post/%s/post"%(env,sales_id)
    body = {"postDescription":postDescription,"platform":platform,
            "url":[],"mediaFbid":[],"pageId":page_id}
    response = requests.post(url,headers=headers,json=body).json()
    post_id = response["data"]["post_id"]
    post_pid = response["data"]["id"]
    return post_id,post_pid,response

def search_post_product(data):
    """
    查询可添加的商品，只查询前10个，和查询openApi/proxy/v1/products不一样，这个接口经过post组装关键字返回
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/common/product/key/spu/list?page=1&searchType=ALL&pageSize=10"%env
    response = requests.get(url, headers=headers).json()
    productSpuKeyVos = response["data"]["productSpuKeyVos"][0]
    skuKeys = productSpuKeyVos["skuKeys"]
    spuId = productSpuKeyVos["spuId"]
    return skuKeys,spuId,response


def model_one_add_product(data):
    """
    贴文销售模式1-模式3添加商品，只添加第一个商品到贴文
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s/products"%(env,sales_id)
    skuKeys, spuId, response = search_post_product(data)
    skuList = []
    body = {}
    if skuKeys != None:
        for index, sku in enumerate(skuKeys):
            skuId = sku["skuId"]
            spuId = sku["spuId"]
            sku_data = {}
            sku_data["skuId"] = skuId
            sku_data["missCommonKey"] = False
            sku_data["keyList"] = ["模式1关键字%d" % index]
            skuList.append(sku_data)
    # print(skuList)
    if skuList == []:
        body = {
            "spuList": [{"spuId": spuId, "missCommonKey": "false", "customNumbers": [], "keyList": ["无规格商品关键字"]}]}
    else:
        body = {
            "spuList": [{"spuId": spuId, "missCommonKey": "false", "customNumbers": [], "skuList": skuList}]}
    response = requests.post(url, headers=headers, json=body).json()
    return response

def model_four_add_product(data):
    """
    贴文销售模式4添加商品，只添加第一个商品到贴文
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s/products"%(env,sales_id)
    skuKeys, spuId, response = search_post_product(data)
    skuList = []
    if skuKeys != None:
        for index, sku in enumerate(skuKeys):
            skuId = sku["skuId"]
            spuId = sku["spuId"]
            sku_data = {}
            sku_data["skuId"] = skuId
            sku_data["missCommonKey"] = False
            skuList.append(sku_data)
    # print(skuList)
    customNumbers = "模式4接口关键字下单"
    body = {}
    if skuList == []:
        body = {"spuList": [
            {"spuId": spuId, "missCommonKey": "true", "customNumbers": [customNumbers], "customNumber": customNumbers}]}
    else:
        body = {"spuList": [
            {"spuId": spuId, "missCommonKey": "false", "customNumbers": [customNumbers], "customNumber": customNumbers,
             "skuList": skuList}]}
    response = requests.post(url, headers=headers, json=body).json()
    return response

def modify_post_schedule(data):
    """
    修改贴文排程时间
    :param data: start_time若没有传则默认给当前时间，end_time若没有传则默认是永远有效
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    start_time = int(time.time() * 1000)
    end_time = 32503611599000
    if "start_time" in data:
        start_time = data["start_time"]
    if "end_time" in data:
        end_time = data["end_time"]
    url = "%s/api/posts/post/sales/schedule/%s"%(env,sales_id)
    body = {"start_time": start_time, "end_time": end_time}
    response = requests.put(url,headers=headers,json=body).json()
    return response

def publish_post(data):
    """启用贴文"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    #启用前先修改排程时间，若没有传时间，则按默认值设置
    modify_post_schedule(data)
    url = "%s/api/posts/post/sales/publish/%s"%(env,sales_id)
    response = requests.put(url, headers=headers).json()
    return response

def end_post_activity(data):
    """
    抽奖活动开奖
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/activity/end/%s"%(env,sales_id)
    response = requests.put(url,headers=headers).json()
    return response

def get_post_activity_winner(data):
    """
    获取获奖者
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/activity/listWinner/%s?limit=1000"%(env,sales_id)
    response = requests.get(url,headers=headers).json()
    return response


def get_post_info(data):
    """
    获取贴文信息
    :param data:
    :return: 贴文全部信息，若需要调用后再过滤
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s?fieldScopes=DETAILS,PRODUCT_NUM," \
          "SALES_CONFIG,LOCK_INVENTORY,PRODUCT_LIST"%(env,sales_id)
    response = requests.get(url, headers=headers).json()
    return response

def get_post_activity_detail(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/activity/detail/%s"%(env,sales_id)
    response = requests.get(url, headers=headers).json()
    return response

def get_post_list(data):
    """
    查询活动列表
    贴文销售列表：POST，活动：ACTIVITY
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_type = "POST"
    if "sales_type" in data:
        sales_type = data["sales_type"]
    params = {"page_num":1,"page_size":10,"sales_type":sales_type}
    url = "%s/api/posts/post/sales"%env
    response = requests.get(url,headers=headers,params=params).json()
    return response


def get_post_product_keyword(data):
    """获取贴文返回第一个商品的关键字"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s?fieldScopes=PRODUCT_LIST" % (env, sales_id)
    response = requests.get(url, headers=headers).json()
    keyword = jsonpath(response,"$..custom_keys_label_str")[0]
    return keyword,response



def send_post_comment(data):
    """
    在贴文下留言
    :param data:
    :return:
    """
    #获取关联的贴文信息-第一则贴文
    type = "post"
    if "type" in data:
        type = data["type"]
    response = {}
    if type == "post":
        response = get_post_info(data)
    elif type == "activity":
        response = get_post_activity_detail(data)
    related_post_list = response["data"]["related_post_list"][0]
    page_id = related_post_list["page_id"]
    post_id = related_post_list["post_id"]
    stamp = int(time.time())
    num = random.randint(100000, 999999)
    user_id = "488864%d" % int(time.time())
    name = "test post%d" % int(time.time())
    comment_id = "%s_%d%d" % (page_id, stamp, num)
    env = data["env"]
    keyword = "接口测试普通留言"
    if "keyword" in data:
        keyword = data['keyword']
    key = data["key"]
    body = {"object": "page", "entry": [{"id": page_id, "time": stamp, "changes": [{"field": "feed", "value": {
        "from": {"id": user_id, "name": name},
        "post": {"status_type": "added_video", "is_published": True, "updated_time": "2022-11-18T09:57:26+0000",
                 "permalink_url": "https://www.facebook.com/permalink.php?story_fbid=pfbid02jLK3e6YdFSXp2DmD7j7vtStLXoBzTi8rxKrp6jFhVMUTTEgz6qvZA8soR9Uwydd8l&id=107977035056574",
                 "promotion_status": "inactive", "id": post_id}, "message": keyword, "item": "comment",
        "verb": "add", "post_id": post_id, "comment_id": comment_id,
        "created_time": stamp, "parent_id": post_id}}]}]}
    url = "%s/facebook/webhook"%env
    sign_text = hmac.new(key.encode("utf-8"), json.dumps(body).encode("utf-8"), sha1)
    signData = sign_text.hexdigest()
    print(signData)
    header = {"Content-Type": "application/json", "x-hub-signature": "sha1=%s" % signData}
    response = requests.post(url, headers=header, data=json.dumps(body))
    return user_id,name,comment_id



def get_payment(data):
    """
    获取店铺的付款方式，默认查询10条
    :param data:
    :return:默认返回第一个支付方式
    """
    env = data["env"]
    headers = data["headers"]
    url ="%s/openApi/proxy/v1/payments?page=1&per_page=10&include_fields[]=config_data.tappay"%env
    response = requests.get(url, headers=headers).json()
    payment_id = response["data"]["items"][0]["id"]
    return payment_id,response

def get_delivery(data):
    """
    获取店铺的物流方式，默认查询10条
    :param data:
    :return:默认返回第一个物流方式
    """
    # print("物流data",data)
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/delivery_options?page=1&per_page=10"%env
    response = requests.get(url, headers=headers).json()
    delivery_id = response["data"]["items"][0]["id"]
    return delivery_id,response

def get_comment_user(data):
    """
    查询留言面板的留言用户，查全部，并返回第一个留言用户
    :return:post_user_id,编辑购物车，发送购物车链接需要用到这个值
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/comments"%env
    params = {"pageNo":1,"pageSize":10,"salesId":sales_id}
    response = requests.get(url, headers=headers,params=params).json()
    post_user_id = jsonpath(response, "$..id")[0]
    return post_user_id,response

def post_edit_cart(data):
    """
    编辑购物车，给用户加入查询到的第一个商品：没有排除无库存的情况
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    post_user_id, __ = get_comment_user(data)
    url = "%s/api/posts/post/sales/%s/user/" \
          "%s/cart/item?skip_reapply_promotion=false"%(env,sales_id,post_user_id)
    response = search_oa_product(data)
    variations = response["data"]["items"][0]["variations"]
    spu_id = response["data"]["items"][0]["id"]
    quantity = 1
    if "quantity" in data:
        quantity = data["quantity"]
    body = {"spu_id": spu_id, "owner_type": "Guest", "quantity": quantity, "type": "product"}
    if variations != []:
        sku_id = variations[0]["id"]
        body = {"spu_id": spu_id, "owner_type": "Guest", "sku_id": sku_id, "quantity": quantity,
                "type": "product"}
    response = requests.post(url, headers=headers, json=body).json()
    return response

def manual_order(data):
    """
    创建会员，若存在则合并会员
    创建订单
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    phone = "18776343453"
    if "query" in data:
        phone = data["query"]
    __,response = get_comment_user(data)
    # print("留言面板查询返回",response)
    name = jsonpath(response,"$..name")[0]
    user_id = jsonpath(response,"$..psid")[0]
    page_id = jsonpath(response, "$..page_id")[0]
    # 先查询号码或邮箱是否被占有
    url = "%s/openApi/proxy/v1/customers/search?query=%s&per_page=50&search_fields[]=mobile_phone" \
          "&search_fields[]=phones" %(env,phone)
    response = requests.get(url, headers=headers).json()
    items = response["data"]["items"]
    #创建会员
    url = "%s/uc/customers/merge" % env
    body = {"email": "", "mobile_phone": phone, "mobile_phone_country_calling_code": "86",
            "name": name, "page_scoped_id": user_id, "locale_code": None, "country_code": "cn",
            "id": None, "party_channel_id": page_id, "platform": "FACEBOOK", "is_member": True}
    if items != []:
        id = jsonpath(response, "$..id")[0]
        body = {"email": "", "mobile_phone": phone, "mobile_phone_country_calling_code": "86",
                "name": name, "page_scoped_id": user_id, "locale_code": None, "country_code": "cn",
                "id": id, "party_channel_id": page_id, "platform": "FACEBOOK", "is_member": True}

    res = requests.put(url, headers=headers, json=body).json()
    customer_id = res["data"]["id"]
    #给会员新增物流地址
    rl = "%s/uc/customers/%s" % (env,customer_id)
    postcode = "76653"
    delivery_data = {"delivery_addresses": [
        {"city": "bb", "country": "CN", "postcode": postcode, "recipient_name": name,
         "recipient_phone": phone, "recipient_phone_country_code": "86", "logistic_codes": [],
         "address_1": "aa"}]}
    res = requests.put(url, json=delivery_data, headers=headers).json()
    # print("信息会员物流地址返回",res)

    # 查询会话ID
    # platform = "facebook"
    # if "platform" in data:
    #     platform = data["platform"]
    # url = "%s/mc/conversation/id?type=%s&user_id=%s&party_channel_id=%s" % (env,platform,user_id, page_id)
    # # param = {"type":"facebook","user_id":vars["user_id"],"party_channel_id":vars["platform_channel_id"]}
    # response = requests.get(url, headers=headers).json()
    # conversation_id = jsonpath(response, "$.data.id")[0]
    data["user_id"] = user_id
    data["page_id"] = page_id
    conversation_id,__ = get_user_conversation_id(data)

    # 给cart 设置物流 和设置支付方式
    url = "%s/openApi/proxy/v1/internal/mc/api/carts/%s?owner_type=User&cart_uid=%s&created_by=post&skip_reapply_promotion=false&shop_session_id=%s" % (
    env,customer_id, customer_id, user_id)
    delivery_id,__ = get_delivery(data)
    payment_id,__ = get_payment(data)
    body = {"delivery_option_id": delivery_id, "country": "CN", "countryCode": "CN",
            "payment_id": payment_id}
    res = requests.put(url, headers=headers, json = body).json()
    # print("设置cart",res)
    # 成立订单
    url = "%s/manual_order/checkout"%env
    delivery_address = delivery_data["delivery_addresses"][0]
    delivery_address["district"] = None
    delivery_address["key"] = None
    delivery_address["regioncode"] = None
    delivery_address["province"] = None
    delivery_address["address_2"] = None
    delivery_address["country_code"] = "CN"
    body = {"country": "CN", "customer_email": None, "customer_id": customer_id, "customer_name": name,
            "customer_phone": phone, "whatsapp_phone": phone, "delivery_address": delivery_address,
            "delivery_data": {"recipient_name": name, "recipient_phone": phone},
            "delivery_option_id": delivery_id, "display_payment_info": False, "invoice": {}, "lang": "zh-cn",
            "order_remarks": "", "order_tags": [], "payment_id": payment_id,
            "payment_info": "{\"text\":\"\",\"images\":[]}", "send_notification": False, "created_by": "post",
            "created_from": "admin_post", "platform": "FACEBOOK", "conversation_id": conversation_id,
            "merchant_name": "泰国店", "shop_session_id": user_id, "platform_channel_name": "kkk",
            "source_data": {"type": "fb", "source_id": page_id}, "customer_phone_country_code": "86",
            "postcode": postcode}
    res = requests.post(url,headers=headers,json=body).json()
    # print("创建订单返回",res)
    #获取订单ID
    orderNumber = jsonpath(res,"$..orderNumber")[0]

    return orderNumber,customer_id,res

def get_user_conversation_id(data):
    """
    :return: 会员ID
    platform 为小写，有一些是大写，这个要注意区分
    """
    # 查询会话ID
    env = data["env"]
    headers = data["headers"]
    user_id = data["user_id"]
    page_id = data["page_id"]
    platform = "facebook"
    if "platform" in data:
        platform = data["platform"].lower()
    url = "%s/mc/conversation/id?type=%s&user_id=%s&party_channel_id=%s" % (env, platform, user_id, page_id)
    # param = {"type":"facebook","user_id":vars["user_id"],"party_channel_id":vars["platform_channel_id"]}
    response = requests.get(url, headers=headers).json()
    print(response)
    conversation_id = jsonpath(response, "$.data.id")[0]
    return conversation_id,response

def get_user_message(data):
    """
    获取信息
    :param data: 
    :return: 
    """""
    env = data["env"]
    headers = data["headers"]
    # 获取发送的私讯内容
    conversation_id,__ = get_user_conversation_id(data)
    url = "%s/mc/message/%s?create_time="%(env,conversation_id)
    response = requests.get(url,headers=headers).json()
    content = jsonpath(response,"$..content")[0]
    text = ""
    if "message" in json.loads(content):
        text = json.loads(content)["message"]["attachment"]["payload"]["text"]
    return text


def modify_order_status(data):
    """
    :param data:
    status:订单的状态
    confirmed:已确认
    pending：处理中
    completed：已完成
    cancelled ：已取消
    :return:
    """
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    status = data["status"]
    # 查询订单id
    global customer_id
    if "customer_id" in data:
        customer_id = data["customer_id"]
    else:
        __,customer_id,__ = manual_order(data)
    url = "%s/v1/orders/search?page=1&per_page=5&customer_id=%s" % (oa_env,customer_id)
    res = requests.get(url, headers=oa_headers).json()
    order_id = jsonpath(res, "$..id")[0]
    # print("订单ID", vars["order_id"])
    # 修改订单状态为-已确认
    url = "%s/v1/orders/%s/status" % (oa_env,order_id)
    body = {
        "status": status,
        "mail_notify": False
    }
    res = requests.patch(url, headers=oa_headers, json=body).json()

def modify_order_payment_status(data):
    """
    :param data:
    status:订单的状态
    pending：未付款
    completed：已付款
    refunding ：退款中
    refunded：已退款
    partially_refunded：部分退款
    :return:
    """
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    status = data["status"]
    # 查询订单id
    global customer_id
    if "customer_id" in data:
        customer_id = data["customer_id"]
    else:
        __,customer_id,__ = manual_order(data)
    url = "%s/v1/orders/search?page=1&per_page=5&customer_id=%s" % (oa_env,customer_id)
    res = requests.get(url, headers=oa_headers).json()
    order_id = jsonpath(res, "$..id")[0]
    # print("订单ID", vars["order_id"])
    # 修改订单状态为-已确认
    url = "%s/v1/orders/%s/order_payment_status" % (oa_env,order_id)
    body = {
        "status": status,
        "mail_notify": False
    }
    res = requests.patch(url, headers=oa_headers, json=body).json()

def modify_order_delivery_status(data):
    """
    :param data:
    status:订单的状态
    pending：备货中
    shipping：发货中
    shipped ：已发货
    arrived：已到达
    collected：已取货
    returned：已退货
    returning：退款中
    :return:
    """
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    status = data["status"]
    # 查询订单id
    global customer_id
    if "customer_id" in data:
        customer_id = data["customer_id"]
    else:
        __,customer_id,__ = manual_order(data)
    url = "%s/v1/orders/search?page=1&per_page=5&customer_id=%s" % (oa_env,customer_id)
    res = requests.get(url, headers=oa_headers).json()
    order_id = jsonpath(res, "$..id")[0]
    # print("订单ID", vars["order_id"])
    # 修改订单状态为-已确认
    url = "%s/v1/orders/%s/order_delivery_status" % (oa_env,order_id)
    body = {
        "status": status,
        "mail_notify": False
    }
    res = requests.patch(url, headers=oa_headers, json=body).json()

def delete_post(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s"%(env,sales_id)
    res = requests.delete(url, headers=headers).json()
    return res

def modelone_create_single_product(data):
    """
    贴文新增无规格商品
    :param data:
    :return: 返回新增的商品的spu_id
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s/product/create" % (env, sales_id)
    product_name = "post接口新增商品多规格商品名称%d" % int(time.time())
    if "product_name" in data:
        product_name = data["product_name"]
    keyword = "post接口新增商品多规格商品关键字%d" % int(time.time())
    if "keyword" in data:
        keyword = data["keyword"]
    body = {"customKey":keyword,"quantity":5,"unlimitedQuantity":False,"productName":product_name,
            "imageUrl":"https://s3-ap-southeast-1.amazonaws.com/static.shoplineapp.com/sc-admin/product-default.png","price":3}
    response = requests.post(url,headers=headers,json=body).json()
    spu_id = response["data"]
    return spu_id

def modelone_create_mutil_product(data):
    """
    贴文新增多规格商品，
    :param data: variance需要传入需要新增的规格:格式:{"color":["红","黄"],"size":["X","M"]}
    规格类型，规格具体名称
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s/product/create"%(env,sales_id)
    product_name = "post接口新增商品多规格商品名称%d"%int(time.time())
    if "product_name" in data:
        product_name = data["product_name"]
    keyword = "post接口新增商品多规格商品关键字%d"%int(time.time())
    if "keyword" in data:
        keyword = data["keyword"]
    variance = {"color":["红","黄"],"size":["X","M"]}
    if "variance" in data:
     variance = data["variance"]
    customVariantTypes = []
    variantOptions = []
    variations = []
    variance_type = variance.keys()
    custom_keys = []
    for index,value in enumerate(variance_type):
        customVariantType = {}
        customVariantType["type"] = "custom_%d"%(index+1)
        customVariantType["name"] = value
        customVariantTypes.append(customVariantType)
        variance_names = variance[value]
        custom_key = []
        for index,value in enumerate(variance_names):
            variantOption = {}
            variantOption["type"] = "custom_%d"%(index+1)
            customVariantType["name"] = value
            customVariantType["key"] = "custom_%d_%s_4218"%(index+1,value)
            custom_key.append(customVariantType["key"])
            variantOptions.append(variantOption)
        custom_keys.append(custom_key)

    # body = {"unlimitedQuantity":False,"productName":product_name,"imageUrl":"https://s3-ap-southeast-1.amazonaws.com/static.shoplineapp.com/sc-admin/product-default.png",
    #         "customVariantTypes":,"price":0}

def get_mc_post(data):
    """
    获取mc贴文信息，若配传page_id,则通过sales_id去查贴文关联的粉丝页信息
    :param data:
    :return:只查询前100个贴文
    """
    env = data["env"]
    headers = data["headers"]
    page_id = ""
    if "page_id" in data:
        page_id = data["page_id"]
    else:
        response = get_post_info(data)
        page_id = jsonpath(response,"$..page_id")[0]
    url = "%s/mc/postcomment/post"%env
    params = {"platform_channel_id":page_id,"staff_id":"all","page_num":1,"page_size":100}
    response = requests.get(url, headers=headers,params=params).json()
    id = jsonpath(response,"$..id")
    post_id = jsonpath(response,"$..post_id")
    return id,post_id,response

def get_post_comment(data):
    """
    没有传则查询贴文关联的post_id
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    id_list, post_id_list, __ = get_mc_post(data)
    post_id = ""
    if "post_id" in data:
        post_id = data["post_id"]
    else:
        response = get_post_info(data)
        post_id = jsonpath(response, "$..post_id")[0]
    mc_post_id = 1
    for index,value in enumerate(post_id_list):
        if value==post_id:
            mc_post_id = id_list[index]
    url = "%s/mc/postcomment/comments"%env
    params = {"post_id":mc_post_id,"page_num":1,"page_size":10}
    response = requests.get(url, headers=headers, params=params).json()
    return response

def get_post_product_comment(data):
    """
    获取盖大楼销售，创建商品评论的信息
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/product/send/msg/info/%s"%(env,sales_id)

def modify_post_general_config(data):
    """
 修改通用配置
    :param data:
    patternModel：默认 INCLUDE_MATCH
    INCLUDE_MATCH：模式1-留言包含 关键字 或 关键字+数量
    WITH_QTY_MATCH：模式2-留言包含 关键字+数量
    EXACT_MATCH：模式3-留言只有 关键字 或 关键字+数量
    WITH_SPU_MATCH:模式4-留言包含 商品编号+规
    lockStock：False,True，默认False
    salesStockLockPreTime:lockStock 为True,必传，枚举值："" ，7，14，传""为每场销售活动自动时间
    schedule_time:枚举值：0,7,14,30    0为：用不过期
    :return:返回查询的通用配置
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales/global/POST" % env
    patternModel = "INCLUDE_MATCH"
    #下单模式
    if "patternModel" in data:
        patternModel = data["patternModel"]
    lockStock = False
    #锁库存设置
    if "lockStock" in data:
        patternModel = data["lockStock"]
    salesStockLockPreTime = 7
    if "salesStockLockPreTime" in data:
        patternModel = data["salesStockLockPreTime"]
    #私讯回复
    needSendMessage = True
    if "needSendMessage" in data:
        needSendMessage = data["needSendMessage"]
    hasInteractionTopMessage = "您好，以下商品加单成功！{products}💰购物车商品总金额: {total}请前往购物网站！一定时间内有交互信息%d"%int(time.time())
    if "hasInteractionTopMessage" in data:
        needSendMessage = data["hasInteractionTopMessage"]
    hasInteractionMessageButton = "一定时间内有交互按钮%d"%int(time.time())
    if "hasInteractionMessageButton" in data:
        hasInteractionMessageButton = data["hasInteractionMessageButton"]
    noInteractionFirstTopMessage = "您好，以下商品加单成功！{products}💰 购物车商品总金额: {total}请前往购物网站！一定时间内没有交互%d"%int(time.time())
    if "noInteractionFirstTopMessage" in data:
        noInteractionFirstTopMessage = data["noInteractionFirstTopMessage"]
    noInteractionFirstMessageButton = "继续%d"%int(time.time())
    if "noInteractionFirstMessageButton" in data:
        noInteractionFirstMessageButton = data["noInteractionFirstMessageButton"]
    noInteractionSecondTopMessage = "您好，以下商品加单成功！{products}💰 购物车商品总金额: {total}请前往购物网站！点击继续后发送的消息%d"%int(time.time())
    if "noInteractionSecondTopMessage" in data:
        noInteractionSecondTopMessage = data["noInteractionSecondTopMessage"]
    noInteractionSecondMessageButton = "立即结账%d"%int(time.time())
    if "noInteractionSecondMessageButton" in data:
        noInteractionSecondMessageButton = data["noInteractionSecondMessageButton"]
    #留言回复
    comment_reply_need_reply = True
    if "comment_reply_need_reply" in data:
        comment_reply_need_reply = data["comment_reply_need_reply"]
    comment_reply_content = "您好，{customerName},谢谢你在贴文下留言订购以下商品。%d"%int(time.time())
    if "comment_reply_content" in data:
        comment_reply_content = data["comment_reply_content"]
    all_out_of_stock_need_reply = True
    if "all_out_of_stock_need_reply" in data:
        all_out_of_stock_need_reply = data["all_out_of_stock_need_reply"]
    all_out_of_stock_content = "您好，{customerName}，以下商品库存不足，请选购其他商品，谢谢!%d"%int(time.time())
    if "all_out_of_stock_content" in data:
        all_out_of_stock_content = data["all_out_of_stock_content"]
    schedule_time = 0
    if "schedule_time" in data:
        schedule_time = data["schedule_time"]
    body = {"saveList":[{"configKey":"PATTERN_MODEL","configValue":{"patternModel":patternModel}},
                        {"configKey":"STOCK","configValue":{"lockStock":lockStock,"salesStockLockPreTime":salesStockLockPreTime}},
                        {"configKey":"MESSAGE","configValue":{"needSendMessage":needSendMessage,"noInteractionMessage":
                            {"firstMessageTemplate":{"topMessage":noInteractionFirstTopMessage},"firstMessageButton":noInteractionFirstMessageButton,
                             "secondMessageTemplate":{"topMessage":noInteractionSecondTopMessage},"secondMessageButton":noInteractionSecondMessageButton},
                           "hasInteractionMessage":{"firstMessageTemplate":{"topMessage":hasInteractionTopMessage},"messageButton":hasInteractionMessageButton},"hasLink":True}},
                        {"configKey":"COMMENT_REPLY","configValue":{"need_reply":comment_reply_need_reply,"content":comment_reply_content}},
                        {"configKey":"ALL_OUT_OF_STOCK_POST","configValue":{"need_reply":all_out_of_stock_need_reply,
                        "content":all_out_of_stock_content}},{"configKey":"SCHEDULE_TIME","configValue":{"salesPreEndTime":schedule_time}}]}
    requests.post(url,headers=headers,json=body).json()
    time.sleep(3)
    #修改后获取通用配置
    response = requests.get(url,headers=headers).json()
    return response

def copy_post(data):
    """
    复制单个贴文销售
    :param data:
    :return: 复制生成贴文的sales_id，请求内容
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/copy/%s"%(env,sales_id)
    response = requests.post(url,headers=headers).json()
    sales_id = response["data"]["id"]
    return sales_id,response

def end_post(data):
    """
    手动结束贴文
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/disconnectPost/%s"%(env,sales_id)
    response = requests.post(url,headers=headers).json()
    return response




if __name__=="__main__":
  pass