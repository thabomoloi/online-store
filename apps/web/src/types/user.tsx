interface UserDetails {
	first_name: string;
	last_name: string;
	email: string;
	phone?: string;
}

interface User extends UserDetails {
	id?: string;
	password?: string;
}

interface LoginDetails {
	email: string;
	password: string;
}
interface SignUpDetails extends UserDetails {
	password: string;
}

interface LoginDetails {
	email: string;
	password: string;
}
