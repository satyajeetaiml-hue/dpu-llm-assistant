import ChatWindow from "../../components/ChatWindow/ChatWindow";
import { useChat } from "../../hooks/useChat";

export default function Chatbot() {
  const { messages, loading, error, send } = useChat();
  return (
    <ChatWindow messages={messages} loading={loading} error={error} onSend={send} />
  );
}
