import { Button } from "@/components/ui/button";
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import {
	TooltipProvider,
	Tooltip,
	TooltipContent,
	TooltipTrigger,
} from "@/components/ui/tooltip";
import { useAuth } from "@/context/auth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import * as z from "zod";
import PasswordInput from "./components/PasswordInput";

const signUpFormSchema = z
	.object({
		first_name: z.string().min(1, { message: "First name is required" }),
		last_name: z.string().min(1, { message: "Last name is required" }),
		email: z
			.string()
			.min(1, { message: "Email is required" })
			.email("Invalid email address"),
		phone: z.string().optional(),
		password: z
			.string({ required_error: "Please enter a password" })
			.min(8, "Password must be at least 8 characters"),
	})
	.refine(
		(data) => {
			const regExp = /^0\d{9}$/;
			if (data.phone) return regExp.test(data.phone);
			return true;
		},
		{ path: ["phone"], message: "Invalid phone number" }
	);

type SignUpFormValues = z.infer<typeof signUpFormSchema>;

export default function SignUpForm() {
	const auth = useAuth();
	const [passwordStrength, setPasswordStrength] = useState<{
		value: number;
		color?: string;
	}>({ value: 0 });

	const form = useForm<SignUpFormValues>({
		resolver: zodResolver(signUpFormSchema),
		defaultValues: {
			first_name: "",
			last_name: "",
			email: "",
			phone: "",
			password: "",
		},
	});

	const onSubmit = async (data: SignUpFormValues): Promise<void> => {
		auth.register(data);
	};

	const checkPassword = (password: string) => {
		let strength = 0;
		let colors = ["#ff0000", "#ff6600", "#ffcc00", "#ccff00", "#00ff00"];

		if (password.match(/(?=.*\d)+/)) {
			strength += 1;
		}
		if (password.match(/(?=.*[a-z])(?=.*[A-Z])+/)) {
			strength += 1;
		}
		if (password.match(/(?=.*[!@#$%^&*()~<>?])+/)) {
			strength += 1;
		}
		if (password.length > 8) {
			strength += 1;
		}

		if (password.trim() !== "") {
			setPasswordStrength({
				value: strength * 20 + 20,
				color: colors[strength],
			});
		} else {
			setPasswordStrength({ value: 0 });
		}
	};

	return (
		<Form {...form}>
			<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
				<FormField
					control={form.control}
					name="first_name"
					render={({ field }) => (
						<FormItem>
							<FormLabel>First Name</FormLabel>
							<FormControl>
								<Input {...field} />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<FormField
					control={form.control}
					name="last_name"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Last Name</FormLabel>
							<FormControl>
								<Input {...field} />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<FormField
					control={form.control}
					name="email"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Email</FormLabel>
							<FormControl>
								<Input {...field} autoComplete="email" />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<FormField
					control={form.control}
					name="phone"
					render={({ field }) => (
						<FormItem>
							<FormLabel>Phone Number (optional)</FormLabel>
							<FormControl>
								<Input
									{...field}
									type="tel"
									placeholder="0712345678"
								/>
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
							<div className="flex items-center gap-4 justify-between">
								<FormLabel>Password</FormLabel>
								<div className="flex flex-nowrap gap-2 items-center">
									<Progress
										value={passwordStrength.value}
										color={passwordStrength.color}
										className="w-48"
									/>
									<TooltipProvider>
										<Tooltip>
											<TooltipTrigger
												type="button"
												className="text-white font-bold bg-primary rounded-full w-6"
											>
												?
											</TooltipTrigger>
											<TooltipContent className="w-60">
												It is recommended to use a mix
												of lowercase and uppercase
												letters, numbers and special
												symbols for a stronger password.
											</TooltipContent>
										</Tooltip>
									</TooltipProvider>
								</div>
							</div>

							<FormControl>
								<PasswordInput
									field={field}
									checkPassword={checkPassword}
								/>
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<div>
					<Button type="submit" className="mt-6 w-full">
						Create Account
					</Button>
				</div>
			</form>
		</Form>
	);
}
