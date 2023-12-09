import { afterEach, expect } from "vitest";
import { cleanup } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import matchers from "@testing-library/jest-dom/types/matchers";

expect.extend(matchers)
// runs a cleanup after each test case (e.g. clearing jsdom)
afterEach(() => {
	cleanup();
});
