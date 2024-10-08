import pyautogui
import time
import pyperclip
from openai import OpenAI
import google.generativeai as genai

def is_last_msg_from_myself(chat_log,sender_name):
    messages = chat_log.strip().split("\n")
    for message in reversed(messages):
        parts = message.split(": ",2)
        if len(parts) >= 2:
            sender,content = parts
            timstamps,name= sender.split("]")
            if(name.strip() == sender_name):
                return True
            else:
                return False
    return False


def autoReply(open_ai_key,genai_key,whatsapp_icon,arrowDown_icon,chat_window_start,chat_window_end,name,description,textbox,top_chat,stop_exec):

    genai.configure(api_key=genai_key)
    client = OpenAI(
        api_key=open_ai_key
    )
    # Click on the icon at (1269, 1061)
    pyautogui.click(whatsapp_icon["x"], whatsapp_icon["y"])

    # Wait for the click action to complete
    time.sleep(1)
    while not stop_exec.is_set():
        # Wait for 2 seconds to give you time to bring the window in focus
        time.sleep(2)

        # select top chat
        pyautogui.click(top_chat["x"],top_chat["y"])
        time.sleep(1)

        #click down text
        pyautogui.click(arrowDown_icon["x"],arrowDown_icon["y"])
        time.sleep(1)

        # Move to (670, 195) and start dragging to (670, 165)
        pyautogui.moveTo(chat_window_start["x"],chat_window_start["y"])
        pyautogui.mouseDown()
        pyautogui.moveTo(chat_window_end["x"], chat_window_end["y"], duration=1)  # Drag with 1 second duration
        pyautogui.mouseUp()

        # Press 'Ctrl+C' to copy the selected text
        pyautogui.hotkey('ctrl', 'c')

        # Wait a moment to ensure the text has been copied
        time.sleep(0.5)
        pyautogui.click(arrowDown_icon["x"], arrowDown_icon["y"])

        # Use pyperclip to get the text from the clipboard
        chat_history = pyperclip.paste()

        # # Print the copied text (optional)
        # print("Copied text:", chat_history)

        if is_last_msg_from_myself(chat_history,name) or chat_history.strip() == "":
            time.sleep(5)
            continue

        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a person named {name}, who speaks both hindi as well as english. Your complete description is this - {description}. You just return reply that should be given and no extra text please.Output should be next chat response as {name}."},
                    {
                        "role": "user",
                        "content": chat_history
                    }
                ]
            )
            response = completion.choices[0].message
        except Exception as e:
            model = genai.GenerativeModel("gemini-1.5-flash")
            chat = model.start_chat(
                history=[
                    {"role": "model", "parts": f"You are a person named {name}, who speaks both hindi as well as english. Your complete description is this - {description}. You just return reply that should be given and no extra text please.Output should be next chat response as {name}."}
                ]
            )   

            response = (chat.send_message(chat_history)).text



        #copying response to clipboard
        pyperclip.copy(response)

        # click on the text box
        pyautogui.click(textbox["x"],textbox["y"])
        time.sleep(1)

        # Press 'Ctrl+V' to copy the selected text
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)

        # press enter
        pyautogui.press('enter')
        time.sleep(1)

        time.sleep(5)


