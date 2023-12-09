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
import { TooltipProvider } from "@/components/ui/tooltip";
import { toast } from "@/components/ui/use-toast";
import { zodResolver } from "@hookform/resolvers/zod";
import {
	Tooltip,
	TooltipContent,
	TooltipTrigger,
} from "@radix-ui/react-tooltip";
import { Eye, EyeOff } from "lucide-react";
import { useRef, useState } from "react";
import { useForm } from "react-hook-form";
import * as z from "zod";

const signUpFormSchema = z
	.object({
		firstName: z.string({
			required_error: "Please enter your first name",
		}),
		lastName: z.string({
			required_error: "Please enter your last name",
		}),
		email: z
			.string({
				required_error: "Please enter your email",
			})
			.email(),
		phone: z
			.string()
			.regex(/^0\d{9}$/, "Invalid phone number")
			.optional(),
		password: z
			.string({ required_error: "Please enter a password" })
			.min(8, "Password must be at least 8 characters"),
	})
	.required({ email: true, firstName: true, lastName: true, password: true });

type SignUpFormValues = z.infer<typeof signUpFormSchema>;

export default function SignUpForm() {
	const [passwordVisible, toggleVisibility] = useState<boolean>(false);
	const passwordRef = useRef<HTMLInputElement>(null);
	const [passwordStrength, setPasswordStrength] = useState<{
		value: number;
		color?: string;
	}>({ value: 0 });

	const form = useForm<SignUpFormValues>({
		resolver: zodResolver(signUpFormSchema),
		defaultValues: {
			firstName: "",
			lastName: "",
			email: "",
			phone: "",
			password: "",
		},
		mode: "onChange",
	});

	const onSubmit = (data: SignUpFormValues): void => {
		toast({
			title: "Submitted data",
			description: (
				<pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
					<code className="text-white">
						{JSON.stringify(data, null, 2)}
					</code>
					~{" "}
				</pre>
			),
		});
		{
			JSON.stringify(data, null, 2);
		}
		console.log(JSON.stringify(data, null, 2));
	};

	const checkPassword = (password: string) => {
		let strength = 0;
		let colors = ["#ff0000", "#ff6600", "#ffcc00", "#ccff00", "#00ff00"];

		if (password.match(/(?=.*\d)+/)) {
			// check for a number from 0-9
			strength += 1;
		}
		if (password.match(/(?=.*[a-z])(?=.*[A-Z])+/)) {
			// lower case from a-z, upper case from A-Z
			strength += 1;
		}
		if (password.match(/(?=.*[!@#$%^&*()~<>?])+/)) {
			// check for special character
			strength += 1;
		}
		if (password.length > 8) {
			// check for at least 10 characters
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
			<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
				<FormField
					control={form.control}
					name="firstName"
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
					name="lastName"
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
												className="text-white font-bold bg-black rounded-full w-6"
											>
												?
											</TooltipTrigger>
											<TooltipContent className="w-72 bg-black/75 rounded text-white p-4">
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
								<div className="flex items-center">
									<Input
										{...field}
										type={
											passwordVisible
												? "text"
												: "password"
										}
										ref={passwordRef}
										autoComplete="current-password"
										onInput={() => {
											if (passwordRef.current) {
												checkPassword(
													passwordRef.current.value
												);
											}
										}}
									/>
									<TooltipProvider>
										<Tooltip>
											<TooltipTrigger
												type="button"
												className="px-2 py-1 -ml-10"
												onClick={() =>
													toggleVisibility(
														(prev) => !prev
													)
												}
											>
												{passwordVisible ? (
													<EyeOff />
												) : (
													<Eye />
												)}
											</TooltipTrigger>
											<TooltipContent>
												{passwordVisible
													? "Hide password"
													: "Show password"}
											</TooltipContent>
										</Tooltip>
									</TooltipProvider>
								</div>
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
				<Button type="submit">Create Account</Button>
			</form>
		</Form>
	);
}
