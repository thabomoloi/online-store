import React from "react";
import ReactDOM from "react-dom/client";
import "./styles/index.css";
import { AuthProvider } from "./context/auth";
import { Toaster } from "./components/ui/toaster";
import LoginForm from "./components/forms/auth/LoginForm";
import SignUpForm from "./components/forms/auth/SignUpForm";

ReactDOM.createRoot(document.getElementById("root")!).render(
	<React.StrictMode>
		<AuthProvider>
			<LoginForm />
			<SignUpForm />
			<Toaster />
		</AuthProvider>
	</React.StrictMode>
);
