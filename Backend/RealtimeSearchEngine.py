import datetime
from serpapi import GoogleSearch as SerpAPISearch
from groq import Groq
from json import load, dump
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
SerpAPIKey = env_vars.get("SerpAPIKey")

client = Groq(api_key=GroqAPIKey)

messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.

IMPORTANT INSTRUCTIONS:
*** You MUST answer ONLY based on the provided search results between [start] and [end] tags ***
*** DO NOT use training data if search results are provided ***
*** Provide answers professionally with proper grammar ***
*** Synthesize info from ALL search results for completeness ***
"""

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
    messages = []


def GoogleSearch(query: str) -> str:
    """Perform a Google search using SerpAPI and format results."""
    try:
        params = {
            "q": query,
            "api_key": SerpAPIKey,
            "num": 5
        }
        search = SerpAPISearch(params)
        results = search.get_dict()
        
        organic_results = results.get("organic_results", [])
        
        if not organic_results:
            return f"REAL-TIME SEARCH RESULTS for '{query}':\n[start]\nNo results found.\n[end]"
        
        out = [f"REAL-TIME SEARCH RESULTS for '{query}':", "[start]"]
        
        for idx, r in enumerate(organic_results[:5], 1):
            title = r.get("title", "").strip()
            snippet = r.get("snippet", "").strip()
            link = r.get("link", "").strip()
            out.append(f"\nResult {idx}:\nTitle: {title}\nDescription: {snippet}\nURL: {link}")
        
        out.append("[end]\nProvide a concise, synthesized answer using only these results.")
        return "\n".join(out)
    except Exception as e:
        return f"REAL-TIME SEARCH RESULTS for '{query}':\n[start]\nError fetching results: {e}\n[end]"


def Information() -> str:
    """Return current datetime info."""
    now = datetime.datetime.now()
    return (
        "Real-time info:\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')}:{now.strftime('%M')}:{now.strftime('%S')}\n"
    )


def AnswerModifier(answer: str) -> str:
    lines = answer.splitlines()
    cleaned = [ln.rstrip() for ln in lines if ln.strip()]
    return "\n".join(cleaned)


def RealtimeSearchEngine(prompt: str) -> str:
    """Run Google search, pass results plus history to Groq model, return formatted answer."""
    global messages

    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
    except:
        messages = []

    messages.append({"role": "user", "content": prompt})

    search_results = GoogleSearch(prompt)

    current_system = SystemChatBot + [
        {"role": "system", "content": search_results},
        {"role": "system", "content": Information()}
    ]

    full_messages = current_system + messages

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=full_messages,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        stream=True
    )

    answer_chunks = []
    for chunk in completion:
        delta = getattr(chunk.choices[0].delta, "content", None)
        if delta:
            answer_chunks.append(delta)

    raw_answer = "".join(answer_chunks).strip().replace("</s>", "")
    final_answer = AnswerModifier(raw_answer)

    messages.append({"role": "assistant", "content": final_answer})
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    return final_answer


if __name__ == "__main__":
    while True:
        q = input("Enter your query (type exit to quit): ").strip()
        if q.lower() == "exit":
            break
        print(RealtimeSearchEngine(q))