import React from "react";
import ReactDOM from "react-dom/client";
import "./styles/index.css";
import { AuthProvider } from "./context/auth";
import { Toaster } from "./components/ui/toaster";
import ShopPage from "./pages/ShopPage";

ReactDOM.createRoot(document.getElementById("root")!).render(
	<React.StrictMode>
		<AuthProvider>
			<ShopPage />
			<Toaster />
		</AuthProvider>
	</React.StrictMode>
);
