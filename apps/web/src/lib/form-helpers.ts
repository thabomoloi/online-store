type ValidityCheck = {
	isInvalid: (input: HTMLInputElement) => boolean;
	invalidityMessage: string;
	element?: Element | null;
};

interface CustomInputElement extends HTMLInputElement {
	customValidation: CustomInputValidation;
}

class CustomInputValidation {
	private _invalidities: string[] = [];
	public validityChecks: ValidityCheck[] = [];
	private _inputNode: CustomInputElement;

	constructor(input: CustomInputElement) {
		this._inputNode = input;
		this.registerListener();
	}

	private addInvalidity(message: string): void {
		this._invalidities.push(message);
	}

	public set invalidities(value: string[]) {
		this._invalidities = value;
	}

	public get invalidities(): string {
		return this._invalidities.join(". \n");
	}

	private checkValidity(): void {
		for (const validityCheck of this.validityChecks) {
			const isInvalid = validityCheck.isInvalid(this._inputNode);
			if (isInvalid) this.addInvalidity(validityCheck.invalidityMessage);

			const requirementElement = validityCheck.element;
			if (requirementElement) {
				const { classList } = requirementElement;
				if (isInvalid) {
					classList.add("invalid");
					classList.remove("valid");
				} else {
					classList.remove("invalid");
					classList.add("valid");
				}
			}
		}
	}

	private checkInput(): void {
		this._inputNode.customValidation.invalidities = [];
		this.checkValidity();

		if (
			this._inputNode.customValidation.invalidities.length == 0 &&
			this._inputNode.value !== ""
		) {
			this._inputNode.setCustomValidity("");
		} else {
			const message = this._inputNode.customValidation.invalidities;
			this._inputNode.setCustomValidity(message);
		}
	}

	private registerListener(): void {
		this._inputNode.addEventListener("keyup", () => {
			this.checkInput();
		});
	}
}

const getPasswordValidityChecks = (
	input: CustomInputElement
): ValidityCheck[] => {
	const ulElement = input.nextElementSibling as HTMLUListElement;
	console.log(ulElement);
	const requirementElements =
		ulElement.childNodes as NodeListOf<HTMLLIElement>;

	const validityChecks: ValidityCheck[] = [
		{
			isInvalid: (input) =>
				input.value.length < 8 || input.value.length > 100,
			invalidityMessage:
				"This input needs to be between 8 and 100 characters",
			element: requirementElements[0],
		},
		{
			isInvalid: (input) => !input.value.match(/[0-9]/g),
			invalidityMessage: "At least 1 number is required",
			element: requirementElements[1],
		},
		{
			isInvalid: (input) => !input.value.match(/[a-z]/g),
			invalidityMessage: "At least 1 lowercase letter is required",
			element: requirementElements[2],
		},
		{
			isInvalid: (input) => !input.value.match(/[A-Z]/g),
			invalidityMessage: "At least 1 uppercase letter is required",
			element: requirementElements[3],
		},
		{
			isInvalid: (input) => !input.value.match(/[\!\@\#\$\%\^\&\*]/g),
			invalidityMessage:
				"You need one of the required special characters",
			element: requirementElements[4],
		},
	];

	return validityChecks;
};
export const setUpRegistrationFormValidation = (
	passwordInput: CustomInputElement
): void => {
	passwordInput.customValidation = new CustomInputValidation(passwordInput);
	passwordInput.customValidation.validityChecks =
		getPasswordValidityChecks(passwordInput);
};

export type { CustomInputElement };
