import { NavLink } from "react-router-dom";
import "./Sidebar.css";

const links = [
  { to: "/chat", label: "Chat Assistant" },
  { to: "/analytics", label: "Admission Analytics" },
  { to: "/compliance", label: "Compliance" },
  { to: "/admin", label: "Admin" },
];

export default function Sidebar() {
  return (
    <nav className="sidebar">
      <h1 className="sidebar-title">University AI</h1>
      <ul className="sidebar-links">
        {links.map((link) => (
          <li key={link.to}>
            <NavLink
              to={link.to}
              className={({ isActive }) =>
                isActive ? "sidebar-link active" : "sidebar-link"
              }
            >
              {link.label}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}
