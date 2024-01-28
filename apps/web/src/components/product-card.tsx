import { Product } from "@/types";
import { Card, CardContent } from "./ui/card";
import Rating from "./rating";

interface ProductProps {
	product: Product;
}
export default function ProductCard({ product }: ProductProps) {
	return (
		<Card className="shadow">
			<CardContent className="h-full p-3">
				<div className="h-full flex flex-col">
					<div className="flex items-center justify-center h-[150px] flex-shrink-0">
						<img
							src={product.image}
							alt={product.name}
							className="object-cover h-full w-full"
						/>
					</div>
					<div className="text-sm mt-2 flex flex-col flex-grow gap-1">
						<p className="line-clamp-2 flex-grow ml-1">
							{product.name} Lorem ipsum, dolor sit amet
							consectetur adipisicing elit. Quos mollitia
							consequuntur, temporibus esse voluptatem non minus
							reiciendis ipsum at. Rem atque placeat ea ad ipsa
							aperiam voluptatum magnam nulla veritatis?
						</p>
						<Rating
							rating={product.rating}
							count={product.reviews_count}
							showCount
						/>
						<p className="font-bold ml-1">R {product.price}</p>
					</div>
				</div>
			</CardContent>
		</Card>
	);
}
