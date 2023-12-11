export interface ApiResponse {
	code: number;
	description: string;
	message: string;
}

export interface ApiTokenResponse extends ApiResponse {
	data: {
		access_token: string | null;
		refresh_token: string | null;
	};
}

export interface ApiIsAuthResponse extends ApiResponse {
	data: {
		is_authenticated: boolean;
	};
}

export interface ApiProfileResponse extends ApiResponse {
	data: {
		name: string;
		email: string;
	};
}
