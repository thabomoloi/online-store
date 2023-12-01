import { Button } from "@/components/ui/button";
import {
	Card,
	CardContent,
	CardDescription,
	CardFooter,
	CardHeader,
	CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type RegisterFormProps = {
	handleSubmit: (user: User) => Response;
};

export function RegisterForm(): JSX.Element {
	return (
		<form>
			<Card>
				<CardHeader className="space-y-1">
					<CardTitle className="text-2xl">
						Create an account
					</CardTitle>
					<CardDescription>
						Enter your details below to create your account
					</CardDescription>
				</CardHeader>
				<CardContent className="grid gap-4">
					<div className="grid gap-2">
						<Label htmlFor="firstName">First Name</Label>
						<Input id="firstName" type="text" required />
					</div>
					<div className="grid gap-2">
						<Label htmlFor="lastName">Last Name</Label>
						<Input id="lastName" type="text" required />
					</div>
					<div className="grid gap-2">
						<Label htmlFor="email">Email</Label>
						<Input
							id="email"
							type="email"
							placeholder="name@example.com"
							required
						/>
					</div>
					<div className="grid gap-2">
						<Label htmlFor="phone">
							Phone{" "}
							<span className="text-gray-700">(optional)</span>
						</Label>
						<Input id="phone" type="tel" placeholder="0123456789" />
					</div>
					<div className="grid gap-2">
						<Label htmlFor="password">Password</Label>
						<Input id="password" type="password" required />
					</div>
					<div className="grid gap-2">
						<Label htmlFor="password">Confirm Password</Label>
						<Input id="password" type="password" required />
					</div>
				</CardContent>
				<CardFooter>
					<Button className="w-full">Create account</Button>
				</CardFooter>
			</Card>
		</form>
	);
}

export default RegisterForm;
