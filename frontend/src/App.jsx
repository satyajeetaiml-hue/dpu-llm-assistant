import { Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar/Sidebar";
import Chatbot from "./pages/Chatbot/Chatbot";
import AdmissionAnalytics from "./pages/AdmissionAnalytics/AdmissionAnalytics";
import Compliance from "./pages/Compliance/Compliance";
import Admin from "./pages/Admin/Admin";

export default function App() {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="content">
        <Routes>
          <Route path="/" element={<Navigate to="/chat" replace />} />
          <Route path="/chat" element={<Chatbot />} />
          <Route path="/analytics" element={<AdmissionAnalytics />} />
          <Route path="/compliance" element={<Compliance />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </main>
    </div>
  );
}
