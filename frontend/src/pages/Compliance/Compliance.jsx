import ChatWindow from "../../components/ChatWindow/ChatWindow";
import { useChat } from "../../hooks/useChat";

// Compliance page reuses the chat UI but forces routing to the compliance agent.
export default function Compliance() {
  const { messages, loading, error, send } = useChat();
  return (
    <div>
      <h2>Compliance & CIQA Assistant</h2>
      <ChatWindow
        messages={messages}
        loading={loading}
        error={error}
        onSend={(text) => send(text, "compliance")}
      />
    </div>
  );
}
