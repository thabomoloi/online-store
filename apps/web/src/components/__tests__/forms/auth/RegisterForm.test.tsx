// import React from "react";
// import { render, fireEvent, screen } from "@testing-library/react";
// import RegisterForm from "./RegisterForm";

// describe("RegisterForm component", () => {
//   it("renders correctly", () => {
//     render(<RegisterForm />);

//     // Check if the form is rendered
//     const formElement = screen.getByRole("form");
//     expect(formElement).toBeInTheDocument();

//     // Check if card title and description are rendered
//     const cardTitle = screen.getByText("Create an account");
//     const cardDescription = screen.getByText(
//       "Enter your details below to create your account"
//     );
//     expect(cardTitle).toBeInTheDocument();
//     expect(cardDescription).toBeInTheDocument();

//     // Check if input fields and labels are rendered
//     const firstNameLabel = screen.getByText("First Name");
//     const lastNameLabel = screen.getByText("Last Name");
//     const emailLabel = screen.getByText("Email");
//     const phoneLabel = screen.getByText("Phone");
//     const passwordLabel = screen.getByText("Password");
//     const confirmPasswordLabel = screen.getByText("Confirm Password");

//     expect(firstNameLabel).toBeInTheDocument();
//     expect(lastNameLabel).toBeInTheDocument();
//     expect(emailLabel).toBeInTheDocument();
//     expect(phoneLabel).toBeInTheDocument();
//     expect(passwordLabel).toBeInTheDocument();
//     expect(confirmPasswordLabel).toBeInTheDocument();

//     const firstNameInput = screen.getByLabelText("First Name");
//     const lastNameInput = screen.getByLabelText("Last Name");
//     const emailInput = screen.getByLabelText("Email");
//     const phoneInput = screen.getByLabelText("Phone");
//     const passwordInput = screen.getByLabelText("Password");
//     const confirmPasswordInput = screen.getByLabelText("Confirm Password");

//     expect(firstNameInput).toBeInTheDocument();
//     expect(lastNameInput).toBeInTheDocument();
//     expect(emailInput).toBeInTheDocument();
//     expect(phoneInput).toBeInTheDocument();
//     expect(passwordInput).toBeInTheDocument();
//     expect(confirmPasswordInput).toBeInTheDocument();

//     // Check if the "Create account" button is rendered
//     const createAccountButton = screen.getByText("Create account");
//     expect(createAccountButton).toBeInTheDocument();
//   });

//   it("submits the form with correct data when 'Create account' button is clicked", () => {
//     const handleSubmitMock = jest.fn();
//     render(<RegisterForm handleSubmit={handleSubmitMock} />);

//     // Fill in the form fields
//     fireEvent.change(screen.getByLabelText("First Name"), {
//       target: { value: "John" },
//     });
//     fireEvent.change(screen.getByLabelText("Last Name"), {
//       target: { value: "Doe" },
//     });
//     fireEvent.change(screen.getByLabelText("Email"), {
//       target: { value: "john.doe@example.com" },
//     });
//     fireEvent.change(screen.getByLabelText("Phone"), {
//       target: { value: "1234567890" },
//     });
//     fireEvent.change(screen.getByLabelText("Password"), {
//       target: { value: "password123" },
//     });
//     fireEvent.change(screen.getByLabelText("Confirm Password"), {
//       target: { value: "password123" },
//     });

//     // Click the "Create account" button
//     fireEvent.click(screen.getByText("Create account"));

//     // Check if handleSubmit function is called with the correct user data
//     expect(handleSubmitMock).toHaveBeenCalledWith({
//       firstName: "John",
//       lastName: "Doe",
//       email: "john.doe@example.com",
//       phone: "1234567890",
//       password: "password123",
//     });
//   });
// });
