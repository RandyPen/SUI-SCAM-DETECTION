import os
import openai
from dotenv import load_dotenv

load_dotenv()


class GPT():
    def __init__(
        self, 
        openai_api_key: str = os.environ.get("OPENAI_API_KEY"),
        model_name: str = "gpt-3.5-turbo",
        max_tokens: int = 1000,
        temperature: float = 0.0,
    ) -> None:
        self.model = openai.OpenAI(
            api_key=openai_api_key,
        )
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature

    def coin_prompt(self) -> str:
        prompt = """
        Your task is to identify SCAM information. 
        Input the information about the coin and determine if it's a SCAM. 
        The official coin is SUI. If the information contains fields like SUI, airdrop, reward, etc., it's usually a SCAM. 
        SSWP, CETUS, TURBOS is not SCAM.
        You can only give two responses: SCAM or not SCAM.
        """
        return prompt
    
    def object_prompt(self) -> str:
        prompt = """
        Your task is to identify SCAM information. 
        Input the information about the NFT object and determine if it's a SCAM. 
        The goal of SCAM is to lure users into hacker websites to steal their assets. 
        It usually contains enticing fields like SUI, airdrop, reward, congrats, etc., 
        and malicious website addresses. 
        Whereas legitimate NFT objects primarily showcase content about themselves, 
        such as a team's work or descriptions of the work. 
        You need to judge based on the description information. 
        You can only give two responses: SCAM or not SCAM.
        """
        return prompt
    
    def judge_coin(self, feature: str):
        messages = [{"role": "system", "content": self.coin_prompt()}]
        messages.append(
            {
                "role": "user",
                "content": feature,
            }
        )
        completions = self.model.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=messages,
        )
        return completions.choices[0].message.content

    def judge_object(self, feature: str):
        messages = [{"role": "system", "content": self.object_prompt()}]
        messages.append(
            {
                "role": "user",
                "content": feature,
            }
        )
        completions = self.model.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=messages,
        )
        return completions.choices[0].message.content


if __name__ == "__main__":
    gpt = GPT()
    res = gpt.judge_coin("{\"decimals\": 9, \"name\": \"Suiswap Token\", \"symbol\": \"SSWP\", \"description\": \"Suiswap Platform Governance Token\", \"supply\": null, \"address\": \"0x41911b7d8d87ceee4043ea3b83f402a03d0ffa0b286e78b23dcd81c9cde0f02f\", \"iconUrl\": \"https://suiswap.app/images/token/suiswap.svg\"}")
    print(res)
    res = gpt.judge_coin("{\"decimals\": 2, \"name\": \"\", \"symbol\": \"SUI\", \"description\": \"\", \"supply\": \"489700000\", \"address\": \"0xc254ad3d3ffdc01552e0437409b076e44185822a29f0b2651e3bc431cf27e6b7\", \"iconUrl\": null}")
    print(res)
    res = gpt.judge_coin("{\"decimals\": 9, \"name\": \"won\", \"symbol\": \"congratulations! you won 1000 sui ! claim your gain now at: www.lottery-sui.com\", \"description\": \"\", \"supply\": \"210000000000000000\", \"address\": \"0x6114f2c5221ed34e9d670145a35f121f5b23b56adb56985038f90483852a8f77\", \"iconUrl\": \"https://i.imgur.com/dw8n306.png\"}")
    print(res)
    res = gpt.judge_object("My SuiFren!")
    print(res)
    res = gpt.judge_object("Win your $SUI ticket now!. here : https://get-sui.pages.dev")
    print(res)
    res = gpt.judge_object("The DMENS NFT-Pass program has been launched to encourage community participation, contribution, and development by attracting more partners and expanding the community.")
    print(res)
