import React from "react";
import ReactDOM from "react-dom/client";
import RegisterForm from "./components/forms/auth/register-form";
import "./styles/index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
	<React.StrictMode>
		<RegisterForm />
	</React.StrictMode>
);
