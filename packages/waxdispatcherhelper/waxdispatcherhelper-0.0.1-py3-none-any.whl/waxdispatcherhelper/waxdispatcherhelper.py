from waxnftdispatcher import AssetSender
import asyncio
import requests
import time
import json

def fetch_container(
	address = '',
	schema = '',
	template = '',
	coll_name = 'pixeltycoons'
	):
    
    max_tries = 3
    limit = 1000
    resultcount = limit
    data = []
    page = 1
    urls = ["http://wax.eosusa.io/atomicassets/v1/assets", "https://api.wax-aa.bountyblok.io/atomicassets/v1/assets", "http://wax.blokcrafters.io/atomicassets/v1/assets", "http://wax.blacklusion.io/atomicassets/v1/assets"]
    n = 1
    while resultcount == limit:
        print(n)
        n+=1
        url = urls[0]#[random.randint(0,3)]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        params = {
        "limit": limit, "order": "asc", "page": page, "burned": "false"}
        if address:
            params['owner'] = address
        if schema:
            params['schema_name'] = schema
        if template:
            params['template_id'] = template
        if coll_name:
            params["collection_name"] = coll_name
        results = requests.get(url, params, headers=headers)
        tries = 0
        sleep_sec = 3
        #print(results.status_code)
        while (results.status_code != 200) and (tries < max_tries):
            #print(results.status_code)
            tries += 1
            time.sleep(sleep_sec)
            url = urls[0]
            results = requests.get(url, params, headers=headers)
        
        assets = json.loads(results.content)
        data += assets["data"]
        resultcount = len(assets['data'])
        page += 1
    return data


class WaxDispatcher:
    def __init__(self, game_assets, collection_wallet, deliver_wallet, private_key):
        self.game_assets = game_assets
        self.collection_wallet = collection_wallet
        self.deliver_wallet = deliver_wallet
        self.private_key = private_key

    def translate_names_to_schema_template_tuples(self, names: list) -> list:
        tuples = []
        for name in names:
            tuples.append(self.game_assets[name])
        print(tuples)
        return tuples


    def prepare_list_with_tx_links(tx_list: list) -> str:
        result_list = ''
        for tx in tx_list:
            result_list += f'[{tx[0:8]}...](https://waxblock.io/transaction/{tx})\n'
        return result_list

    def prep_non_native_nft_txn(self,payload):
        data = fetch_container(address="pixeltycoons", template=payload["template"], coll_name=payload["collection"])
        list = []
        for i in data:
            list.append(i["template_mint"])
        list.sort()
        mint_to_send = list[0]
        for i in data:
            if i["template_mint"] ==mint_to_send:
                asset_id = i["asset_id"]
        assetsender = AssetSender(payload["collection"], self.collection_wallet, self.private_key)
        response = assetsender.send_assets((str(asset_id), ), self.deliver_wallet)
        return response
    
    def prep_txn(self, list_names, address, mint=False):
        print(list_names)
        assets_to_send = self.translate_names_to_schema_template_tuples(list_names)
        print(assets_to_send)           
        assetsender = AssetSender("pixeltycoons", self.collection_wallet, self.private_key)
        if not mint:
            response = assetsender.send_or_mint_assets(assets_to_send, address)
        else:
            response = assetsender.mint_assets(assets_to_send[0][0],assets_to_send[0][1], address,1)
        return response
    
    def deliver(self, prizes, native=True):
        response = self.prep_txn(prizes, self.deliver_wallet, mint=True)
        transfer_results = [tr[1] for tr in response]
        text = f"""\nExtracted: {prizes}"""
        text += f"\nHere are TX links:\n{self.prepare_list_with_tx_links(transfer_results)}"
        return text
        
    def deliver_non_native(self, payload):
        response = self.prep_non_native_nft_txn(payload)
        transfer_results = [tr[1] for tr in response]
        text = f"""\nExtracted: {payload["prize"]}"""
        text += f"\nHere are TX links:\n{self.prepare_list_with_tx_links(transfer_results)}"
        return text