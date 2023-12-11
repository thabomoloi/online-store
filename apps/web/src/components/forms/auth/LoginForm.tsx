import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/context/auth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import PasswordInput from "./components/PasswordInput";
import { Button } from "@/components/ui/button";

const schema = z.object({
	email: z
		.string()
		.min(1, { message: "Email is required" })
		.email("Invalid email address"),
	password: z.string().min(1, { message: "Password is required" }),
});

type LoginFormValues = z.infer<typeof schema>;

export default function LoginForm() {
	const auth = useAuth();

	const form = useForm<LoginFormValues>({
		resolver: zodResolver(schema),
		defaultValues: {
			email: "",
			password: "",
		},
	});

	const onSubmit = (data: LoginFormValues) => {
		auth.login(data);
	};

	return (
		<Form {...form}>
			<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
				<FormField
					control={form.control}
					name="email"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Email</FormLabel>
							<FormControl>
								<Input {...field} />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<FormField
					control={form.control}
					name="password"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Password</FormLabel>
							<FormControl>
								<PasswordInput field={field} />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<div>
					<Button type="submit" className="mt-6 w-full">
						Login
					</Button>
				</div>
			</form>
		</Form>
	);
}
