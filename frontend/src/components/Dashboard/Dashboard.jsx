import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

// Renders admission metrics as a grouped bar chart plus summary cards.
export default function Dashboard({ data }) {
  if (!data) return null;

  return (
    <div>
      <div style={{ display: "flex", gap: 16, marginBottom: 24 }}>
        <SummaryCard label="Total Applications" value={data.total_applications} />
        <SummaryCard label="Total Admitted" value={data.total_admitted} />
      </div>

      <div style={{ height: 360, background: "var(--panel)", borderRadius: 12, padding: 16 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data.metrics}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
            <XAxis dataKey="program" stroke="var(--muted)" />
            <YAxis stroke="var(--muted)" />
            <Tooltip
              contentStyle={{ background: "var(--bg)", border: "none", borderRadius: 8 }}
            />
            <Legend />
            <Bar dataKey="applications" fill="#6366f1" name="Applications" />
            <Bar dataKey="admitted" fill="#22d3ee" name="Admitted" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function SummaryCard({ label, value }) {
  return (
    <div style={{ background: "var(--panel)", padding: 20, borderRadius: 12, flex: 1 }}>
      <p style={{ color: "var(--muted)", margin: 0 }}>{label}</p>
      <p style={{ fontSize: "2rem", fontWeight: 700, margin: "8px 0 0" }}>{value}</p>
    </div>
  );
}
