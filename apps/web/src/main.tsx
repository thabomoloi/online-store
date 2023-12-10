import React from "react";
import ReactDOM from "react-dom/client";
import SignUpForm from "./components/forms/auth/SignUpForm";
import "./styles/index.css";
import { AuthProvider } from "./context/auth";
import { Toaster } from "./components/ui/toaster";

ReactDOM.createRoot(document.getElementById("root")!).render(
	<React.StrictMode>
		<AuthProvider>
			<SignUpForm />
			<Toaster />
		</AuthProvider>
	</React.StrictMode>
);
