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
			<div className="flex-grow p-4">
				<Card className="max-w-md mx-auto">
					<CardHeader>
						<h1 className="text-2xl text-center">Welcome Back!</h1>
					</CardHeader>
					<CardContent>
						<LoginForm />
					</CardContent>
				</Card>
			</div>
		</div>
	);
}
