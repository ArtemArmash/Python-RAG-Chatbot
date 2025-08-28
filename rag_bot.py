import telebot
import pandas
import faiss
import numpy
import os
import google.generativeai as genai

faiss_index=faiss.read_index('faiss_index.index')
DataFrame = pandas.read_csv('test.csv')

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Нажаль сталося помилка при зверненні до AІ: {e}")
        return "Не вдалося згенерувати висновок через технічну помилку"

        

def find_relevant_context(user_question):
    vector_user_question = genai.embed_content(
        model='models/embedding-001',
        content=user_question,
        task_type="RETRIEVAL_DOCUMENT"
    )["embedding"]
    
    vector = numpy.array([vector_user_question], dtype="float32")
    distances, indices = faiss_index.search(vector, k=100)
    
    relevant_chunks = DataFrame.iloc[indices[0]]['text_chunk']
    
    context = "\n\n".join(relevant_chunks.tolist())
    
    return context
    



@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, f"Привіт {message.from_user.first_name}")
@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id, "help information")
@bot.message_handler(func=lambda message: True)
def handle_user_question(message):
    user_question = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    context = find_relevant_context(user_question)
    final_prompt=(
         "Ти - корисний AI-асистент. Твоя задача - дати чітку відповідь на питання користувача, "
            "спираючись виключно на наданий нижче контекст. Якщо відповіді в контексті немає, "
            "так і скажи: 'На жаль, в моїй базі знань немає інформації на цю тему'.\n\n"
            f"--- КОНТЕКСТ ---\n{context}\n\n"
            f"--- ПИТАННЯ ---\n{user_question}\n\n"
            "--- ВІДПОВІДЬ ---"
    )
    final_answer = get_gemini_response(final_prompt)
    
    bot.send_message(message.chat.id, final_answer)
    
    


if __name__ == "__main__":
    
    print('Bot starting...')
    bot.polling(none_stop=False)