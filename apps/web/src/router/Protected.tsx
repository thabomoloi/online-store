import { useAuth } from "@/context/auth";
import React from "react";

export default function Protected({ children }: React.PropsWithChildren) {
	const auth = useAuth();

	return (
		<div>
			{auth.isLoggedIn && children}
			{!auth.isLoggedIn && <p>You need to login to access this page.</p>}
		</div>
	);
}
