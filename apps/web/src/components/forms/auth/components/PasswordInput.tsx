import { Input } from "@/components/ui/input";
import { Eye, EyeOff } from "lucide-react";

import { useRef, useState } from "react";
type PasswordInputProps = {
	value: string;
	handleChange: (value: string) => void;
};

export function PasswordInput({
	value = "",
	handleChange,
}: PasswordInputProps) {
	const [passwordVisible, toggleVisibility] = useState<boolean>(false);
	const passwordRef = useRef<HTMLInputElement>(null);
	const reqListRef = useRef<HTMLUListElement>(null);
	const requirementElements = [
		"At least 8 characters long (and less than 100 characters)",
		"Contains at least 1 number",
		"Contains at least 1 lowercase letter",
		"Contains at least 1 uppercase letter",
		"Contains a special character (e.g. !@#$%^&*()_+)",
	].map((requirement) => ({
		text: requirement,
		ref: useRef<HTMLLIElement>(null),
	}));

	return (
		<>
			<div className="flex items-center">
				<Input
					id="password"
					type={passwordVisible ? "text" : "password"}
					maxLength={100}
					minLength={8}
					required
					ref={passwordRef}
					value={value}
					onChange={(event) => handleChange(event.target.value)}
					pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+]{8,100}$"
				/>
				<button
					className="px-2 py-1 -ml-10"
					type="button"
					onClick={() => toggleVisibility((prev) => !prev)}
				>
					{passwordVisible ? <EyeOff /> : <Eye />}
				</button>
			</div>
			<ul className="inputRequirements" ref={reqListRef}>
				{requirementElements.map((requirement, index) => (
					<li key={index} ref={requirement.ref}>
						{requirement.text}
					</li>
				))}
			</ul>
		</>
	);
}
