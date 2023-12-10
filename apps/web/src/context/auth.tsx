import React, { createContext, useContext, useEffect, useState } from "react";

const AUTH_URL = import.meta.env.VITE_AUTH_URL;

type Token = string | null;
type Tokens = {
	jwt_access_token: Token;
	jwt_refresh_token: Token;
};

type Auth = {
	isLoggedIn: boolean;
	logout: () => Promise<string>;
	login: (email: string, password: string) => Promise<string>;
	register: (user: SignUpDetails) => Promise<string>;
};

export const AuthContext = createContext<Auth>({
	isLoggedIn: false,
	login: () => Promise.resolve(""),
	logout: () => Promise.resolve(""),
	register: () => Promise.resolve(""),
});

export function AuthProvider({
	children,
}: React.PropsWithChildren): JSX.Element {
	const [accessToken, setAccessToken] = useState<Token>(
		localStorage.getItem("access_token")
	);
	const [refreshToken, setRefreshToken] = useState<Token>(
		localStorage.getItem("refresh_token")
	);
	const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

	useEffect(() => {
		if (accessToken && refreshToken) {
			fetch(`${AUTH_URL}/is-authenticated`, {
				method: "get",
				headers: {
					Authorization: `Bearer ${accessToken}`,
				},
			})
				.then((res) => res.json())
				.then((data: { is_authenticated: boolean }) =>
					setIsLoggedIn(data.is_authenticated)
				)
				.catch(() => setIsLoggedIn(false));
		} else {
			setIsLoggedIn(false);
		}
	}, []);

	useEffect(() => {
		if (!(accessToken && refreshToken)) {
			localStorage.removeItem("access_token");
			localStorage.removeItem("refresh_token");
		}
	}, [accessToken, refreshToken]);

	const removeTokens = () => {
		setRefreshToken(null);
		setAccessToken(null);
	};

	const login = async (email: string, password: string) => {
		const response = await fetch(`${AUTH_URL}/login`, {
			method: "post",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ email, password }),
		});
		if (response.status === 200) {
			const { tokens }: { tokens: Tokens } = await response.json();
			if (tokens.jwt_access_token && tokens.jwt_refresh_token) {
				localStorage.setItem("access_token", tokens.jwt_access_token);
				localStorage.setItem("refresh_token", tokens.jwt_refresh_token);
			}
		} else {
			removeTokens();
		}
		return (await response.json()).msg as string;
	};

	const register = async (user: SignUpDetails) => {
		const response = await fetch(`${AUTH_URL}/signup`, {
			method: "post",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ ...user }),
		});
		console.log(response.status);
		return (await response.json()).msg as string;
	};

	const logout = async () => {
		const response = await fetch(`${AUTH_URL}/logout`, {
			method: "post",
		});
		removeTokens();

		return (await response.json()).msg as string;
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
