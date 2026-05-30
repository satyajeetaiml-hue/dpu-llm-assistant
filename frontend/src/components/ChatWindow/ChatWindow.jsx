import { useEffect, useRef, useState } from "react";
import "./ChatWindow.css";

export default function ChatWindow({ messages, loading, error, onSend }) {
  const [input, setInput] = useState("");
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;
    onSend(text);
    setInput("");
  };

  return (
    <div className="chat-window">
      <div className="chat-messages">
        {messages.length === 0 && (
          <p className="chat-empty">Ask about admissions, courses, policies, or events.</p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`chat-bubble ${m.role}`}>
            {m.agent && m.role === "assistant" && (
              <span className="chat-agent-tag">{m.agent}</span>
            )}
            <p>{m.content}</p>
            {m.citations?.length > 0 && (
              <ul className="chat-citations">
                {m.citations.map((c) => (
                  <li key={c.index}>
                    [{c.index}] {c.source} (p.{c.page})
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
        {loading && <div className="chat-bubble assistant">Thinking…</div>}
        {error && <div className="chat-error">{error}</div>}
        <div ref={endRef} />
      </div>

      <form className="chat-input" onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question…"
        />
        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
    </div>
  );
}
