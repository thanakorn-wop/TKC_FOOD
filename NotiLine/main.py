from fastapi import FastAPI, Request

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
import gspread
from google.oauth2.service_account import Credentials
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("tkcfood-8f98274f30fb.json", scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "15IWOHK72Pg7TkrfY6F_dQTaIYdiemjONnubIiSN_c04"
sheet = client.open_by_key(sheet_id).sheet1
value_list = sheet.sheet1.row_values(1)  # สมมุติว่าค่าที่ต้องการอยู่ในแถวแรก
print("check data ",value_list)
app = FastAPI()

ACCESS_TOKEN = "b2OWovv+Tb1RFeG4cfna2VoqvyiKxveehmq71P/Iz5bSzkPK+HobwYARprfmHXrXo5SnWdC7diDITbt4C2PvQzR/vShEDKiae1BY5y7TgY8ZaaEtxoJTRXoBdu/SI3H0zEBwpUakpNIQpA9Uts+4UwdB04t89/1O/w1cDnyilFU="

USER_ID = "e083ff7ce8eea0a44d73028b3eb89a01"

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(USER_ID)


class Product:

    def __init__(self, name, amount,in_product,exp_date):

        self.name = name
        self.amount = amount
        self.in_product = in_product
        self.exp_date = exp_date

    # def add_stock(self, qty):

    #     self.stock += qty

    # def remove_stock(self, qty):

    #     self.stock -= qty

    def show(self):
        print(self.name, self.amount, self.in_product, self.exp_date)


@app.post("/callback")
async def callback(request: Request):

    signature = request.headers["X-Line-Signature"]

    body = await request.body()
    body = body.decode("utf-8")

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        return {"status": "invalid signature"}

    return {"status": "ok"}


@app.post("/sheet")
async def get_sheet(request: Request):

   

    return {"status": "ok"}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user_text = event.message.text

    print("ข้อความที่ได้รับ:", user_text)
    if(user_text.lower().strip() == "stock" or user_text.upper().strip() == "STOCK" or user_text.strip() == "สต๊อก"):
        user_text = "stock วันนี้?"
        productt    = Product("สินค้า A", 100, "2023-12-31", "2023-12-31")
    
    list_product = f"-------รายการสินค้า-------"+f"\nชื่อสินค้า: {productt.name}\nจำนวน: {productt.amount}\nวันที่รับเข้า: {productt.in_product}\nวันหมดอายุ: {productt.exp_date}"
    user_text = list_product
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text=user_text
        )
    )
