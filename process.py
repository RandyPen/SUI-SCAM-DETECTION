from pysui import SuiConfig, SuiRpcResult
from pysui.sui.sui_pgql.pgql_clients import SuiGQLClient
import pysui.sui.sui_pgql.pgql_query as qn
import pysui.sui.sui_pgql.pgql_types as ptypes
import gpt
import json


sui_object_not_own_types = (ptypes.SuiObjectOwnedImmutable, ptypes.SuiObjectOwnedShared, ptypes.SuiObjectOwnedParent)
sui_coin_datatype = "0x0000000000000000000000000000000000000000000000000000000000000002::coin::Coin"


class Processor():
    def __init__(
        self
    ) -> None:
        self.client = SuiGQLClient(
            write_schema=False,
            config=SuiConfig.default_config(),
        )
        self.judger = gpt.GPT()
        with open('./data/coin-list.json', 'r') as file:
            coin_data = json.load(file)

        self.coin_block_list = coin_data['blocklist']
        self.coin_white_list = coin_data['whitelist']

        with open('./data/object-list.json', 'r') as file:
            object_data = json.load(file)

        self.object_block_list = object_data['blocklist']
        self.object_white_list = object_data['whitelist']

    def process(self, file_path: str = "to_process.txt"):
        with open(file_path, 'r') as file:
            for line in file:
                object_id = line.strip()
                if not object_id.startswith("0x"):
                    continue
                
                try:
                    print("-------------")
                    print(object_id)
                    res = self.get_object_info(object_id)
                    if res:
                        self.parse(res)
                except KeyError: # for kiosk object
                    continue

    def get_object_info(self, object_id: str) -> SuiRpcResult:
        """Fetch specific object data."""
        result = self.client.execute_query_node(with_node=qn.GetObject(object_id=object_id))
        return result if result.is_ok() else None
        
    def get_coin_metadata(self, object_type: str) -> SuiRpcResult:
        """Fetch coin meta data."""
        result = self.client.execute_query_node(with_node=qn.GetCoinMetaData(coin_type=object_type))
        return result if result.is_ok() else None
    
    def get_object_display_info(self, object_id: str) -> None:
        """Fetch specific object data."""
        QUERY = """
        query Object {
            object(address: \"""" + object_id + """\") {
                display {
                key 
                value
                error
                }
            }
        }
        """
        result = self.client.execute_query_string(string=QUERY)
        return result if result.is_ok() else None
    
    def parse(self, result: SuiRpcResult):
        data = result.result_data
        try:
            object_owner = data.object_owner
            if isinstance(object_owner, sui_object_not_own_types):
                # print(object_owner)
                return
        except AttributeError: # for kiosk object
            return
        
        content = data.content
        object_type = data.object_type
        has_public_transfer = data.has_public_transfer
        owner_id = data.owner_id
        object_id = data.object_id

        if object_type.startswith(sui_coin_datatype):
            print("Coin")
            object_type = object_type[79:-1]
            if object_type in self.coin_white_list or object_type.startswith(sui_coin_datatype[:-12]):
                return
            coin_metadata = self.get_coin_metadata(object_type)
            feature = str(coin_metadata.result_data.to_json())
            result = self.judger.judge_coin(feature)
            print(result)
            if result == "SCAM" and object_type not in self.coin_block_list:
                self.coin_block_list.append(object_type)
        else:
            print("Not Coin")
            if object_type in self.object_white_list:
                return
            display_info = self.get_object_display_info(object_id)
            feature = "content: " + str(content) + str(display_info)
            result = self.judger.judge_object(feature)
            print(result)
            if result == "SCAM" and object_type not in self.object_block_list:
                self.object_block_list.append(object_type)

    def write(self) -> None:
        coin_data = dict()
        coin_data['blocklist'] = self.coin_block_list
        coin_data['whitelist'] = self.coin_white_list
        with open('./data/coin-list.json', 'w') as file:
            json.dump(coin_data, file, indent=4)

        object_data = dict()
        object_data['blocklist'] = self.object_block_list
        object_data['whitelist'] = self.object_white_list
        with open('./data/object-list.json', 'w') as file:
            json.dump(object_data, file, indent=4)

        # with open('./to_process.txt', 'w') as file:
        #     file.write("")


if __name__ == "__main__":
    processor = Processor()
    processor.process("to_process.txt")
    processor.write()
