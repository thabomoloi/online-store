import { Input } from "@/components/ui/input";
import {
	Tooltip,
	TooltipContent,
	TooltipProvider,
	TooltipTrigger,
} from "@/components/ui/tooltip";
import { Eye, EyeOff } from "lucide-react";
import { useRef, useState } from "react";

interface PasswordInputProps {
	field?: object;
	checkPassword?: (password: string) => void;
}
export default function PasswordInput({
	field,
	checkPassword,
}: PasswordInputProps): JSX.Element {
	const [visible, toggleVisibility] = useState<boolean>(false);
	const passwordRef = useRef<HTMLInputElement>(null);

	const handleInput = () => {
		if (passwordRef.current && checkPassword)
			checkPassword(passwordRef.current.value);
	};

	return (
		<div className="flex items-center">
			<Input
				{...field}
				ref={passwordRef}
				type={visible ? "text" : "password"}
				autoComplete="current-password"
				onInput={handleInput}
			/>
			<TooltipProvider>
				<Tooltip>
					<TooltipTrigger
						type="button"
						className="px-2 py-1 -ml-10 text-gray-500"
						onClick={() => toggleVisibility((prev) => !prev)}
					>
						{visible ? <EyeOff /> : <Eye />}
					</TooltipTrigger>
					<TooltipContent>{visible ? "Hide" : "Show"}</TooltipContent>
				</Tooltip>
			</TooltipProvider>
		</div>
	);
}
