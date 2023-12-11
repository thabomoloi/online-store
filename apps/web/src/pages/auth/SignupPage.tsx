import SignUpForm from "@/components/forms/auth/SignUpForm";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export default function SignupPage() {
	return (
		<div
			className={cn(
				"fixed top-0 left-0 w-full min-h-screen",
				"flex items-center justify-center",
				"bg-secondary overflow-y-auto"
			)}
		>
			<div className="flex-grow p-4 overflow-auto">
				<Card className="max-w-md mx-auto">
					<CardHeader>
						<h1 className="text-2xl text-center">New Account!</h1>
					</CardHeader>
					<CardContent>
						<SignUpForm />
					</CardContent>
				</Card>
			</div>
		</div>
	);
}
