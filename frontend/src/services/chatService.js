import client from "../api/client";

export async function sendMessage({ message, history = [], agent = null, sessionId = null }) {
  const { data } = await client.post("/api/chat", {
    message,
    history,
    agent,
    session_id: sessionId,
  });
  return data;
}
