import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";

let count = 0;

function genId() {
	count = (count + 1) % Number.MAX_SAFE_INTEGER;
	return count.toString();
}

interface StarProps {
	fillPercent?: number;
	fillColor?: string;
	unfillColor?: string;
	onClick?: () => void;
	readonly?: boolean;
	className?: string;
}

function Star({
	fillPercent = 0,
	fillColor = "gold",
	unfillColor = "gray",
	onClick,
	readonly = true,
	className,
}: StarProps): JSX.Element {
	const gradientId = genId();
	return (
		<svg
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 24 24"
			fill="none"
			width="100%"
			height="100%"
			className={cn(className, !readonly && "cursor-pointer")}
			onClick={onClick}
		>
			{/* Define the linear gradient */}
			<defs>
				<linearGradient
					id={gradientId}
					x1="0%"
					y1="0%"
					x2="100%"
					y2="0%"
				>
					{/* Fill stops */}
					<stop
						offset={`${fillPercent}%`}
						style={{ stopColor: fillColor, stopOpacity: 1 }}
					/>
					<stop
						offset={`${fillPercent}%`}
						style={{ stopColor: unfillColor, stopOpacity: 1 }}
					/>
				</linearGradient>
			</defs>

			{/* Star path */}
			<path
				d="M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z"
				fill={`url(#${gradientId})`}
			/>
		</svg>
	);
}

interface RatingProps {
	rating: number;
	count: number;
	showCount?: boolean;
	readonly?: boolean;
	handleRate?: (value: number) => void;
}

function Rating({
	rating,
	count,
	showCount = false,
	readonly = true,
	handleRate,
}: RatingProps) {
	const [stars, setStars] = useState<JSX.Element[]>();

	useEffect(() => {
		const updatedStars: JSX.Element[] = [];
		for (let index = 0, difference, fillPercent; index < 5; index++) {
			difference = rating - index;
			if (difference > 1) fillPercent = 100;
			else if (difference < 0) fillPercent = 0;
			else fillPercent = Math.round(difference * 100);

			updatedStars[index] = (
				<Star
					key={index}
					fillPercent={fillPercent}
					fillColor="var(--rating)"
					unfillColor="var(--rating-background)"
					readonly={readonly}
					onClick={() => {
						!readonly && handleRate && handleRate(index + 1);
					}}
				/>
			);
		}
		setStars(updatedStars);
	}, [handleRate, rating, readonly]);

	return (
		<div className="flex flex-nowrap items-center rating">
			<span className="flex flex-nowrap items-center h-6">{stars}</span>
			{showCount && <span className="ml-1">{count} reviews</span>}
		</div>
	);
}

export default Rating;
