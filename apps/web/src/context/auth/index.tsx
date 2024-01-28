import React, { createContext, useContext, useEffect, useState } from "react";
import Authentication from "./auth";
import { toast } from "@/components/ui/use-toast";

type Token = string | null;

interface Auth {
	isLoggedIn: boolean;
	logout: () => Promise<void>;
	login: (details: LoginDetails) => Promise<void>;
	register: (details: SignUpDetails) => Promise<void>;
}

export const AuthContext = createContext<Auth>({
	isLoggedIn: false,
	login: () => Promise.resolve(),
	logout: () => Promise.resolve(),
	register: () => Promise.resolve(),
});

export function AuthProvider({ children }: React.PropsWithChildren) {
	const [accessToken, setAccessToken] = useState<Token>(
		localStorage.getItem("access_token")
	);
	const [refreshToken, setRefreshToken] = useState<Token>(
		localStorage.getItem("refresh_token")
	);
	const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

	useEffect(() => {
		if (accessToken && refreshToken) {
			Authentication.isAuth(accessToken)
				.then((is_auth) => setIsLoggedIn(is_auth))
				.catch(() => setIsLoggedIn(false));
		} else {
			setIsLoggedIn(false);
		}
	}, [accessToken, refreshToken]);

	useEffect(() => {
		if (isLoggedIn && accessToken && refreshToken) {
			localStorage.setItem("access_token", accessToken);
			localStorage.setItem("refresh_token", refreshToken);
		} else {
			localStorage.removeItem("access_token");
			localStorage.removeItem("refresh_token");
		}
		const tokenRefreshInterval = setInterval(async () => {
			const tokenData = jwt_decode(accessToken);
			const currentTime = Math.floor(Date.now() / 1000);
			// check if token expires in 300s (5min)
			if (tokenData.exp - currentTime < 300) {
				const responseData = await Authentication.refreshAccessToken(
					refreshToken
				);
				if (responseData.code === 200) {
					setAccessToken(responseData.data.access_token);
				}
			}
		}, 60000);
		console.log(isLoggedIn);

		if (!isLoggedIn) return () => clearInterval(tokenRefreshInterval);
	}, [isLoggedIn, accessToken, refreshToken]);

	const login = async (details: LoginDetails) => {
		const responseData = await Authentication.login(details);
		if (responseData.code >= 400) {
			toast({
				description: <p>{responseData.message}</p>,
				className: "bg-destructive text-destructive-foreground",
			});
		} else if (responseData.code === 200) {
			toast({
				description: <p>{responseData.message}</p>,
			});
			setAccessToken(responseData.data.access_token);
			setRefreshToken(responseData.data.refresh_token);
		}
	};

	const register = async (details: SignUpDetails) => {
		const responseData = await Authentication.register(details);
		if (responseData.code >= 400) {
			toast({
				description: <p>{responseData.message}</p>,
				className: "bg-destructive text-destructive-foreground",
			});
		} else if (responseData.code === 201) {
			toast({
				description: <p>{responseData.message}</p>,
			});
		}
	};

	const logout = async () => {
		const responseData = await Authentication.logout(accessToken);
		if (responseData.code >= 400) {
			toast({
				description: <p>{responseData.message}</p>,
				className: "bg-destructive text-destructive-foreground",
			});
		} else {
			setRefreshToken(null);
			setAccessToken(null);
		}
	};

	return (
		<AuthContext.Provider value={{ isLoggedIn, login, logout, register }}>
			{children}
		</AuthContext.Provider>
	);
}

export function useAuth(): Auth {
	const context = useContext(AuthContext);
	if (context === undefined) {
		throw new Error("useAuth must be used within an AuthProvider");
	}
	return context;
}
function jwt_decode(accessToken: Token): { exp: number } {
	console.log(accessToken);
	//throw new Error("Function not implemented.");
	return {
		exp: Date.now() / 1000 + 120,
	};
}
