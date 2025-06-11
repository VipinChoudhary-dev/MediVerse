import os   
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, END, WORD
from langchain_community.document_loaders import PyPDFLoader 
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory


# setting up hugging face api token for using ai models
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# path for images and pdf
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/vipinchoudhary/Desktop/MediVerse/Medical_Chatbot/build/assets/frame0")
PDF_DIR = Path(r"/Users/vipinchoudhary/Desktop/MediVerse/Medical_Chatbot/Books")

PDF_FILES = [
    "cardio.pdf",
    "hiv_aids.pdf",
    "anatomy.pdf",
    "cancer.pdf",
    "dermatology.pdf"
]


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# opening all pdf's and loading all the content into an list
all_documents = []
for pdf_name in PDF_FILES:
    loader = PyPDFLoader(str(PDF_DIR / pdf_name))
    all_documents.extend(loader.load())


# converting pdf content into searchable format - highlight
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(all_documents, embeddings)
retriever = db.as_retriever()


# setting up the AI Model
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    temperature=0.5,
    max_new_tokens=250,
    model_kwargs={}
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="result"
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    memory=memory,
    return_source_documents=False,
    output_key="result"
)

# setting up gui
window = Tk()
window.geometry("1100x733")
window.configure(bg="#FFFFFF")
window.resizable(False, False)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=733,
    width=1100,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Background image
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(550.0, 366.0, image=image_image_1)

# Chat area background
canvas.create_rectangle(
    464.0,
    117.0,
    954.0,
    659.0,
    fill="#D9D9D9",
    outline=""
)

# Title text
canvas.create_text(
    124.0,
    117.0,
    anchor="nw",
    text="MEDICAL\nCHATBOT",
    fill="#FFFFFF",
    font=("IBMPlexMono Bold", 48 * -1)
)

# Logo image
image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(
    171.0,
    624.0,
    image=image_image_2
)

# Chat display textbox with larger font
chat_display = Text(
    window,
    bd=0,
    bg="#D9D9D9",
    fg="#000000",
    font=("Helvetica", 16),
    wrap=WORD
)

chat_display.place(x=470, y=130, width=480, height=510)
chat_display.insert(END, "Welcome to the Chatbot! Ask me anything about the PDFs.\n\n")
chat_display.configure(state="disabled")


# User input entry with larger font
query_entry = Entry(
    window,
    bd=1,
    font=("Helvetica", 14)  # Increased font size
)
query_entry.place(x=470, y=660, width=400, height=30)


# Function to handle user query
def ask_question():
    user_query = query_entry.get().strip()
    if not user_query:
        return
    # Display user question
    chat_display.configure(state="normal")
    chat_display.insert(END, f"You: {user_query}\n")
    # Get answer from chain
    try:
        response = qa_chain.invoke({"query": user_query})
        answer = response.get("result", "No answer returned.")
    except Exception as e:
        answer = f"Error: {str(e)}"
    # Display bot answer
    chat_display.insert(END, f"Bot: {answer}\n\n")
    chat_display.configure(state="disabled")
    chat_display.see(END)
    query_entry.delete(0, END)

# creating the ask button
ask_button = Button(
    window,
    text="Ask",
    command=ask_question,
    font=("Helvetica", 14),
    bd=0,
    relief="ridge"
)
ask_button.place(x=880, y=660, width=70, height=30)


window.mainloop()
