import {
	ApiIsAuthResponse,
	ApiResponse,
	ApiTokenResponse,
} from "@/types/api-response";

const AUTH_URL = import.meta.env.VITE_AUTH_URL;

class Authentication {
	static readonly IS_AUTH_URL = `${AUTH_URL}/is-authenticated`;
	static readonly LOGIN_URL = `${AUTH_URL}/login`;
	static readonly LOGOUT_URL = `${AUTH_URL}/logout`;
	static readonly SIGNUP_URL = `${AUTH_URL}/signup`;

	public static async register(data: SignUpDetails) {
		const response = await fetch(this.SIGNUP_URL, {
			method: "post",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ ...data }),
		});
		const responseData = (await response.json()) as ApiResponse;
		return responseData;
	}

	public static async login(data: LoginDetails) {
		const response = await fetch(this.LOGIN_URL, {
			method: "post",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ ...data }),
		});
		const responseData = (await response.json()) as ApiTokenResponse;
		return responseData;
	}

	public static async isAuth(access_token: string | null = null) {
		const response = await fetch(this.IS_AUTH_URL, {
			headers: {
				Authorization: `Bearer ${access_token}`,
			},
		});
		const responseData = (await response.json()) as ApiIsAuthResponse;
		return responseData.data.is_authenticated;
	}

	public static async logout(access_token: string | null = null) {
		const response = await fetch(this.LOGOUT_URL, {
			method: "delete",
			headers: {
				Authorization: `Bearer ${access_token}`,
			},
		});
		const responseData = (await response.json()) as ApiResponse;
		return responseData;
	}
}

export default Authentication;
