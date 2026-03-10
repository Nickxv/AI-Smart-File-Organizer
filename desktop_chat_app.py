import tkinter as tk
from tkinter import scrolledtext

from ai_assistant import AssistantEngine


class DesktopChatApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Local AI Assistant")
        self.root.geometry("800x600")

        self.engine = AssistantEngine()

        self.chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="disabled")
        self.chat_box.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

        self.user_input = tk.Entry(self.input_frame)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.send_message)

        send_btn = tk.Button(self.input_frame, text="Send", command=self.send_message)
        send_btn.pack(side=tk.LEFT, padx=(8, 0))

        clear_btn = tk.Button(self.input_frame, text="Clear", command=self.clear_chat)
        clear_btn.pack(side=tk.LEFT, padx=(8, 0))

        self._append("Assistant", "Hello! Ask for coding help, summaries, plans, or debugging guidance.")

    def _append(self, speaker: str, text: str) -> None:
        self.chat_box.configure(state="normal")
        self.chat_box.insert(tk.END, f"{speaker}: {text}\n\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.see(tk.END)

    def send_message(self, event=None) -> None:
        prompt = self.user_input.get().strip()
        if not prompt:
            return

        self._append("You", prompt)
        self.user_input.delete(0, tk.END)

        reply = self.engine.ask(prompt)
        self._append("Assistant", reply)

    def clear_chat(self) -> None:
        self.engine.clear()
        self.chat_box.configure(state="normal")
        self.chat_box.delete("1.0", tk.END)
        self.chat_box.configure(state="disabled")
        self._append("Assistant", "Chat cleared. Start a new question.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopChatApp(root)
    root.mainloop()
