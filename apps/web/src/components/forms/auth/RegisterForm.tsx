import {
	FormControl,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { toast } from "@/components/ui/use-toast";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form, useForm } from "react-hook-form";
import * as z from "zod";

const signUpFormSchema = z.object({
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
		.regex(/^0\d{9}z$/, "Invalid phone number")
		.optional(),
	password: z
		.string({ required_error: "Please enter a password" })
		.min(8, "Password must be at least 8 characters")
		.max(32, "Password must not be longer than 32 characters")
		.regex(/[0-9]/g, "At least 1 number is required")
		.regex(/[a-z]/g, "At least 1 lowercase letter is required")
		.regex(/[A-Z]/g, "At least 1 uppercase letter is required")
		.regex(
			/[\!\@\#\$\%\^\&\*]/g,
			"You need one of the required special characters"
		),
});

type SignUpFormValues = z.infer<typeof signUpFormSchema>;

export default function SignUpForm() {
	const form = useForm<SignUpFormValues>({
		resolver: zodResolver(signUpFormSchema),
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
				</pre>
			),
		});
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
								<Input {...field} />
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
								<Input {...field} type="tel" />
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
								<Input {...field} type="password" />
							</FormControl>
							<FormMessage />
						</FormItem>
					)}
				/>
			</form>
		</Form>
	);
}
