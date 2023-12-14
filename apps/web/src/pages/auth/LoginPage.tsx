import LoginForm from "@/components/forms/auth/LoginForm";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export default function LoginPage() {
	return (
		<div
			className={cn(
				"fixed top-0 left-0 w-full h-full",
				"flex items-center justify-center",
				"bg-secondary"
			)}
		>
			<div className="flex-grow flex flex-col items-center p-4">
				<div className="w-full max-w-md space-y-4">
					<Card className="rounded-lg">
						<CardHeader>
							<h1 className="text-2xl text-center">
								Welcome Back!
							</h1>
						</CardHeader>
						<CardContent>
							<LoginForm />
						</CardContent>
					</Card>
					<div className="w-full bg-gray-300 p-4 rounded-lg text-center">
						<p className="text-gray-700">
							Don't have an account?&nbsp;
							<a href="#" className="text-primary font-semibold">
								Get Started
							</a>
						</p>
					</div>
				</div>
			</div>
		</div>
	);
}
