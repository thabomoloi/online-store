import React from "react";
import ReactDOM from "react-dom/client";
import SignUpForm from "./components/forms/auth/SignUpForm";
import "./styles/index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
	<React.StrictMode>
		<SignUpForm />
	</React.StrictMode>
);
