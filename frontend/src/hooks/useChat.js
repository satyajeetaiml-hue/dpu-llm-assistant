import { useCallback, useState } from "react";
import { sendMessage } from "../services/chatService";

// Manages chat message state and the request lifecycle.
export function useChat() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const send = useCallback(
    async (text, agent = null) => {
      const userMsg = { role: "user", content: text };
      const history = messages.map((m) => ({ role: m.role, content: m.content }));
      setMessages((prev) => [...prev, userMsg]);
      setLoading(true);
      setError(null);
      try {
        const data = await sendMessage({ message: text, history, agent });
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: data.answer,
            agent: data.agent,
            citations: data.citations || [],
          },
        ]);
        return data;
      } catch (err) {
        setError(err?.response?.data?.detail || err.message);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [messages]
  );

  return { messages, loading, error, send };
}
