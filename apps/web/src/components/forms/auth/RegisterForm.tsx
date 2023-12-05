// import { Button } from "@/components/ui/button";
// import {
// 	Card,
// 	CardContent,
// 	CardDescription,
// 	CardFooter,
// 	CardHeader,
// 	CardTitle,
// } from "@/components/ui/card";
// import { Input } from "@/components/ui/input";
// import { Label } from "@/components/ui/label";

// import * as z from "zod";
// import { useForm } from "react-hook-form";
// import { zodResolver } from "@hookform/resolvers/zod";
// import {
// 	Form,
// 	FormField,
// 	FormItem,
// 	FormLabel,
// 	FormMessage,
// } from "@/components/ui/form";

// type RegisterFormProps = {
// 	handleSubmit: (user: User) => Response;
// };

// const FormSchema = z.object({
// 	firstName: z.string({
// 		required_error: "Please enter your first name",
// 	}),
// 	lastName: z.string({
// 		required_error: "Please enter your last name",
// 	}),
// 	email: z.string({
// 		required_error: "Please enter your email",
// 	}),
// 	password: z
// 		.string({ required_error: "Please enter a password" })
// 		.min(8, "Password must be at least 8 characters")
// 		.regex(/[0-9]/g, "At least 1 number is required")
// 		.regex(/[a-z]/g, "At least 1 lowercase letter is required")
// 		.regex(/[A-Z]/g, "At least 1 uppercase letter is required")
// 		.regex(
// 			/[\!\@\#\$\%\^\&\*]/g,
// 			"You need one of the required special characters"
// 		),
// });

// export function RegisterForm(): JSX.Element {
// 	const form = useForm<z.infer<typeof FormSchema>>({
// 		resolver: zodResolver(FormSchema),
// 		defaultValues: {
// 			firstName: "",
// 			lastName: "",
// 			email: "",
// 			password: "",
// 		},
// 	});

// 	const onSubmit = (data: z.infer<typeof FormSchema>) => {
// 		console.log(data);
// 	};
// 	return (
// 		<Card>
// 			<CardHeader className="space-y-1">
// 				<CardTitle className="text-2xl">Create an account</CardTitle>
// 				<CardDescription>
// 					Enter your details below to create your account
// 				</CardDescription>
// 			</CardHeader>
// 			<CardContent className="grid gap-4">
// 				<Form {...form}>
// 					<form onSubmit={form.handleSubmit(onSubmit)}>
// 						<FormField
// 							control={form.control}
// 							name="firstName"
// 							render={({ field }) => (
// 								<FormItem>
// 									<FormLabel>First Name</FormLabel>
// 									<Input {...field} />
// 									<FormMessage />
// 								</FormItem>
// 							)}
// 						/>
// 						{/* <div className="grid gap-2">
// 							<Label htmlFor="firstName">First Name</Label>
// 							<Input id="firstName" type="text" required />
// 						</div>
// 						<div className="grid gap-2">
// 							<Label htmlFor="lastName">Last Name</Label>
// 							<Input id="lastName" type="text" required />
// 						</div>
// 						<div className="grid gap-2">
// 							<Label htmlFor="email">Email</Label>
// 							<Input
// 								id="email"
// 								type="email"
// 								placeholder="name@example.com"
// 								required
// 							/>
// 						</div>
// 						<div className="grid gap-2">
// 							<Label htmlFor="phone">
// 								Phone{" "}
// 								<span className="text-gray-700">
// 									(optional)
// 								</span>
// 							</Label>
// 							<Input
// 								id="phone"
// 								type="tel"
// 								placeholder="0123456789"
// 							/>
// 						</div>
// 						<div className="grid gap-2">
// 							<Label htmlFor="password">Password</Label>
// 							<PasswordInput
// 								value=""
// 								handleChange={(value) => {}}
// 							/>
// 						</div> */}
// 						<Button
// 							className="w-full"
// 							type="submit"
// 							onClick={() => alert("hello")}
// 						>
// 							Create account
// 						</Button>
// 					</form>
// 				</Form>
// 			</CardContent>
// 		</Card>
// 	);
// }

// export default RegisterForm;

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
			<form></form>
		</Form>
	);
}
